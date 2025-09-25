#!/usr/bin/env python3

import sys
import json
from pathlib import Path
from typing import Dict, List
import time
import random

sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))
from config import config

from agents.orchestrator import Orchestrator
from agents.models import OrchestratorRequest
from retrieval.hybrid_search import HybridSearch
from ir_metrics import calculate_metrics, aggregate_metrics


class EvaluationRunner:
    def __init__(self):
        self.seed = 42
        random.seed(self.seed)

        self.orchestrator = Orchestrator()
        self.hybrid_search = HybridSearch()
        self.golden_dataset = self._load_dataset()
        self.cached_metrics = None

    def _load_dataset(self) -> List[Dict]:
        with open(Path(__file__).parent / "golden_dataset.json", 'r') as f:
            return json.load(f)

    def evaluate_retrieval(self) -> Dict[str, float]:
        all_metrics = []
        for item in self.golden_dataset:
            relevant_ids = set(item['relevant_chunk_ids'])
            results = self.hybrid_search.search(item['question'], k=10)
            retrieved_ids = [r['chunk_id'] for r in results]
            metrics = calculate_metrics(relevant_ids, retrieved_ids)
            all_metrics.append(metrics)
        return aggregate_metrics(all_metrics)

    def evaluate_qa_quality(self) -> Dict[str, float]:
        correct = 0
        times: List[float] = []
        for item in self.golden_dataset:
            start = time.time()
            result = self.orchestrator.process(OrchestratorRequest(query=item['question']))
            elapsed = time.time() - start
            times.append(elapsed)
            if self._answer_matches(result.content, item['golden_answer']):
                correct += 1

        count = len(self.golden_dataset) or 1
        factual_accuracy = correct / count
        avg_time = sum(times) / count if times else 0.0
        sorted_times = sorted(times)
        if sorted_times:
            index = max(0, int(len(sorted_times) * 0.95) - 1)
            p95 = sorted_times[index]
        else:
            p95 = 0.0

        return {
            'factual_accuracy': factual_accuracy,
            'avg_response_time': avg_time,
            'p95_response_time': p95,
            'correct_answers': correct,
        }

    def _answer_matches(self, response: str, golden_answers: List) -> bool:
        response_lower = response.lower()
        return any(str(answer).lower() in response_lower for answer in golden_answers)

    def run_full_evaluation(self) -> Dict:
        ir_metrics = self.evaluate_retrieval()
        qa_metrics = self.evaluate_qa_quality()
        return self._build_results(ir_metrics, qa_metrics)

    def _build_results(self, ir_metrics: Dict, qa_metrics: Dict) -> Dict:
        return {
            'dataset_size': len(self.golden_dataset),
            'seed': self.seed,
            'retrieval_metrics': ir_metrics,
            'qa_metrics': qa_metrics,
            'overall_score': self._overall_score(ir_metrics, qa_metrics),
        }

    def _overall_score(self, ir_metrics: Dict, qa_metrics: Dict) -> float:
        retrieval_score = (
            ir_metrics.get('recall_at_10', 0) * config.eval_recall_weight +
            ir_metrics.get('mrr', 0) * config.eval_mrr_weight +
            ir_metrics.get('precision_at_5', 0) * config.eval_precision_weight
        )
        qa_score = qa_metrics.get('factual_accuracy', 0)
        return round((retrieval_score * config.eval_retrieval_weight + qa_score * (1 - config.eval_retrieval_weight)) * 100, 2)

    def log_query(self, query: str, result):
        pass  # Minimal implementation for API compatibility

    def get_recent_metrics(self) -> Dict:
        if not self.cached_metrics:
            # Run quick evaluation on first 3 questions for performance
            original = self.golden_dataset
            self.golden_dataset = original[:3]
            self.cached_metrics = self.run_full_evaluation()
            self.golden_dataset = original

        return {
            'overall_score': self.cached_metrics.get('overall_score', 0),
            'recall_at_10': self.cached_metrics.get('retrieval_metrics', {}).get('recall_at_10', 0),
            'factual_accuracy': self.cached_metrics.get('qa_metrics', {}).get('factual_accuracy', 0),
            'avg_response_time': self.cached_metrics.get('qa_metrics', {}).get('avg_response_time', 0),
        }


def main():
    runner = EvaluationRunner()
    results = runner.run_full_evaluation()

    recall5 = results['retrieval_metrics'].get('recall_at_5', 0.0)
    factual = results['qa_metrics'].get('factual_accuracy', 0.0) * 100
    p95 = results['qa_metrics'].get('p95_response_time', 0.0)

    print(f"Seed: {results['seed']}")
    print(f"Recall@5: {recall5:.3f}")
    print(f"Factual match: {factual:.1f}%")
    print(f"P95 latency: {p95:.3f}s")

    print("-- Detailed Metrics --")
    print(f"Dataset: {results['dataset_size']} questions")
    print(f"Overall Score: {results['overall_score']}/100")
    print("Retrieval Metrics:")
    for metric, value in results['retrieval_metrics'].items():
        print(f"  {metric}: {value:.3f}")
    print("QA Metrics:")
    for metric, value in results['qa_metrics'].items():
        if isinstance(value, float):
            print(f"  {metric}: {value:.3f}")
        else:
            print(f"  {metric}: {value}")

    return results


if __name__ == "__main__":
    main()
