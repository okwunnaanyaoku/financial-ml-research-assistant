#!/usr/bin/env python3

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

import pymupdf

def test_pdf_bookmarks():
    pdf_path = list(Path('data/raw_papers').glob('*.pdf'))[0]
    print(f"Testing bookmarks in: {pdf_path.name}")

    doc = pymupdf.open(str(pdf_path))

    # Check for PDF outline/bookmarks
    outline = doc.get_toc()
    print(f"\nBookmarks found: {len(outline)}")

    if outline:
        for level, title, page in outline:
            indent = "  " * (level - 1)
            print(f"{indent}Level {level}: {title} (Page {page})")
    else:
        print("No bookmarks found in this PDF")

    # Alternative: Check for font changes to detect headings
    print(f"\nAnalyzing font patterns for section detection...")

    font_analysis = {}
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")
        for block in blocks.get("blocks", []):
            if "lines" in block:
                for line in block["lines"]:
                    for span in line.get("spans", []):
                        font_info = f"{span.get('font', 'unknown')}_{span.get('size', 0):.1f}"
                        text = span.get("text", "").strip()

                        if text and len(text.split()) <= 10:  # Potential headings
                            if font_info not in font_analysis:
                                font_analysis[font_info] = []
                            font_analysis[font_info].append((page_num + 1, text))

    print("\nFont patterns (potential headings):")
    for font, texts in sorted(font_analysis.items()):
        if len(texts) < 20:  # Avoid common text fonts
            print(f"Font {font}: {len(texts)} instances")
            for page, text in texts[:3]:  # Show first 3 examples
                print(f"  Page {page}: {text[:50]}")

    doc.close()

if __name__ == "__main__":
    test_pdf_bookmarks()