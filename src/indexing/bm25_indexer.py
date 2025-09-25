from rank_bm25 import BM25Okapi
import pickle
from pathlib import Path
from typing import List, Dict
from config import config

class BM25Indexer:
    def __init__(self, index_path=None):
        self.index_path = Path(index_path or config.bm25_index_path)
        self.index_path.mkdir(parents=True, exist_ok=True)
        self.bm25 = None
        self.chunk_ids = []

    def build_index(self, chunks: List[Dict]):
        corpus = []
        self.chunk_ids = []

        for chunk in chunks:
            corpus.append(chunk['text'].lower().split())
            self.chunk_ids.append(chunk['chunk_id'])

        self.bm25 = BM25Okapi(corpus)
        self._save_index()

    def search(self, query: str, k: int = 10) -> List[str]:
        if not self.bm25:
            self._load_index()

        if not self.bm25:
            return []

        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        # Get top k indices
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [self.chunk_ids[i] for i in top_indices]

    def _save_index(self):
        with open(self.index_path / "bm25_index.pkl", "wb") as f:
            pickle.dump(self.bm25, f)
        with open(self.index_path / "chunk_ids.pkl", "wb") as f:
            pickle.dump(self.chunk_ids, f)

    def _load_index(self):
        bm25_path = self.index_path / "bm25_index.pkl"
        ids_path = self.index_path / "chunk_ids.pkl"

        if bm25_path.exists() and ids_path.exists():
            with open(bm25_path, "rb") as f:
                self.bm25 = pickle.load(f)
            with open(ids_path, "rb") as f:
                self.chunk_ids = pickle.load(f)