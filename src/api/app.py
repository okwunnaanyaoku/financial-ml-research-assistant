
from fastapi import Depends, FastAPI, HTTPException
import sys
from pathlib import Path

root_path = Path(__file__).parent.parent
sys.path.extend([str(root_path), str(root_path.parent / 'tests/evaluation')])

from agents.models import OrchestratorRequest, OrchestratorResponse
from agents.orchestrator import Orchestrator
from eval_runner import EvaluationRunner

app = FastAPI(title="Financial ML Research Assistant", version="1.0.0")

_orchestrator = Orchestrator()
_eval_runner = EvaluationRunner()

def get_orchestrator() -> Orchestrator:
    return _orchestrator


def get_evaluation_runner() -> EvaluationRunner:
    return _eval_runner


@app.post("/query", response_model=OrchestratorResponse)
async def query_papers(
    request: OrchestratorRequest,
    orchestrator: Orchestrator = Depends(get_orchestrator),
    eval_runner: EvaluationRunner = Depends(get_evaluation_runner),
) -> OrchestratorResponse:
    try:
        result = orchestrator.process(request)
        eval_runner.log_query(request.query, result)
        return result
    except Exception as exc:  # pragma: no cover - allow API to surface error
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/evaluate")
async def run_evaluation(
    eval_runner: EvaluationRunner = Depends(get_evaluation_runner),
):
    try:
        return eval_runner.run_full_evaluation()
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/health")
async def health_check(
    eval_runner: EvaluationRunner = Depends(get_evaluation_runner),
):
    try:
        health_data = {
            "status": "healthy",
            "components": {"orchestrator": "operational", "evaluation": "operational"},
        }

        recent_metrics = _get_quality_indicators(eval_runner)
        if recent_metrics:
            health_data["quality_indicators"] = recent_metrics

        return health_data
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def _get_quality_indicators(eval_runner: EvaluationRunner):
    try:
        return eval_runner.get_recent_metrics()
    except Exception:  # pragma: no cover
        return None
