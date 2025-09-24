#!/usr/bin/env python3

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

from ingestion.pdf_extractor import PDFExtractor
from ingestion.paper_parser import PaperParser
from ingestion.chunker import HierarchicalChunker
import json

def test_chunker():
    extractor = PDFExtractor()
    parser = PaperParser()
    chunker = HierarchicalChunker()

    pdf_path = list(Path('data/raw_papers').glob('*.pdf'))[0]
    print(f"Testing chunker with: {pdf_path.name}")

    # Extract and parse
    extracted = extractor.extract_from_pdf(str(pdf_path))
    structure = parser.parse_structure(extracted['pages'])

    # Create chunks
    chunks = chunker.chunk_paper(structure, extracted['metadata'])

    print(f"\nCreated {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks[:5]):  # Show first 5
        print(f"  {i+1}. {chunk['chunk_id']} - {chunk['metadata']['section']} ({chunk['token_count']} tokens)")
        print(f"     Preview: {chunk['text'][:100]}...")

    # Stats
    total_tokens = sum(c['token_count'] for c in chunks)
    avg_tokens = total_tokens / len(chunks) if chunks else 0

    print(f"\nChunking stats:")
    print(f"  Total chunks: {len(chunks)}")
    print(f"  Total tokens: {total_tokens}")
    print(f"  Average tokens per chunk: {avg_tokens:.1f}")

    # Save sample
    with open('test_chunker_output.json', 'w') as f:
        json.dump({
            'total_chunks': len(chunks),
            'total_tokens': total_tokens,
            'sample_chunks': chunks[:3]
        }, f, indent=2)

    print(f"\nChunker output saved to test_chunker_output.json")
    print("✅ Chunker test passed")

if __name__ == "__main__":
    test_chunker()