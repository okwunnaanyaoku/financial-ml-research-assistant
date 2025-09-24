import tiktoken
from typing import List, Dict

class HierarchicalChunker:
    def __init__(self, max_tokens=400, overlap=50):
        self.encoder = tiktoken.encoding_for_model("gpt-4")
        self.max_tokens = max_tokens
        self.overlap = overlap

    def chunk_paper(self, structure: Dict, metadata: Dict) -> List[Dict]:
        chunks = []
        chunk_id = 0

        for section in structure['sections']:
            content = '\n'.join(section['content'])
            if not content.strip():
                continue

            section_chunks = self._create_chunks(content, {
                'paper_title': metadata.get('title', 'Unknown'),
                'section': section['title'],
                'level': section.get('level', 1),
                'page_start': section.get('page_start', section.get('page', 1))
            })

            for chunk in section_chunks:
                chunk['chunk_id'] = f"chunk_{chunk_id}"
                chunks.append(chunk)
                chunk_id += 1

        return chunks

    def _create_chunks(self, text: str, metadata: Dict) -> List[Dict]:
        if not text.strip():
            return []

        sentences = self._split_sentences(text)
        chunks = []
        current_chunk = []
        current_tokens = 0

        for sentence in sentences:
            sentence_tokens = len(self.encoder.encode(sentence))

            if current_tokens + sentence_tokens > self.max_tokens and current_chunk:
                chunks.append({
                    'text': ' '.join(current_chunk),
                    'metadata': metadata.copy(),
                    'token_count': current_tokens
                })

                # Keep overlap
                if self.overlap > 0 and len(current_chunk) > 1:
                    current_chunk = current_chunk[-1:]
                    current_tokens = len(self.encoder.encode(current_chunk[-1]))
                else:
                    current_chunk = []
                    current_tokens = 0

            current_chunk.append(sentence)
            current_tokens += sentence_tokens

        if current_chunk:
            chunks.append({
                'text': ' '.join(current_chunk),
                'metadata': metadata.copy(),
                'token_count': current_tokens
            })

        return chunks

    def _split_sentences(self, text: str) -> List[str]:
        import re
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        return [s.strip() for s in sentences if s.strip()]