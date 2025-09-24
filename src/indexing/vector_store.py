import chromadb
from typing import List, Dict
import uuid

class ChromaDBStore:
    def __init__(self, path="data/chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name="financial_ml_papers",
            metadata={"hnsw:space": "cosine"}
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