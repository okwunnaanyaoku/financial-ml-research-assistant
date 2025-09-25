import pytest

from ingestion.chunker import HierarchicalChunker


def test_chunker_emits_section_scoped_chunks():
    structure = {
        "sections": [
            {
                "title": "Introduction",
                "content": [
                    "Alpha models outperform competitors.",
                    "Beta results show incremental gains."
                ],
                "level": 1,
                "page_start": 1,
            },
            {
                "title": "Results",
                "content": [
                    "Sharpe ratio improves with better risk controls.",
                ],
                "level": 1,
                "page_start": 2,
            },
        ]
    }
    metadata = {"title": "Sample Report"}

    chunker = HierarchicalChunker(max_tokens=120, overlap=0)
    chunks = chunker.chunk_paper(structure, metadata)

    assert len(chunks) == 2, "Each section should yield one chunk with generous token limit"
    assert chunks[0]["chunk_id"] == "chunk_0"
    assert chunks[0]["metadata"]["section"] == "Introduction"
    assert "Introduction" not in chunks[1]["text"]
    assert chunks[1]["metadata"]["section"] == "Results"
