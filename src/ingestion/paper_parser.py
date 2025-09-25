try:
    import fitz
except ImportError:
    import pymupdf as fitz
from typing import List, Dict

class PaperParser:
    def parse_structure(self, pdf_path: str) -> Dict:
        doc = fitz.open(pdf_path)
        outline = doc.get_toc()

        if not outline:
            return self._fallback_parse(doc)

        sections = []
        for level, title, page_num in outline:
            if level <= 2:  # Only main sections and subsections
                sections.append({
                    'level': level,
                    'title': title.strip(),
                    'page_start': page_num,
                    'content': []
                })

        # Extract content for each section
        for i, section in enumerate(sections):
            start_page = section['page_start'] - 1  # 0-indexed
            end_page = sections[i + 1]['page_start'] - 1 if i + 1 < len(sections) else len(doc)

            content_text = ""
            for page_idx in range(start_page, min(end_page, len(doc))):
                page = doc[page_idx]
                content_text += page.get_text()

            # Clean content (remove section title if it appears)
            lines = content_text.split('\n')
            cleaned_lines = [line for line in lines if line.strip() and section['title'] not in line]
            section['content'] = cleaned_lines

        doc.close()
        return {'sections': sections}

    def _fallback_parse(self, doc) -> Dict:
        # Fallback for PDFs without bookmarks
        sections = [{
            'level': 1,
            'title': 'Full Document',
            'page_start': 1,
            'content': []
        }]

        for page in doc:
            sections[0]['content'].extend(page.get_text().split('\n'))

        return {'sections': sections}