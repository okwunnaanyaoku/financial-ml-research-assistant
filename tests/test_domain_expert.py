from typing import List, Dict

import pytest

from agents.domain_expert import DomainExpert
from agents.models import DomainExpertRequest, DomainExpertResponse, QueryAnalyzerMetadata

LLM_RESPONSE = (
    "Key findings indicate improved accuracy. Methodology uses LSTM models. "
    "Important limitations include small sample size."
)


class StubSearch:
    def __init__(self, results: List[Dict]):
        self._results = results

    def search(self, query: str, k: int = 5) -> List[Dict]:
        return self._results[:k]


def _make_expert(chunks: List[Dict]) -> DomainExpert:
    expert = DomainExpert()
    expert._is_llm_available = lambda: True  # type: ignore[attr-defined]
    expert._generate_llm_response = lambda *args, **kwargs: LLM_RESPONSE  # type: ignore[attr-defined]
    expert.search_system = StubSearch(chunks)  # type: ignore[attr-defined]
    return expert


def test_domain_expert_returns_structured_metadata(sample_query_metadata: QueryAnalyzerMetadata):
    chunks = [
        {
            "text": "LSTM models achieve a higher Sharpe ratio in crypto trading.",
            "metadata": {"section": "Results", "paper_title": "Deep Trading"},
            "hybrid_score": 0.9,
        }
    ]
    expert = _make_expert(chunks)

    request = DomainExpertRequest(query="Compare LSTM trading performance", query_analysis=sample_query_metadata)
    response = expert.process(request)

    assert isinstance(response, DomainExpertResponse)
    assert response.metadata.analysis.key_finding
    assert response.metadata.sources


def test_domain_expert_handles_no_chunks(sample_query_metadata: QueryAnalyzerMetadata):
    expert = _make_expert([])

    request = DomainExpertRequest(query="Any insight?", query_analysis=sample_query_metadata)
    response = expert.process(request)

    assert response.metadata.analysis.key_finding == "No relevant information found"
    assert response.metadata.analysis.confidence == 0.0
    assert response.metadata.sources == []


def test_domain_expert_respects_ranking_and_citation_format(sample_query_metadata: QueryAnalyzerMetadata):
    ranked_chunks = [
        {
            "text": "Sharpe improves with LSTM risk controls.",
            "metadata": {"section": "Findings", "paper_title": "Very Long Financial Markets Study Title For Citation"},
            "hybrid_score": 0.91,
        },
        {
            "text": "CNN variants lag in volatile markets.",
            "metadata": {"section": "Discussion", "paper_title": "Another Extensive Research Paper Title Discussing Quantitative Strategies"},
            "hybrid_score": 0.74,
        },
        {
            "text": "Risk parity provides diversification benefits.",
            "metadata": {"section": "Appendix", "paper_title": "Risk Parity Supplemental Analysis"},
            "hybrid_score": 0.52,
        },
        {
            "text": "Lower scoring chunk that should be discarded.",
            "metadata": {"section": "Noise", "paper_title": "Irrelevant"},
            "hybrid_score": 0.21,
        },
    ]
    expert = _make_expert(ranked_chunks)

    response = expert.process(DomainExpertRequest(query="Sharpe improvements", query_analysis=sample_query_metadata))
    sources = response.metadata.sources

    assert [s.relevance_score for s in sources] == [0.91, 0.74, 0.52]
    assert [s.section for s in sources] == ["Findings", "Discussion", "Appendix"]
    assert all(source.paper.endswith("...") for source in sources)
