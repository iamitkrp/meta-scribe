from __future__ import annotations

import re
from typing import Any, Dict, Tuple
import httpx
import xml.etree.ElementTree as ET


_ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")


def _extract_arxiv_id(id_or_url: str) -> str | None:
    m = _ARXIV_ID_RE.search(id_or_url)
    if m:
        return m.group(1)
    return None


async def fetch_arxiv_pdf_and_meta(id_or_url: str, timeout_seconds: int = 30) -> Tuple[bytes, Dict[str, Any]]:
    arxiv_id = _extract_arxiv_id(id_or_url)
    if not arxiv_id:
        raise ValueError("Invalid arXiv id or URL")

    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    meta_url = f"http://export.arxiv.org/api/query?search_query=id:{arxiv_id}"

    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
        pdf_resp = await client.get(pdf_url)
        pdf_resp.raise_for_status()
        meta_resp = await client.get(meta_url)
        meta_resp.raise_for_status()

    meta: Dict[str, Any] = {"title": None, "abstract": None}
    try:
        root = ET.fromstring(meta_resp.text)
        # Atom namespace handling
        ns = {"a": "http://www.w3.org/2005/Atom"}
        entry = root.find("a:entry", ns)
        if entry is not None:
            title_node = entry.find("a:title", ns)
            summary_node = entry.find("a:summary", ns)
            if title_node is not None:
                meta["title"] = (title_node.text or "").strip()
            if summary_node is not None:
                meta["abstract"] = (summary_node.text or "").strip()
    except Exception:
        pass

    return pdf_resp.content, meta


