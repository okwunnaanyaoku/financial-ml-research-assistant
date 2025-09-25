# Financial ML Research Assistant

This project delivers an end-to-end Retrieval-Augmented Generation (RAG) assistant for financial machine-learning research. It ingests academic PDFs, builds hybrid search indices (ChromaDB + BM25), and serves LLM-backed answers with inline citations through a FastAPI interface. The core agents run on Google Gemini; you can obtain a free API key at https://ai.google.dev/gemini-api/docs.

## High-Level Architecture
1. **Ingestion Pipeline** (`scripts/ingest_papers.py`)
   - Extract PDF text with PyMuPDF (`fitz`).
   - Parse document structure via the PDF outline (fallback to full document where absent).
   - Chunk content using a hierarchical strategy that respects section boundaries and GPT-4 token counting (max 400 tokens, 50 overlap).
   - Persist processed chunks to `data/processed_papers/` and update both ChromaDB and BM25 indexes.
2. **Hybrid Retrieval** (`src/retrieval/hybrid_search.py`)
   - Fetch k candidates from Chroma (semantic) and BM25 (keyword).
   - Combine scores with configurable weighting (default `semantic_weight=0.7`).
3. **Agents** (`src/agents/`)
   - `QueryAnalyzer`: classifies the question and extracts entities using Gemini.
   - `DomainExpert`: pulls top search results, filters to the three highest scoring chunks (score >= 0.3), and asks Gemini for a structured synthesis.
   - `Orchestrator`: coordinates the flow, performs final LLM synthesis, and surfaces metadata + citations.
4. **API Layer** (`src/api/app.py`)
   - FastAPI application exposing `/query`, `/evaluate`, and `/health` endpoints with typed request/response models.
5. **Evaluation Loop** (`tests/evaluation/eval_runner.py`)
   - Mini benchmark over a curated golden dataset (3 samples are used for the cached health metrics).

## End-to-End Query Flow
1. **API ingress** � A client sends POST /query with the user question. FastAPI validates the payload against OrchestratorRequest and passes it to the orchestrator agent.
2. **Query analysis** � QueryAnalyzer enriches the request. It first tries Gemini (prompts/query_analyzer/financial_classification.txt) to classify complexity, entities, question type, and financial focus; it falls back to rule-based heuristics when the LLM is unavailable.
3. **Hybrid retrieval** � The orchestrator invokes HybridSearch. The retriever executes parallel searches against ChromaDB (semantic embeddings) and BM25 (lexical). Scores are normalised and fused (semantic_weight from config.yaml), producing a ranked candidate list.
4. **Expert chunk selection** � DomainExpert keeps the top-scoring chunks above the 0.3 hybrid-score threshold (up to three). Each chunk retains section metadata so we can cite the original paper.
5. **Domain synthesis** � Using prompts/domain_expert/content_analysis.txt, Gemini analyses the shortlisted chunks and returns a structured DomainExpertResponse containing key findings, methodology insights, limitations, and citations.
6. **Final orchestration** � The orchestrator feeds the expert analysis, original question, and query metadata into prompts/orchestrator/response_synthesis.txt. Gemini generates the final narrative answer, which is wrapped in an OrchestratorResponse together with provenance (metadata.expert_analysis.sources).
7. **Response + logging** � The API returns the JSON payload to the caller. The evaluation runner optionally logs the interaction for /evaluate so the same pipeline can be scored against the golden dataset.

## Chunking & Retrieval Engine
### Chunking pipeline
- **PDF extraction**: `PDFExtractor` relies on PyMuPDF (`fitz`) to capture text spans, bounding boxes, and page numbers so downstream components can reason about layout.
- **Structured section detection**: `PaperParser` walks the PDF outline when it is available. Each heading becomes a logical section id; when outlines are missing, the parser synthesises a single top-level section so chunks still have stable metadata.
- **Hierarchical chunker**: `HierarchicalChunker` traverses the section tree and emits contiguous, context-aware chunks that never cross section boundaries. Sentences are grouped until ~400 GPT-4 tokens, then the chunk is closed with a 50-token overlap so adjacent context is preserved for retrieval. This keeps semantic units together while staying within LLM context limits.
- **Post-processing**: every chunk receives deterministic ids (`chunk_{n}`), the originating section title, hierarchy level, page span, character counts, and token counts. The metadata is stored alongside the text and fuels evaluation, citation rendering, and future audits.

### Hybrid retrieval
- **Vector search**: ChromaDB stores `all-MiniLM-L6-v2` embeddings for each chunk. We query the top-k semantic matches (default 5).
- **Sparse search**: the BM25 index (via `rank_bm25`) captures exact term matches, which helps with numerical facts and explicit terminology.
- **Score fusion**: `HybridSearch` normalises each candidate's semantic and lexical scores, combines them using a configurable weight (`semantic_weight` defaults to 0.7), deduplicates chunk ids, and sorts by the blended score. The DomainExpert filters this list to the three highest-scoring items above a 0.3 threshold before invoking Gemini.
- **Why section boundaries matter**: because chunks never straddle headings, a retrieved span can be mapped back to the same section used in the golden dataset. This alignment keeps recall@k and citation quality high even when PDFs evolve.

## Evaluation & Benchmarking
### Execution flow
1. `/query` sends the user's question through the orchestrator, logs the request, and returns a structured `OrchestratorResponse` with citations and agent metadata.
2. `/evaluate` iterates over the golden dataset (15 questions by default), runs both retrieval-only and full RAG evaluations, and caches the resulting metrics so they can be surfaced quickly.
3. `/health` reads the cached metrics; the first call will trigger `/evaluate` automatically if no cache exists.

### Golden dataset
- Curated finance ML questions that map to the included sample paper: model comparisons, data coverage, feature engineering, and performance numbers.
- Each entry lists accepted answers (`golden_answer`), expected sections, and the authoritative chunk ids so we can verify retrieval fidelity.
- Extend `tests/evaluation/golden_dataset.json` with additional questions when you ingest more papers; the evaluation runner consumes anything in that array.

### Metrics captured
- **Recall@k / Precision@k**: fraction of golden chunk ids retrieved within the top *k*. Recall speaks to coverage; precision shows how concentrated relevant items are at the top.
- **Mean Reciprocal Rank (MRR)**: average of `1 / rank` for the first relevant chunk. It punishes correct answers that appear lower in the list.
- **Mean Average Precision (MAP)**: averages precision at every position where a relevant chunk is found, rewarding consistent ordering of relevant context.
- **QA factual accuracy**: percentage of questions whose answers contain any of the accepted strings. Augment `golden_answer` with synonyms or numeric ranges to avoid false negatives.
- **Average response time**: mean wall-clock runtime per answer, measured across the orchestrator calls during evaluation.
- **Overall score**: weighted blend of retrieval metrics and QA accuracy. The weights live in `config.yaml` (`eval_retrieval_weight`, `eval_recall_weight`, etc.).

### Baseline performance
```json
{
  "dataset_size": 15,
  "retrieval_metrics": {
    "recall_at_5": 0.49,
    "recall_at_10": 0.64,
    "precision_at_5": 0.17,
    "precision_at_10": 0.11,
    "mrr": 0.42,
    "map": 0.37
  },
  "qa_metrics": {
    "factual_accuracy": 0.33,
    "avg_response_time": 9.6,
    "correct_answers": 5
  },
  "overall_score": 39.46
}
```
Use this as a regression guard; higher recall@k, MRR, and factual accuracy indicate healthier retrieval and answer synthesis.

## Improving Retrieval & QA Metrics
- **Ensure chunk alignment**: run `uv run --python .venv/bin/python python debug_chunk_ids.py` after re-ingestion to confirm every golden `chunk_*` id still exists. Missing ids depress recall and MRR regardless of LLM quality.
- **Refine chunk boundaries**: if recall is low for section-specific questions, adjust `HierarchicalChunker` settings (`max_tokens`, `overlap`) or enhance outline parsing so critical paragraphs remain in a single chunk.
- **Tweak score fusion**: experiment with `semantic_weight`, BM25 candidate counts, or additional reranking. Increasing lexical weight often boosts precision@k for numeric-heavy questions; stronger semantic weight can improve coverage.
- **Add a reranking stage**: pass the fused candidate list through a lexical or cross-encoder reranker (e.g., `sentence-transformers/ms-marco-MiniLM-L-6-v3`). Promoting the most relevant chunk before Gemini sees it typically lifts precision@k and MRR without altering ingestion.
- **Prompt for explicit answers**: modify `prompts/domain_expert/content_analysis.txt` and `prompts/orchestrator/response_synthesis.txt` to ask the LLM for structured bullet lists with numeric values, improving the odds of matching `golden_answer` strings.
- **Broaden golden answers**: add alternate phrasings (e.g., `"sixty-seven to eighty-four percent"`) or tolerance ranges when the assistant gives correct but differently formatted responses.
- **Instrument latency**: if average response time spikes, trim `MAX_CHUNKS_FOR_LLM`, switch to a lighter Gemini model, or cache intermediate embeddings.
- **Grow the benchmark**: append new questions per paper and categorise them (methodology, features, performance) to expose blind spots and prevent regressions as the corpus expands.

## Getting Started

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) CLI (optional but recommended; instructions below use it).
- Google Gemini API key (obtain a free key at https://ai.google.dev/gemini-api/docs). Export it as `GEMINI_API_KEY`.

### Setup
```bash
uv venv
source .venv/bin/activate
uv pip install --upgrade pip
uv pip install -r requirements.txt
```

### Ingest Papers
Place PDFs in `data/raw_papers/` (the repo ships with sample files). Then run:
```bash
python scripts/ingest_papers.py
```
This will:
- Write processed chunks to `data/processed_papers/`.
- Build/refresh ChromaDB under `data/chroma_db/`.
- Build/refresh BM25 under `data/bm25_index/`.

### Environment Variables
```bash
export GEMINI_API_KEY=your_api_key
```
The agents require Gemini; if the key is missing, they raise immediately so failures are obvious.

## Testing
Run the core suite:
```bash
pytest tests/test_query_analyzer.py tests/test_domain_expert.py tests/test_orchestrator.py tests/test_api.py
```
Target retrieval validation (ensure ingestion was run first):
```bash
python scripts/tools/test_search.py
```

## FastAPI Server
Start the API after ingestion and exporting your key:
```bash
uvicorn src.api.app:app --reload
```
Endpoints:
- `POST /query` � accepts `{ "query": "..." }` and returns the `OrchestratorResponse` JSON.
- `POST /evaluate` � runs the mini evaluation (3 samples) to warm cached metrics.
- `GET /health` � returns service status plus cached metrics (first call triggers evaluation).

Interact via Swagger UI (`http://127.0.0.1:8000/docs`) or curl:
```bash
curl -X POST http://127.0.0.1:8000/query      -H "Content-Type: application/json"      -d '{"query": "what social media sources were used in this paper?"}'
```

## Querying the Assistant
1. Ensure the ingestion pipeline has run and `uvicorn src.api.app:app --reload` is active (see sections above).
2. Issue a request to `/query` with a JSON body containing the user prompt:
   ```bash
   curl -X POST http://127.0.0.1:8000/query \
        -H "Content-Type: application/json" \
        -d '{
              "query": "What neural networks were compared in the cryptocurrency study?"
            }'
   ```
3. Successful responses follow the `OrchestratorResponse` schema:
   ```json
   {
     "agent": "Orchestrator",
     "content": "... synthesized answer ...",
     "metadata": {
       "query_analysis": { "complexity": "factual", ... },
       "expert_analysis": {
         "analysis": {
           "key_finding": "...",
           "relevant_sections": ["2.1 Technical Indicators", "6 Conclusions"],
           "confidence": 0.78,
           "limitations": ["..."]
         },
         "sources": [
           {
             "section": "2.1 Technical Indicators",
             "paper": "arXiv:2102.08189v2 ...",
             "relevance_score": 0.52
           }
         ]
       }
     }
   }
   ```
   - `content` is the final narrative returned to clients.
   - `metadata.expert_analysis.sources` lists the cited chunks with relevance scores.
   - `query_analysis` echoes the classifier output (complexity, entities, focus) for telemetry.
4. To evaluate in bulk, call `/evaluate` which runs the golden dataset and returns aggregate metrics; see the Evaluation section for interpretation.
5. When scripting integrations, reuse the same JSON contract. Example (Python):
   ```python
   import requests

   payload = {"query": "How many hourly observations were used in the analysis?"}
   response = requests.post("http://127.0.0.1:8000/query", json=payload, timeout=30)
   response.raise_for_status()
   data = response.json()
   print(data["content"])
   for source in data["metadata"]["expert_analysis"]["sources"]:
       print(source)
   ```
   This mirrors the curl call and is useful for notebook-based workflows or regression tests.

## How to Use
1. **Clone the repository**
   ```bash
   git clone https://github.com/okwunnaanyaoku/financial-ml-research-assistant.git
   cd financial-ml-research-assistant
   ```
2. **Set up the environment** (uv recommended)
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install --upgrade pip
   uv pip install -r requirements.txt
   ```
3. **Ingest papers** (place PDFs in `data/raw_papers/` first)
   ```bash
   python scripts/ingest_papers.py
   ```
4. **Export your Gemini API key**
   ```bash
   export GEMINI_API_KEY=your_api_key
   ```
5. **Run the FastAPI service**
   ```bash
   uvicorn src.api.app:app --reload
   ```
6. **Interact with the assistant**
   - Query: `curl -X POST http://127.0.0.1:8000/query -H "Content-Type: application/json" -d '{"query": "..."}'`
   - Evaluate: `curl -X POST http://127.0.0.1:8000/evaluate`
   - Health: `curl http://127.0.0.1:8000/health`
7. **(Optional) Run tests** to verify the stack
   ```bash
   pytest tests/test_query_analyzer.py tests/test_domain_expert.py tests/test_orchestrator.py tests/test_api.py
   ```

## Project Structure
```
src/
  agents/            BaseAgent + QueryAnalyzer/DomainExpert/Orchestrator + models
  ingestion/         PDFExtractor, PaperParser, HierarchicalChunker
  indexing/          ChromaDBStore, BM25Indexer
  retrieval/         HybridSearch orchestrator
  api/               FastAPI app entry point (dependency overrides for testing)
  llm/               Gemini client with retry + fallback config
scripts/
  ingest_papers.py   Pipeline entry for ingestion/index building
prompts/             LLM prompt templates per agent
.tests/              Unit + integration suites
```

## Configuration
`config.yaml` controls:
- Paths (`data_dir`, `chroma_db_path`, `bm25_index_path`).
- Retrieval weights (`semantic_weight`).
- Chunking parameters (`max_tokens`, `overlap`).
- LLM provider/model (`models/gemini-2.5-flash-lite` by default).

## Troubleshooting
- **422 from `/query`**: ensure the body is `{ "query": "..." }`.
- **Gemini errors**: confirm `GEMINI_API_KEY` and network access. The client retries automatically; persistent failures surface in the response.
- **Slow `/health`**: the first call runs three Gemini queries. Subsequent calls reuse cached metrics.
- **Chroma telemetry warnings**: informational only; they do not impact functionality.

## License
MIT (or insert license details if defined).






