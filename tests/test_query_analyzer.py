from pydantic import ValidationError

from agents.query_analyzer import QueryAnalyzer
from agents.models import QueryAnalyzerRequest, QueryAnalyzerResponse

MOCK_RESPONSE = ("""
Comparative analysis of trading models.
This response discusses crypto markets and mentions LSTM models and Sharpe metrics.
""")

def _make_analyzer() -> QueryAnalyzer:
    analyzer = QueryAnalyzer()
    analyzer._is_llm_available = lambda: True  # type: ignore[attr-defined]
    analyzer._generate_llm_response = lambda *args, **kwargs: MOCK_RESPONSE  # type: ignore[attr-defined]
    return analyzer

def test_process_returns_response_model():
    analyzer = _make_analyzer()
    result = analyzer.process({"query": "Compare LSTM and CNN trading performance"})
    assert isinstance(result, QueryAnalyzerResponse)
    assert result.agent == "QueryAnalyzer"
    assert result.metadata.query_type in {"comparative", "factual", "methodology", "evaluation"}

def test_process_accepts_request_model():
    analyzer = _make_analyzer()
    request = QueryAnalyzerRequest(query="How does volatility affect trading models?")
    result = analyzer.process(request)
    assert result.metadata.financial_focus in {"trading", "general", "equity", "cryptocurrency"}

def test_request_validation_enforces_non_empty_query():
    try:
        QueryAnalyzerRequest(query="   ")
    except ValidationError:
        return
    raise AssertionError("Whitespace-only query should raise ValidationError")

def test_entities_extracted_from_llm_response():
    analyzer = _make_analyzer()
    result = analyzer.process({"query": "Evaluate LSTM accuracy and Sharpe ratio in trading"})
    metadata = result.metadata
    assert "lstm" in metadata.entities.models
    assert metadata.query_type == "comparative"
