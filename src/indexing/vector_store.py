import chromadb
from typing import List, Dict
import uuid
from config import config

class ChromaDBStore:
    def __init__(self, path=None, collection_name=None):
        self.client = chromadb.PersistentClient(path=path or config.chroma_db_path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name or "financial_ml_papers",
            metadata={"hnsw:space": "cosine"}
        )


    def clear(self) -> None:
        """Remove all entries from the collection."""
        try:
            self.client.delete_collection(self.collection.name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata=self.collection.metadata or {"hnsw:space": "cosine"}
        )

    def add_chunks(self, chunks: List[Dict]):
        documents = []
        metadatas = []
        ids = []

        for chunk in chunks:
            documents.append(chunk['text'])
            metadatas.append({
                'chunk_id': chunk['chunk_id'],
                'paper_title': chunk['metadata']['paper_title'],
                'section': chunk['metadata']['section'],
                'page_start': chunk['metadata'].get('page_start', 1)
            })
            ids.append(str(uuid.uuid4()))

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query: str, k: int = 10) -> List[Dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )

        chunks = []
        for i in range(len(results['ids'][0])):
            chunks.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })

        return chunks

    def get_stats(self) -> Dict:
        return {
            'total_chunks': self.collection.count(),
            'collection_name': self.collection.name
        }