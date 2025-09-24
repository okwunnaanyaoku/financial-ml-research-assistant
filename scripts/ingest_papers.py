#!/usr/bin/env python3

import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from ingestion.pdf_extractor import PDFExtractor
from ingestion.paper_parser import PaperParser
from ingestion.chunker import HierarchicalChunker

def ingest_papers(papers_dir="data/raw_papers"):
    extractor = PDFExtractor()
    parser = PaperParser()
    chunker = HierarchicalChunker()

    papers_path = Path(papers_dir)
    pdf_files = list(papers_path.glob('*.pdf'))

    if not pdf_files:
        print(f"No PDF files found in {papers_dir}")
        return

    all_chunks = []
    stats = {'papers_processed': 0, 'total_chunks': 0}

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")

        try:
            # Extract PDF
            extracted = extractor.extract_from_pdf(str(pdf_path))

            # Parse structure using PDF path directly
            structure = parser.parse_structure(str(pdf_path))

            # Create chunks
            chunks = chunker.chunk_paper(structure, extracted['metadata'])

            # Save processed paper
            output_path = Path("data/processed_papers") / f"{pdf_path.stem}.json"
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w') as f:
                json.dump({
                    'metadata': extracted['metadata'],
                    'chunks': chunks,
                    'stats': {'num_chunks': len(chunks)}
                }, f, indent=2)

            all_chunks.extend(chunks)
            stats['papers_processed'] += 1
            stats['total_chunks'] += len(chunks)

            print(f"  ✅ {len(chunks)} chunks created")

        except Exception as e:
            print(f"  ❌ Error: {e}")

    print(f"\nIngestion complete:")
    print(f"  Papers: {stats['papers_processed']}")
    print(f"  Total chunks: {stats['total_chunks']}")

    # Save stats
    with open('ingestion_stats.json', 'w') as f:
        json.dump(stats, f, indent=2)

    return stats

if __name__ == "__main__":
    ingest_papers()