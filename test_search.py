#!/usr/bin/env python3

import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

from indexing.vector_store import ChromaDBStore
from indexing.bm25_indexer import BM25Indexer

def test_search_infrastructure():
    # Load processed chunks
    processed_file = Path("data/processed_papers").glob("*.json")
    processed_file = list(processed_file)[0]

    with open(processed_file, 'r') as f:
        data = json.load(f)

    chunks = data['chunks']
    print(f"Testing with {len(chunks)} chunks from {processed_file.name}")

    # Test ChromaDB
    print("\n🔍 Testing ChromaDB semantic search...")
    vector_store = ChromaDBStore()
    vector_store.add_chunks(chunks)

    semantic_results = vector_store.search("LSTM neural networks cryptocurrency", k=3)
    print(f"Found {len(semantic_results)} semantic results:")
    for i, result in enumerate(semantic_results):
        print(f"  {i+1}. {result['metadata']['section']} (distance: {result['distance']:.3f})")
        print(f"     Preview: {result['text'][:80]}...")

    # Test BM25
    print("\n🔍 Testing BM25 keyword search...")
    bm25_indexer = BM25Indexer()
    bm25_indexer.build_index(chunks)

    keyword_results = bm25_indexer.search("LSTM neural networks cryptocurrency", k=3)
    print(f"Found {len(keyword_results)} keyword results:")
    for i, chunk_id in enumerate(keyword_results):
        chunk = next(c for c in chunks if c['chunk_id'] == chunk_id)
        print(f"  {i+1}. {chunk['metadata']['section']} ({chunk_id})")
        print(f"     Preview: {chunk['text'][:80]}...")

    print(f"\n✅ Search infrastructure test passed")
    print(f"   ChromaDB: {vector_store.get_stats()['total_chunks']} chunks indexed")
    print(f"   BM25: {len(bm25_indexer.chunk_ids)} chunks indexed")

if __name__ == "__main__":
    test_search_infrastructure()