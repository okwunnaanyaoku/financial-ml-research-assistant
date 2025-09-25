# Financial ML Research Assistant

This repository houses a compact Retrieval-Augmented Generation (RAG) stack tailored to financial machine-learning research. PDFs are ingested once, chunked with section-aware heuristics, indexed in hybrid stores (ChromaDB + BM25), and served through a FastAPI layer that orchestrates Google Gemini responses with inline citations.

## Key Design Choices & Trade-offs
- **Section-aware chunking**: The hierarchical chunker respects document outlines and keeps ~400-token windows with 50-token overlap. This improves contextual fidelity at the cost of slightly slower ingestion for very large PDFs.
- **Hybrid retrieval**: Semantic (MiniLM) and lexical (BM25) scores are fused (`semantic_weight=0.7`). The blend captures numerics and finance jargon well, but adds an extra store to maintain.
- **Top-3 expert context**: DomainExpert trims the fused list to three chunks above a 0.3 score threshold. Latency stays low and Gemini responses stay focused, though absolute recall can drop for very broad questions.
- **Gemini orchestration**: Gemini handles both query analysis and final synthesis. It delivers strong reasoning, yet introduces external dependency, quota management, and non-zero response time.
- **Mini evaluation loop**: `/evaluate` replays 15 golden questions tied to the sample paper. It provides a sanity check for regressions but does not yet cover multi-paper corpora.

## System Architecture
1. **Ingestion (`scripts/ingest_papers.py`)** – PyMuPDF extracts text; `PaperParser` builds a section tree; `HierarchicalChunker` emits context-aware chunks saved to `data/processed_papers/`.
2. **Indexing** – ChromaDB stores MiniLM embeddings; BM25 stores lexical representations. Indices live under `data/chroma_db/` and `data/bm25_index/` (git-ignored).
3. **Agents (`src/agents/`)** – `QueryAnalyzer` classifies intent, `DomainExpert` synthesises chunk evidence, `Orchestrator` stitches the final `OrchestratorResponse`.
4. **API (`src/api/app.py`)** – FastAPI exposes `/query`, `/evaluate`, and `/health`; `EvaluationRunner` powers the golden-set scoring.

## How to Use
1. **Clone & install**
   ```bash
   git clone https://github.com/okwunnaanyaoku/financial-ml-research-assistant.git
   cd financial-ml-research-assistant
   uv venv && source .venv/bin/activate
   uv pip install --upgrade pip
   uv pip install -r requirements.txt
   ```
2. **Prepare data** – Drop PDFs into `data/raw_papers/` and run:
   ```bash
   python scripts/ingest_papers.py
   ```
3. **Configure Gemini**
   ```bash
   export GEMINI_API_KEY=your_api_key
   ```
4. **Launch the API**
   ```bash
   uvicorn src.api.app:app --reload
   ```
5. **Interact**
   - Query: `curl -X POST http://127.0.0.1:8000/query -H "Content-Type: application/json" -d '{"query": "..."}'`
   - Evaluate: `curl -X POST http://127.0.0.1:8000/evaluate`
   - Health: `curl http://127.0.0.1:8000/health`
6. **(Optional) Tests**
   ```bash
   pytest tests/test_query_analyzer.py tests/test_domain_expert.py tests/test_orchestrator.py tests/test_api.py
   ```

## Evaluation Snapshot
`/evaluate` returns blended IR + QA metrics. Current baseline (single-paper corpus):
- Retrieval: recall@10 ~ 0.64, precision@5 ~ 0.17, MRR ~ 0.42
- QA: factual accuracy ~ 0.33, average response ~ 9.6s
- Overall score: ~ 39 / 100 using weights in `config.yaml`

Use `scripts/tools/debug_chunk_ids.py` to verify that golden chunk IDs still exist after re-ingestion, and adjust prompts or retrieval weights when metrics drift.

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
