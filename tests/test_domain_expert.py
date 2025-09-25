from agents.domain_expert import DomainExpert
from agents.models import DomainExpertRequest, DomainExpertResponse, Entities, QueryAnalyzerMetadata

LLM_RESPONSE = (
    "Key findings indicate improved accuracy. Methodology uses LSTM models. "
    "Important limitations include small sample size."
)


def _metadata() -> QueryAnalyzerMetadata:
    return QueryAnalyzerMetadata(
        complexity="moderate",
        entities=Entities(models=["lstm"], metrics=["sharpe"], concepts=["trading"]),
        query_type="comparative",
        financial_focus="trading",
    )


def _make_expert(chunks):
    expert = DomainExpert()
    expert._is_llm_available = lambda: True  # type: ignore[attr-defined]
    expert._generate_llm_response = lambda *args, **kwargs: LLM_RESPONSE  # type: ignore[attr-defined]
    expert.search_system.search = lambda query, k=5: chunks  # type: ignore[attr-defined]
    return expert


def test_domain_expert_returns_structured_metadata():
    chunks = [
        {
            "text": "LSTM models achieve a higher sharpe ratio in crypto trading.",
            "metadata": {"section": "Results", "paper_title": "Deep Trading"},
            "hybrid_score": 0.9,
        }
    ]
    expert = _make_expert(chunks)

    request = DomainExpertRequest(query="Compare LSTM trading performance", query_analysis=_metadata())
    response = expert.process(request)

    assert isinstance(response, DomainExpertResponse)
    assert response.metadata.analysis.key_finding
    assert response.metadata.sources


def test_domain_expert_handles_no_chunks():
    expert = _make_expert([])

    request = DomainExpertRequest(query="Any insight?", query_analysis=_metadata())
    response = expert.process(request)

    assert response.metadata.analysis.key_finding == "No relevant information found"
    assert response.metadata.analysis.confidence == 0.0
    assert response.metadata.sources == []
