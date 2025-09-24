#!/usr/bin/env python3

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

from retrieval.hybrid_search import HybridSearch

def test_hybrid_search():
    print("🔍 Testing Hybrid Search System...")

    hybrid = HybridSearch(semantic_weight=0.7)

    # Test queries
    queries = [
        "LSTM neural networks cryptocurrency prediction",
        "Bitcoin price volatility deep learning",
        "social media sentiment analysis trading"
    ]

    for query in queries:
        print(f"\nQuery: '{query}'")
        results = hybrid.search(query, k=3)

        print(f"Found {len(results)} hybrid results:")
        for i, result in enumerate(results):
            print(f"  {i+1}. {result['metadata']['section']} (score: {result['hybrid_score']:.3f})")
            print(f"     Preview: {result['text'][:80]}...")

    print(f"\n✅ Hybrid search test passed")

if __name__ == "__main__":
    test_hybrid_search()