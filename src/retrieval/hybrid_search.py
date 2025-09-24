import json
from pathlib import Path
from typing import List, Dict
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from indexing.vector_store import ChromaDBStore
from indexing.bm25_indexer import BM25Indexer

class HybridSearch:
    def __init__(self, semantic_weight=0.7):
        self.semantic_weight = semantic_weight
        self.keyword_weight = 1 - semantic_weight
        self.vector_store = ChromaDBStore()
        self.bm25_indexer = BM25Indexer()
        self.chunks_cache = self._load_chunks()

    def _load_chunks(self) -> Dict[str, Dict]:
        chunks = {}
        for json_file in Path("data/processed_papers").glob("*.json"):
            with open(json_file, 'r') as f:
                data = json.load(f)
                for chunk in data['chunks']:
                    chunks[chunk['chunk_id']] = chunk
        return chunks

    def search(self, query: str, k: int = 10) -> List[Dict]:
        # Get semantic results
        semantic_results = self.vector_store.search(query, k=k*2)

        # Get keyword results
        keyword_chunk_ids = self.bm25_indexer.search(query, k=k*2)

        # Combine and score results
        combined_scores = {}

        # Add semantic scores
        for i, result in enumerate(semantic_results):
            chunk_id = result['metadata']['chunk_id']
            # Convert distance to similarity (lower distance = higher similarity)
            similarity = 1 - result['distance']
            combined_scores[chunk_id] = similarity * self.semantic_weight

        # Add keyword scores
        for i, chunk_id in enumerate(keyword_chunk_ids):
            # Rank-based scoring (higher rank = higher score)
            score = (len(keyword_chunk_ids) - i) / len(keyword_chunk_ids)
            if chunk_id in combined_scores:
                combined_scores[chunk_id] += score * self.keyword_weight
            else:
                combined_scores[chunk_id] = score * self.keyword_weight

        # Sort by combined score and return top k
        sorted_chunks = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:k]

        results = []
        for chunk_id, score in sorted_chunks:
            if chunk_id in self.chunks_cache:
                chunk = self.chunks_cache[chunk_id].copy()
                chunk['hybrid_score'] = score
                results.append(chunk)

        return results