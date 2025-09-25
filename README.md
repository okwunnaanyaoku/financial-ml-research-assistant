# Financial ML Research Assistant

This repository houses a compact Retrieval-Augmented Generation (RAG) stack tailored to financial machine-learning research. PDFs are ingested once, chunked with section-aware heuristics, indexed in hybrid stores (ChromaDB + BM25), and served through a FastAPI layer that orchestrates Google Gemini responses with inline citations.

## Key Design Choices & Trade-offs
- **Section-aware chunking**: The hierarchical chunker respects document outlines and keeps ~400-token windows with 50-token overlap. This improves contextual fidelity at the cost of slightly slower ingestion for very large PDFs.
- **Hybrid retrieval**: Semantic (MiniLM) and lexical (BM25) scores are fused (`semantic_weight=0.7`). The blend captures numerics and finance jargon well, but adds an extra store to maintain.
- **Top-3 expert context**: DomainExpert trims the fused list to three chunks above a 0.3 score threshold. Latency stays low and Gemini responses stay focused, though absolute recall can drop for very broad questions.
- **Gemini 2.5 Flash Lite**: The default model keeps API latency manageable on modest hardware, trading a bit of reasoning power compared to the flagship Gemini models.
- **Mini evaluation loop**: `/evaluate` replays 15 golden questions tied to the sample paper. It provides a quick regression check but does not yet cover multi-paper corpora.

## High-Level Architecture
1. **Ingestion Pipeline (`scripts/ingest_papers.py`)**
   - Extract PDF text with PyMuPDF (`fitz`).
   - Parse document structure via the PDF outline (fallback to full document when absent).
   - Chunk content using the hierarchical strategy (max 400 GPT-4 tokens, 50 overlap) while respecting section boundaries.
   - Persist processed chunks to `data/processed_papers/` and refresh both ChromaDB and BM25 indexes.
2. **Hybrid Retrieval (`src/retrieval/hybrid_search.py`)**
   - Fetch top-k candidates from Chroma (semantic) and BM25 (keyword).
   - Combine scores with configurable weighting (default `semantic_weight=0.7`).
3. **Agents (`src/agents/`)**
   - `QueryAnalyzer` classifies intent and extracts entities via Gemini.
   - `DomainExpert` pulls the highest-scoring chunks (score >= 0.3) and asks Gemini for analysis.
   - `Orchestrator` coordinates the flow, synthesises the final answer, and surfaces citations.
4. **API Layer (`src/api/app.py`)**
   - FastAPI app exposing `/query`, `/evaluate`, and `/health` with typed models.
5. **Evaluation Loop (`tests/evaluation/eval_runner.py`)**
   - Mini benchmark over a curated golden dataset (15 questions; first 3 cached for health checks).

## End-to-End Query Flow
1. **API ingress** – client sends `POST /query`; FastAPI validates `OrchestratorRequest`.
2. **Query analysis** – `QueryAnalyzer` enriches the request via Gemini (with rule-based fallback).
3. **Hybrid retrieval** – `HybridSearch` gathers semantic and lexical matches, normalises scores, and fuses the ranked list.
4. **Expert chunk selection** – `DomainExpert` keeps the top chunks above 0.3 and preserves section metadata for citations.
5. **Domain synthesis** – Gemini processes the shortlisted context using `prompts/domain_expert/content_analysis.txt`.
6. **Final orchestration** – The orchestrator feeds the analysis, question, and metadata into `prompts/orchestrator/response_synthesis.txt` to produce the user-facing answer.
7. **Response + logging** – The API returns the `OrchestratorResponse`; the evaluation runner can log the interaction for offline scoring.

## Chunking & Retrieval Engine
### Chunking pipeline
- **PDF extraction**: `PDFExtractor` uses PyMuPDF to capture text spans, bounding boxes, and page numbers.
- **Structured section detection**: `PaperParser` walks the outline when available; otherwise it creates a single top-level section.
- **Hierarchical chunker**: `HierarchicalChunker` emits contiguous, context-aware chunks that never cross headings and enforces the 400-token + 50-overlap windows.
- **Post-processing**: Each chunk receives `chunk_id`, section title, hierarchy level, page span, character count, and token count for downstream auditing.

### Hybrid retrieval
- **Vector search**: ChromaDB stores `all-MiniLM-L6-v2` embeddings and returns the top-k semantic matches (default 5).
- **Sparse search**: The BM25 index captures exact term matches, boosting numerical and jargon-heavy questions.
- **Score fusion**: `HybridSearch` normalises semantic and lexical scores, blends them via `semantic_weight`, deduplicates chunk IDs, and sorts by the fused score.
- **Section alignment**: Because chunks never straddle sections, citations map cleanly to the same segments referenced in the golden dataset.

## Evaluation & Benchmarking
### Execution flow
- `/query` runs the full agent pipeline, optionally logging results for evaluation.
- `/evaluate` iterates over the 15 golden questions, computing retrieval and QA metrics, then caches the output.
- `/health` serves the cached metrics; the first call triggers `/evaluate` if needed.

### Golden dataset
- Finance ML questions covering models, data, features, and performance from the included sample paper.
- Each entry specifies accepted answers (`golden_answer`), expected sections, and authoritative chunk IDs.
- Extend `tests/evaluation/golden_dataset.json` as new papers are ingested.

### Metrics captured
- **Recall@k / Precision@k** – coverage vs concentration of relevant chunks.
- **MRR / MAP** – rank-sensitive retrieval quality.
- **QA factual accuracy** – substring match against `golden_answer` variants.
- **Average response time** – mean latency per answer.
- **Overall score** – weighted blend (weights in `config.yaml`).

### Improving retrieval & QA metrics
- Ensure chunk alignment after re-ingestion via `uv run --python .venv/bin/python python scripts/tools/debug_chunk_ids.py`.
- Tweak `HierarchicalChunker` settings when section-specific recall drops.
- Adjust `semantic_weight` or add reranking (e.g., `sentence-transformers/ms-marco-MiniLM-L-6-v3`).
- Tune prompts for explicit, citation-rich answers and broaden `golden_answer` variants.
- Monitor latency: reduce `MAX_CHUNKS_FOR_LLM` or switch to lighter models if responses slow down.
- Grow the benchmark with new questions per paper to expose blind spots.

## How to Use
1. **Clone & install**
   ```bash
   git clone https://github.com/okwunnaanyaoku/financial-ml-research-assistant.git
   cd financial-ml-research-assistant
   uv venv && source .venv/bin/activate
   uv pip install --upgrade pip
   uv pip install -r requirements.txt
   ```
2. **Prepare data** – drop PDFs into `data/raw_papers/` and run `python scripts/ingest_papers.py`.
3. **Configure Gemini** – `export GEMINI_API_KEY=your_api_key`.
4. **Launch the API** – `uvicorn src.api.app:app --reload`.
5. **Interact**
   - Query: `curl -X POST http://127.0.0.1:8000/query -H "Content-Type: application/json" -d '{"query": "..."}'`
   - Evaluate: `curl -X POST http://127.0.0.1:8000/evaluate`
   - Health: `curl http://127.0.0.1:8000/health`
6. **(Optional) Tests** – `pytest tests/test_query_analyzer.py tests/test_domain_expert.py tests/test_orchestrator.py tests/test_api.py`

## Evaluation Snapshot
`/evaluate` currently reports (single-paper corpus):
- Retrieval: recall@10 ~ 0.64, precision@5 ~ 0.17, MRR ~ 0.42
- QA: factual accuracy ~ 0.33, average response ~ 9.6s
- Overall score: ~ 39 / 100

## Project Layout
```
src/
  agents/          QueryAnalyzer, DomainExpert, Orchestrator, shared models
  ingestion/       PDFExtractor, PaperParser, HierarchicalChunker
  indexing/        ChromaDBStore, BM25Indexer
  retrieval/       HybridSearch fusion logic
  api/             FastAPI entry point
  llm/             Gemini client + retry logic
scripts/tools/     Debug utilities (search, chunking, metrics)
tests/             Agent + API tests, evaluation harness
```
