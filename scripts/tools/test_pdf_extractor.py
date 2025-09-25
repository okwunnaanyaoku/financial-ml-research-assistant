#!/usr/bin/env python3

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

from ingestion.pdf_extractor import PDFExtractor
import json

def test_pdf_extraction():
    extractor = PDFExtractor()

    # Test with any PDF in raw_papers directory
    papers_dir = Path('data/raw_papers')
    pdf_files = list(papers_dir.glob('*.pdf'))

    if not pdf_files:
        print("No PDF files found in data/raw_papers/")
        print("Please add some financial ML research papers to test with")
        return

    pdf_path = pdf_files[0]
    print(f"Testing with: {pdf_path.name}")

    try:
        result = extractor.extract_from_pdf(str(pdf_path))

        # Print results
        print(f"\nExtracted metadata:")
        print(f"Title: {result['metadata']['title']}")
        print(f"Year: {result['metadata']['year']}")
        print(f"Abstract length: {len(result['metadata']['abstract'])} chars")
        print(f"Total pages: {len(result['pages'])}")
        print(f"Total text length: {len(result['raw_text'])} chars")

        # Save sample output
        sample_output = {
            'metadata': result['metadata'],
            'page_count': len(result['pages']),
            'text_preview': result['raw_text'][:500] + '...'
        }

        with open('test_output.json', 'w') as f:
            json.dump(sample_output, f, indent=2)

        print(f"\nSample output saved to test_output.json")
        print("✅ PDF extraction test passed")

    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_pdf_extraction()