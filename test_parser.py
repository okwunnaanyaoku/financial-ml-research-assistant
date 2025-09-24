#!/usr/bin/env python3

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

from ingestion.pdf_extractor import PDFExtractor
from ingestion.paper_parser import PaperParser
import json

def test_parser():
    extractor = PDFExtractor()
    parser = PaperParser()

    pdf_path = list(Path('data/raw_papers').glob('*.pdf'))[0]
    print(f"Testing parser with: {pdf_path.name}")

    # Extract PDF
    extracted = extractor.extract_from_pdf(str(pdf_path))

    # Parse structure using PDF path directly
    structure = parser.parse_structure(str(pdf_path))

    print(f"\nFound {len(structure['sections'])} sections:")
    for i, section in enumerate(structure['sections'][:10]):  # Show first 10
        content_preview = ' '.join(section['content'][:3])[:100]
        print(f"  {i+1}. Level {section['level']}: {section['title']} (Page {section['page_start']}) - {content_preview}...")

    # Save results
    with open('test_parser_output.json', 'w') as f:
        json.dump({
            'total_sections': len(structure['sections']),
            'sections_preview': [{
                'level': s['level'],
                'title': s['title'],
                'page_start': s['page_start'],
                'content_lines': len(s['content'])
            } for s in structure['sections'][:5]]
        }, f, indent=2)

    print(f"\nParser output saved to test_parser_output.json")
    print("✅ Paper parser test passed")

if __name__ == "__main__":
    test_parser()