# Agents Overview

The system coordinates three LLM-powered agents. Each agent inherits from `BaseAgent` (a `pydantic.BaseModel`) and exchanges typed request/response models defined in `agents.models`.

## QueryAnalyzer
- **Purpose:** classify incoming queries, extract entities/intent for downstream agents.
- **Input:** `QueryAnalyzerRequest(query: str)`
- **Output:** `QueryAnalyzerResponse`
  - `metadata` is a `QueryAnalyzerMetadata` (complexity, entities, query type, financial focus).
- **Dependencies:** Gemini LLM (required), financial keyword dictionary.
- **Notes:** raises if `GEMINI_API_KEY` is missing or the LLM response cannot be parsed.

## DomainExpert
- **Purpose:** retrieve relevant chunks and analyze them with LLM expertise.
- **Input:** `DomainExpertRequest(query: str, query_analysis: QueryAnalyzerMetadata)`
- **Output:** `DomainExpertResponse`
  - `metadata.analysis` is a `DomainExpertAnalysis` (key finding, methodology insights, limitations, confidence).
  - `metadata.sources` is a list of `SourceInfo` objects.
- **Dependencies:** `HybridSearch` (Chroma + BM25), Gemini LLM (required).
- **Notes:** emits structured results or raises if Gemini fails.

## Orchestrator
- **Purpose:** orchestrate the pipeline and synthesize final responses.
- **Input:** `OrchestratorRequest(query: str)`
- **Output:** `OrchestratorResponse`
  - `metadata.query_analysis` is the analyzer metadata.
  - `metadata.expert_analysis` is the expert metadata.
- **Dependencies:** `QueryAnalyzer`, `DomainExpert`, Gemini LLM.
- **Notes:** raises if Gemini is unavailable; always returns the synthesized LLM output.

## Retrieval Stack
- **ChromaDBStore:** persistent vector search (configurable via `config.chroma_db_path`).
- **BM25Indexer:** keyword index stored under `config.bm25_index_path`.
- **HybridSearch:** wraps both stores and provides hybrid relevance scoring.

## Operational Checklist
1. `python scripts/ingest_papers.py` – build processed chunks, Chroma, and BM25 indexes.
2. Export `GEMINI_API_KEY` and ensure network access to Google Gemini.
3. Run verification tests: `pytest tests/test_query_analyzer.py tests/test_domain_expert.py tests/test_orchestrator.py`.
4. Launch API (`uvicorn src.api.app:app --reload`) and hit `/query`, `/evaluate`, `/health`.
5. Monitor `/health` quality indicators (cached after the first run).
