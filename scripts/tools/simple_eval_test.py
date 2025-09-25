#!/usr/bin/env python3

import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'src'))
sys.path.append(str(Path(__file__).parent / 'tests/evaluation'))

from ir_metrics import calculate_metrics

def test_metrics():
    relevant = {"chunk_0", "chunk_2", "chunk_3", "chunk_58"}
    retrieved = ["chunk_0", "chunk_15", "chunk_1", "chunk_32", "chunk_58", "chunk_3"]
    metrics = calculate_metrics(relevant, retrieved)
    expected_recall = 3 / 4  # 3 chunks found out of 4 relevant
    return abs(metrics['recall_at_10'] - expected_recall) < 0.1

def test_dataset():
    try:
        with open('tests/evaluation/golden_dataset.json', 'r') as f:
            dataset = json.load(f)
        return len(dataset) > 0
    except:
        return False

def test_evaluation():
    tests = [
        ("IR Metrics", test_metrics()),
        ("Golden Dataset", test_dataset())
    ]

    results = [f"{'PASS' if result else 'FAIL'}: {name}" for name, result in tests]
    overall = all(result for _, result in tests)

    print("\n".join(results))
    print(f"Overall: {'OPERATIONAL' if overall else 'NEEDS FIXES'}")
    return overall

if __name__ == "__main__":
    test_evaluation()