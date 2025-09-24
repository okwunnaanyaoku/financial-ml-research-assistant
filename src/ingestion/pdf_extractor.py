import pymupdf
from typing import Dict

class PDFExtractor:
    def extract_from_pdf(self, pdf_path: str) -> Dict:
        doc = pymupdf.open(pdf_path)
        pages = []

        for page_num, page in enumerate(doc):
            pages.append({
                'page_num': page_num + 1,
                'text': page.get_text(),
                'blocks': page.get_text("blocks")
            })

        raw_text = '\n'.join([p['text'] for p in pages])
        metadata = self._extract_metadata(raw_text)

        return {
            'raw_text': raw_text,
            'pages': pages,
            'metadata': metadata
        }

    def _extract_metadata(self, text: str) -> Dict:
        import re

        title_match = re.search(r'^(.+?)[\n\r]', text[:500])
        title = title_match.group(1).strip() if title_match else 'Unknown'

        abstract_match = re.search(r'(?:Abstract|ABSTRACT)[\s:\n]+(.+?)(?:\n\n|Introduction)', text[:3000], re.IGNORECASE | re.DOTALL)
        abstract = abstract_match.group(1).strip() if abstract_match else ''

        year_match = re.search(r'(20[0-9]{2})', text[:1000])
        year = int(year_match.group(1)) if year_match else None

        return {'title': title, 'abstract': abstract, 'year': year}