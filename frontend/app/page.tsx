"use client";

import { useEffect, useRef, useState } from "react";
import type { ParseResponse } from "./types";

export default function Home() {
  const [pdf, setPdf] = useState<File | null>(null);
  const [methodology, setMethodology] = useState<string>("");
  const [pseudocode, setPseudocode] = useState<string>("");
  const [code, setCode] = useState<string>("");
  const [runOut, setRunOut] = useState<string>("");
  const [provider, setProvider] = useState<string>("gemini");
  const [apiKey, setApiKey] = useState<string>("");
  const [loading, setLoading] = useState<{parse:boolean; pseudo:boolean; code:boolean; run:boolean}>({parse:false,pseudo:false,code:false,run:false});
  const [parsed, setParsed] = useState<ParseResponse | null>(null);
  const dropRef = useRef<HTMLDivElement | null>(null);
  const [arxivUrl, setArxivUrl] = useState<string>("");

  const uploadPdf = async () => {
    if (!pdf) return;
    const fd = new FormData();
    fd.append("file", pdf);
    setLoading((s) => ({...s, parse:true}));
    try {
      const res = await fetch("/api/papers/parse", { method: "POST", body: fd });
      const data: ParseResponse = await res.json();
      setParsed(data);
      setMethodology(data.methodology ?? "");
    } finally {
      setLoading((s) => ({...s, parse:false}));
    }
  };

  const fetchArxiv = async () => {
    if (!arxivUrl.trim()) return;
    setLoading((s) => ({...s, parse:true}));
    try {
      const res = await fetch("/api/papers/parse-arxiv", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: arxivUrl.trim() }),
      });
      const data: ParseResponse = await res.json();
      setParsed(data);
      setMethodology(data.methodology ?? "");
    } finally {
      setLoading((s) => ({...s, parse:false}));
    }
  };

  const genPseudo = async () => {
    setLoading((s)=>({...s,pseudo:true}));
    try {
      const res = await fetch("/api/pseudocode/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ methodology, provider, api_key: apiKey }),
      });
      const data = await res.json();
      setPseudocode(data.pseudocode ?? "");
    } finally {
      setLoading((s)=>({...s,pseudo:false}));
    }
  };

  const genCode = async () => {
    setLoading((s)=>({...s,code:true}));
    try {
      const res = await fetch("/api/codegen/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pseudocode, framework: "pytorch", provider, api_key: apiKey }),
      });
      const data = await res.json();
      setCode(data.code ?? "");
    } finally {
      setLoading((s)=>({...s,code:false}));
    }
  };

  const run = async () => {
    setLoading((s)=>({...s,run:true}));
    try {
      const res = await fetch("/api/experiment/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      const data = await res.json();
      setRunOut(`${data.returncode}\n${data.stdout}\n${data.stderr}`);
    } finally {
      setLoading((s)=>({...s,run:false}));
    }
  };

  useEffect(() => {
    const el = dropRef.current;
    if (!el) return;
    const onDragOver = (e: DragEvent) => { e.preventDefault(); el.classList.add("dragover"); };
    const onDragLeave = () => { el.classList.remove("dragover"); };
    const onDrop = (e: DragEvent) => {
      e.preventDefault();
      el.classList.remove("dragover");
      const f = (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) || null;
      if (f && (f as any).type === "application/pdf") setPdf(f as unknown as File);
    };
    el.addEventListener("dragover", onDragOver as any);
    el.addEventListener("dragleave", onDragLeave as any);
    el.addEventListener("drop", onDrop as any);
    return () => {
      el.removeEventListener("dragover", onDragOver as any);
      el.removeEventListener("dragleave", onDragLeave as any);
      el.removeEventListener("drop", onDrop as any);
    };
  }, []);

  const copy = async (text: string) => {
    try { await navigator.clipboard.writeText(text); } catch {}
  };

  return (
    <div className="container">
      <header className="header">
        <div>
          <div className="brand">METASCRIBE</div>
          <div className="subtle">AI Agent for Research Paper Implementation</div>
        </div>
      </header>

      <div className="stepper">
        <div className={`step ${methodology ? 'active' : ''}`}>1. Upload</div>
        <div className={`step ${methodology ? 'active' : ''}`}>2. Parse</div>
        <div className={`step ${pseudocode ? 'active' : ''}`}>3. Pseudocode</div>
        <div className={`step ${code ? 'active' : ''}`}>4. Code</div>
        <div className={`step ${runOut ? 'active' : ''}`}>5. Run</div>
      </div>

      <div className="grid grid-2" style={{ marginTop: 10 }}>
        <section className="card">
          <h3>LLM Settings</h3>
          <div className="row" style={{ marginTop: 8 }}>
            <label className="subtle" style={{ minWidth: 80 }}>Provider</label>
            <select className="select" value={provider} onChange={(e) => setProvider(e.target.value)}>
              <option value="gemini">Gemini</option>
            </select>
          </div>
          <div className="row" style={{ marginTop: 8 }}>
            <label className="subtle" style={{ minWidth: 80 }}>API Key</label>
            <input className="input" type="password" placeholder="Paste your API Key" value={apiKey} onChange={(e) => setApiKey(e.target.value)} />
          </div>
        </section>

        <section className="card">
          <h3>Upload PDF</h3>
          <div ref={dropRef} className="dropzone" style={{ marginTop: 8 }}>
            Drag & drop PDF here or click to select
          </div>
          <div className="row" style={{ marginTop: 8 }}>
            <input className="input" type="file" accept="application/pdf" onChange={(e) => setPdf(e.target.files?.[0] ?? null)} />
            <button className="btn btn-primary" onClick={uploadPdf} disabled={!pdf || loading.parse}>{loading.parse ? 'Parsing...' : 'Parse'}</button>
          </div>
          <div className="subtle" style={{ marginTop: 8 }}>PDF se methodology, equations aur datasets nikalenge.</div>
          <div className="row" style={{ marginTop: 14 }}>
            <input className="input" placeholder="arXiv URL or ID (e.g., 1706.03762)" value={arxivUrl} onChange={(e)=>setArxivUrl(e.target.value)} />
            <button className="btn" onClick={fetchArxiv} disabled={!arxivUrl || loading.parse}>{loading.parse ? 'Fetching...' : 'Fetch arXiv'}</button>
          </div>
        </section>
      </div>

      <div className="grid" style={{ marginTop: 16 }}>
        {parsed && (
          <section className="card">
            <div className="toolbar">
              <h3>Parse Results</h3>
              <div className="actions">
                <button className="btn btn-ghost" onClick={() => copy(parsed.abstract || '')}>Copy Abstract</button>
                <button className="btn btn-ghost" onClick={() => copy((parsed.equations||[]).join('\n'))}>Copy Equations</button>
              </div>
            </div>
            {parsed.abstract && (
              <div style={{ marginBottom: 10 }}>
                <div className="subtle" style={{ marginBottom: 6 }}>Abstract</div>
                <div className="codeblock">{parsed.abstract}</div>
              </div>
            )}
            {parsed.datasets?.length ? (
              <div style={{ marginTop: 8 }}>
                <div className="subtle" style={{ marginBottom: 6 }}>Datasets</div>
                <div className="chips">
                  {parsed.datasets.map((d) => (<span key={d} className="chip">{d}</span>))}
                </div>
              </div>
            ) : null}
            {parsed.equations?.length ? (
              <div style={{ marginTop: 8 }}>
                <div className="subtle" style={{ marginBottom: 6 }}>Equations</div>
                <div className="codeblock">{parsed.equations.join('\n\n')}</div>
              </div>
            ) : null}
          </section>
        )}
        <section className="card">
          <div className="toolbar">
            <h3>Methodology</h3>
            <div className="kpi">Step 2</div>
          </div>
          <textarea className="textarea" value={methodology} onChange={(e) => setMethodology(e.target.value)} rows={8} />
          <div className="row" style={{ marginTop: 8 }}>
            <button className="btn btn-primary" onClick={genPseudo} disabled={!methodology || loading.pseudo}>{loading.pseudo ? 'Generating...' : 'Generate pseudocode'}</button>
            <button className="btn btn-ghost" onClick={() => setMethodology("")}>Clear</button>
          </div>
        </section>

        <section className="card">
          <div className="toolbar">
            <h3>Pseudocode</h3>
            <div className="kpi">Step 3</div>
          </div>
          <textarea className="textarea" value={pseudocode} onChange={(e) => setPseudocode(e.target.value)} rows={10} />
          <div className="row" style={{ marginTop: 8 }}>
            <button className="btn btn-primary" onClick={genCode} disabled={!pseudocode || loading.code}>{loading.code ? 'Generating...' : 'Generate code'}</button>
            <button className="btn btn-ghost" onClick={() => setPseudocode("")}>Clear</button>
          </div>
        </section>
      </div>

      <div className="grid" style={{ marginTop: 16 }}>
        <section className="card">
          <div className="toolbar">
            <h3>Generated Code</h3>
            <div className="kpi">Step 4</div>
          </div>
          <textarea className="textarea" value={code} onChange={(e) => setCode(e.target.value)} rows={14} style={{ fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace' }} />
          <div className="row" style={{ marginTop: 8 }}>
            <button className="btn btn-primary" onClick={run} disabled={!code || loading.run}>{loading.run ? 'Running...' : 'Run'}</button>
            <button className="btn btn-ghost" onClick={() => setCode("")}>Clear</button>
          </div>
        </section>

        <section className="card">
          <div className="toolbar">
            <h3>Run Output</h3>
            <div className="kpi">Step 5</div>
          </div>
          <pre className="codeblock">{runOut}</pre>
        </section>
      </div>
    </div>
  );
}
