from fastapi.testclient import TestClient

from agents.models import (
    DomainExpertAnalysis,
    DomainExpertMetadata,
    Entities,
    OrchestratorMetadata,
    OrchestratorRequest,
    OrchestratorResponse,
    QueryAnalyzerMetadata,
    SourceInfo,
)
from api.app import app, get_evaluation_runner, get_orchestrator


class DummyOrchestrator:
    def __init__(self, response: OrchestratorResponse):
        self._response = response

    def process(self, request: OrchestratorRequest) -> OrchestratorResponse:
        self.last_request = request
        return self._response


class DummyEvaluationRunner:
    def __init__(self):
        self.logged = []

    def log_query(self, query: str, result):
        self.logged.append((query, result))

    def run_full_evaluation(self):
        return {"overall_score": 42}

    def get_recent_metrics(self):
        return {"overall_score": 42, "recall_at_10": 0.7, "factual_accuracy": 0.5, "avg_response_time": 0.1}


def build_response() -> OrchestratorResponse:
    entities = Entities(models=["lstm"], metrics=["sharpe"], concepts=["trading"])
    query_metadata = QueryAnalyzerMetadata(
        complexity="moderate",
        entities=entities,
        query_type="comparative",
        financial_focus="trading",
    )
    analysis = DomainExpertAnalysis(
        key_finding="LLM output",
        relevant_sections=["Results"],
        confidence=0.9,
        methodology_insights=["Uses LSTM"],
        limitations=["Small sample"],
    )
    metadata = DomainExpertMetadata(
        analysis=analysis,
        sources=[SourceInfo(section="Results", paper="Deep Trading...", relevance_score=0.95)],
    )
    return OrchestratorResponse(
        agent="Orchestrator",
        content="LLM output",
        metadata=OrchestratorMetadata(
            query_analysis=query_metadata,
            expert_analysis=metadata,
        ),
    )


def setup_overrides(response: OrchestratorResponse):
    orchestrator = DummyOrchestrator(response)
    evaluator = DummyEvaluationRunner()
    app.dependency_overrides[get_orchestrator] = lambda: orchestrator
    app.dependency_overrides[get_evaluation_runner] = lambda: evaluator
    return orchestrator, evaluator


def teardown_overrides():
    app.dependency_overrides.clear()


def test_query_endpoint_returns_orchestrator_response():
    response_payload = build_response()
    orchestrator, evaluator = setup_overrides(response_payload)
    client = TestClient(app)

    payload = {"query": "Compare LSTM and CNN"}
    result = client.post("/query", json=payload)

    teardown_overrides()

    assert result.status_code == 200
    data = result.json()
    assert data["content"] == "LLM output"
    assert orchestrator.last_request.query == payload["query"]
    assert evaluator.logged[0][0] == payload["query"]


def test_evaluate_endpoint_uses_evaluation_runner():
    response_payload = build_response()
    _, evaluator = setup_overrides(response_payload)
    client = TestClient(app)

    result = client.post("/evaluate")

    teardown_overrides()

    assert result.status_code == 200
    assert result.json()["overall_score"] == 42


def test_health_endpoint_includes_quality_metrics():
    response_payload = build_response()
    setup_overrides(response_payload)
    client = TestClient(app)

    result = client.get("/health")

    teardown_overrides()

    assert result.status_code == 200
    data = result.json()
    assert data["quality_indicators"]["overall_score"] == 42
