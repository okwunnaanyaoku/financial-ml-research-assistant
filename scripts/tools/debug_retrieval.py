#!/usr/bin/env python3

import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

from retrieval.hybrid_search import HybridSearch

def debug_retrieval():
    """Debug retrieval results vs golden dataset expectations"""

    # Load golden dataset
    with open('tests/evaluation/golden_dataset.json', 'r') as f:
        golden_dataset = json.load(f)

    search = HybridSearch()

    # Test first few questions
    for i, item in enumerate(golden_dataset[:3]):
        print(f"\n{'='*60}")
        print(f"Question {i+1}: {item['question']}")
        print(f"Expected chunks: {item['relevant_chunk_ids']}")
        print(f"{'='*60}")

        # Get search results
        results = search.search(item['question'], k=10)

        print(f"Retrieved chunks:")
        retrieved_ids = []
        for j, result in enumerate(results):
            chunk_id = result['chunk_id']
            retrieved_ids.append(chunk_id)
            in_golden = "✅" if chunk_id in item['relevant_chunk_ids'] else "❌"
            print(f"  {j+1}. {chunk_id} {in_golden} (score: {result['hybrid_score']:.3f})")
            print(f"     Section: {result['metadata']['section']}")
            print(f"     Preview: {result['text'][:80]}...")

        # Check overlap
        expected_set = set(item['relevant_chunk_ids'])
        retrieved_set = set(retrieved_ids)
        overlap = expected_set.intersection(retrieved_set)

        print(f"\nAnalysis:")
        print(f"  Expected: {len(expected_set)} chunks")
        print(f"  Retrieved: {len(retrieved_set)} chunks")
        print(f"  Overlap: {len(overlap)} chunks - {list(overlap)}")
        print(f"  Recall@10: {len(overlap) / len(expected_set):.3f}")

if __name__ == "__main__":
    debug_retrieval()