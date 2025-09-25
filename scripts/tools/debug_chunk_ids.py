#!/usr/bin/env python3

"""Utilities for checking alignment between the golden evaluation set and the
processed paper chunks that feed retrieval.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import sys
sys.path.append(str(Path(__file__).parent / "src"))

from retrieval.hybrid_search import HybridSearch

GOLDEN_DATASET_PATH = Path("tests/evaluation/golden_dataset.json")
PROCESSED_PAPER_PATH = Path("data/processed_papers/On Technical Trading and Social Media Indicators in Cryptocurrencies Price Classification Through Deep Learning.json")


def load_golden_dataset() -> List[Dict]:
    with GOLDEN_DATASET_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_processed_chunks() -> List[Dict]:
    with PROCESSED_PAPER_PATH.open("r", encoding="utf-8") as f:
        paper_data = json.load(f)
    return paper_data.get("chunks", [])


def show_chunk_inventory(chunks: List[Dict], limit: int = 10) -> None:
    print(f"Total chunks available: {len(chunks)}")
    print(f"
First {limit} chunks (id, section, preview):")
    for chunk in chunks[:limit]:
        chunk_id = chunk.get("chunk_id")
        section = chunk.get("metadata", {}).get("section", "Unknown")
        preview = (chunk.get("text", "")[:80] + "...") if chunk.get("text") else ""
        print(f"  {chunk_id} | {section}")
        if preview:
            print(f"    {preview}")


def compare_ids(golden: List[Dict], chunks: List[Dict]) -> None:
    actual_ids = {chunk.get("chunk_id") for chunk in chunks}
    missing_ids = set()
    for item in golden:
        missing_ids.update(set(item.get("relevant_chunk_ids", [])) - actual_ids)

    if missing_ids:
        print("
??  Missing chunk IDs referenced by the golden set:")
        for chunk_id in sorted(missing_ids):
            print(f"  - {chunk_id}")
    else:
        print("
? All golden-set chunk IDs are present in the processed data.")


def sample_search(query: str, k: int = 5) -> None:
    search = HybridSearch()
    results = search.search(query, k=k)
    print(f"
Sample search for: '{query}' (top {k})")
    for idx, result in enumerate(results, start=1):
        chunk_id = result.get("chunk_id")
        section = result.get("metadata", {}).get("section", "Unknown")
        score = result.get("hybrid_score", 0.0)
        preview = result.get("text", "")[:60]
        print(f"  {idx}. {chunk_id} | {section} | score={score:.3f}")
        print(f"     {preview}...")


def show_question_alignment(golden: List[Dict], question_idx: int = 0) -> None:
    try:
        item = golden[question_idx]
    except IndexError:
        print(f"No question at index {question_idx}")
        return

    print(f"
Golden question {item['id']}:")
    print(f"  Question: {item['question']}")
    print(f"  Expected chunks: {item['relevant_chunk_ids']}")
    print(f"  Expected sections: {item.get('expected_sections', [])}")
    print(f"  Accepted answers: {item['golden_answer']}")


def main() -> None:
    golden = load_golden_dataset()
    chunks = load_processed_chunks()

    show_chunk_inventory(chunks)
    compare_ids(golden, chunks)
    show_question_alignment(golden, question_idx=0)
    sample_search("What neural networks were compared?", k=5)


if __name__ == "__main__":
    main()
