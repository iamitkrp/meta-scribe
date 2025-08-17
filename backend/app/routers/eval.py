from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import re
from ..db import get_session
from ..models import Evaluation, Run


router = APIRouter()


class EvalRequest(BaseModel):
    run_id: int
    # Metric instructions: regex to capture a float from stdout and compare with reported
    metrics: List[dict]
    # Each metric dict: { name, pattern, reported, direction ('higher'|'lower'), threshold }


class EvalResponse(BaseModel):
    results: List[dict]


@router.post("/evaluate", response_model=EvalResponse)
async def evaluate_run(req: EvalRequest) -> EvalResponse:
    with get_session() as session:
        run = session.get(Run, req.run_id)
        if not run:
            return EvalResponse(results=[])

        results = []
        for cfg in req.metrics:
            name = cfg.get("name")
            pattern = cfg.get("pattern")
            reported = float(cfg.get("reported"))
            direction = cfg.get("direction", "higher")
            threshold = float(cfg.get("threshold", 0.0))
            measured_val = None
            if pattern:
                m = re.search(pattern, run.stdout)
                if m:
                    try:
                        measured_val = float(m.group(1))
                    except Exception:
                        measured_val = None
            if measured_val is None:
                measured_val = 0.0
            delta = measured_val - reported
            ev = Evaluation(
                run_id=run.id,
                metric_name=name,
                reported=reported,
                measured=measured_val,
                direction=direction,
                delta=delta,
                threshold=threshold,
                pattern=pattern,
            )
            session.add(ev)
            results.append({
                "name": name,
                "reported": reported,
                "measured": measured_val,
                "delta": delta,
                "direction": direction,
                "threshold": threshold,
                "pass": (measured_val >= reported - threshold) if direction == "higher" else (measured_val <= reported + threshold),
            })
        session.commit()
    return EvalResponse(results=results)


@router.get("/runs")
async def list_runs() -> list[dict]:
    with get_session() as session:
        runs = session.query(Run).order_by(Run.created_at.desc()).limit(50).all()
        return [
            {
                "id": r.id,
                "created_at": r.created_at.isoformat(),
                "returncode": r.returncode,
                "stdout": r.stdout[:1000],
            }
            for r in runs
        ]


