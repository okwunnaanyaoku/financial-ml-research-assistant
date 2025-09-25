from agents.orchestrator import Orchestrator
from agents.models import OrchestratorRequest, OrchestratorResponse

ORCH_RESPONSE = """**Answer**: LLM synthesis output

**Confidence**: High"""


class FixedSearch:
    def __init__(self, chunks):
        self._chunks = chunks

    def search(self, query: str, k: int = 5):
        return self._chunks[:k]


def _dummy_chunks():
    return [
        {
            "text": "LSTM models achieve higher Sharpe ratio compared to CNN.",
            "metadata": {"section": "Results", "paper_title": "Deep Trading Insights"},
            "hybrid_score": 0.92,
        }
    ]


def _make_orchestrator(search=None):
    orchestrator = Orchestrator()
    orchestrator._is_llm_available = lambda: True  # type: ignore[attr-defined]
    orchestrator._generate_llm_response = lambda *args, **kwargs: ORCH_RESPONSE  # type: ignore[attr-defined]

    orchestrator.query_analyzer._is_llm_available = lambda: True  # type: ignore[attr-defined]
    orchestrator.query_analyzer._generate_llm_response = (lambda *args, **kwargs: "Comparative trading analysis mentioning LSTM Sharpe metrics")  # type: ignore[attr-defined]

    orchestrator.domain_expert._is_llm_available = lambda: True  # type: ignore[attr-defined]
    orchestrator.domain_expert._generate_llm_response = (
        lambda *args, **kwargs: "Key findings include accuracy improvements. Methodology uses LSTM. Limitations include sample size."
    )  # type: ignore[attr-defined]
    orchestrator.domain_expert.search_system = search or FixedSearch(_dummy_chunks())  # type: ignore[attr-defined]
    return orchestrator


def test_orchestrator_process_dict_input():
    orchestrator = _make_orchestrator()
    response = orchestrator.process({"query": "Compare LSTM and CNN trading performance"})

    assert isinstance(response, OrchestratorResponse)
    assert response.agent == "Orchestrator"
    assert response.metadata.query_analysis.query_type in {"comparative", "factual", "methodology", "evaluation"}
    assert response.metadata.expert_analysis.analysis.key_finding
    assert response.metadata.expert_analysis.sources


def test_orchestrator_process_model_input():
    orchestrator = _make_orchestrator()
    request = OrchestratorRequest(query="How does Sharpe ratio differ across models?")
    response = orchestrator.process(request)

    assert isinstance(response, OrchestratorResponse)
    assert "Confidence" in response.content
    assert response.metadata.query_analysis.financial_focus in {"trading", "general", "equity", "cryptocurrency"}
