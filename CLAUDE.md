# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Multi-Agent Financial ML Research Assistant that answers complex questions about machine learning applications in finance using advanced retrieval techniques. The system orchestrates multiple specialized agents to provide comprehensive, well-cited responses from a curated database of financial ML research papers.

## Architecture

The system follows a multi-agent architecture with these core components:

- **Query Analyzer Agent**: Classifies questions, identifies complexity, breaks down multi-part queries
- **Retrieval Agent**: Implements hybrid retrieval (dense + sparse) with hierarchical document understanding
- **Domain Expert Agent**: Provides financial ML expertise, methodology analysis, and cross-paper insights
- **Orchestrator Agent**: Coordinates workflow, manages agent communication, ensures response quality

## Directory Structure

```
financial-ml-research-assistant/
├── src/
│   ├── ingestion/          # PDF extraction and paper parsing
│   ├── preprocessing/      # Text cleaning and section detection
│   ├── indexing/          # Embeddings and vector store operations
│   ├── agents/            # Multi-agent system components
│   ├── retrieval/         # Hybrid search and context building
│   ├── utils/             # Prompt loading and utilities
│   └── config.py          # Configuration management
├── data/
│   ├── raw_papers/        # PDF research papers
│   ├── processed_papers/  # JSON files with processed chunks
│   ├── chroma_db/         # Vector database
│   └── bm25_index/        # BM25 index files
├── prompts/               # LLM prompts organized by agent
├── scripts/               # Pipeline execution scripts
├── tests/
├── notebooks/
└── requirements.txt
```

## Development Commands

### Setup and Dependencies
```bash
# Install dependencies
pip install -r requirements.txt

# Install spaCy model for entity extraction
python -m spacy download en_core_web_sm
```

### Data Ingestion Pipeline
```bash
# Ingest PDF papers into the system
python scripts/ingest_papers.py --papers_dir data/raw_papers

# Build search indices
python scripts/build_index.py

# Run system evaluation
python scripts/evaluate_system.py
```

### Configuration
The system uses `config.yaml` for configuration management, including:
- Model settings (embeddings, LLM parameters)
- Chunking parameters
- Retrieval settings
- Agent configurations
- Evaluation metrics

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run specific test modules
python -m pytest tests/test_ingestion.py
python -m pytest tests/test_agents.py
```

## Key Technical Concepts

### Hierarchical Document Processing
The system implements sophisticated document chunking that:
- Preserves paper structure (sections, subsections, paragraphs)
- Uses different chunking strategies per section type
- Maintains hierarchical relationships between chunks
- Extracts financial ML specific metadata

### Hybrid Retrieval System
- **Semantic Search**: Uses SentenceTransformers for dense retrieval
- **Keyword Search**: BM25 indexing for sparse retrieval
- **Reranking**: Cross-encoder models for improved relevance
- **Context Expansion**: Intelligently includes parent/child sections

### Prompt Management
All agent prompts are stored as text files in the `prompts/` directory, organized by agent type. The `PromptLoader` utility handles template loading and variable substitution.

### Financial ML Entity Extraction
The system identifies and extracts:
- ML models (LSTM, transformer, random forest, etc.)
- Financial metrics (Sharpe ratio, VaR, maximum drawdown, etc.)
- Datasets (NYSE, NASDAQ, high-frequency data, etc.)
- Methodologies (time series analysis, portfolio optimization, etc.)

## Implementation Notes

### PDF Processing
- Primary extraction using PyMuPDF with pdfplumber fallback
- Handles academic paper structure (equations, tables, references)
- Preserves font information for section detection

### Multi-Agent Coordination
- Agents communicate through structured message passing
- Query decomposition for complex multi-part questions
- Response validation and quality assurance

### Vector Database
- ChromaDB for storing document embeddings
- Metadata filtering capabilities
- Efficient similarity search with relevance scoring

### Performance Considerations
- Batch processing for embedding generation
- Caching mechanisms for repeated queries
- Configurable chunk sizes and overlap strategies

## Development Workflow

1. **Adding New Papers**: Place PDFs in `data/raw_papers/` and run ingestion pipeline
2. **Modifying Agents**: Update prompt templates in `prompts/` directory
3. **Configuration Changes**: Modify `config.yaml` for system parameters
4. **Testing Changes**: Run evaluation scripts to measure impact

## Dependencies

Key Python packages:
- `sentence-transformers`: For semantic embeddings
- `chromadb`: Vector database
- `pymupdf`: PDF text extraction
- `spacy`: Named entity recognition
- `rank-bm25`: Keyword search indexing
- `tqdm`: Progress bars for long-running operations

The system is designed to be modular and extensible, allowing for easy addition of new agents, retrieval strategies, or document types.

## Code Standards & Context Guidelines

### Minimal Code Requirements
- **Essential functionality only** - no fluff, no over-engineering
- **Maximum 50 lines per function** - break down larger functions
- **Single responsibility** - one function, one purpose
- **No duplicate logic** - DRY principle strictly enforced
- **Essential imports only** - remove unused dependencies
- **Clear variable names** - self-documenting code
- **No comments unless absolutely necessary** - code should be self-explanatory

### Context Referencing
- **Always reference CLAUDE.md** for project context before implementing
- **Check implementation tracker** in `.claude/` for current progress
- **Follow existing patterns** established in the codebase
- **Maintain architectural consistency** with multi-agent design
- **Use established directory structure** - don't create unnecessary files

### Code Review Process
- **Use `/review-code` command** after each implementation
- **Validate minimalism** - remove any bloat immediately
- **Check for duplicates** across modules
- **Ensure real functionality** - no mocks or placeholders
- **Verify clean interfaces** between components

### Implementation Tracking
- **Update todos actively** in `.claude/implementation-tracker.md`
- **Mark progress immediately** after completing tasks
- **Document real functionality** with actual results
- **Track testing with real data** - PDF papers, embeddings, queries