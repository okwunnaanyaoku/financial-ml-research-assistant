from typing import List, Dict, Set
import statistics

def recall_at_k(relevant_ids: Set[str], retrieved_ids: List[str], k: int) -> float:
    if not relevant_ids:
        return 0.0
    retrieved_k = set(retrieved_ids[:k])
    return len(relevant_ids.intersection(retrieved_k)) / len(relevant_ids)

def precision_at_k(relevant_ids: Set[str], retrieved_ids: List[str], k: int) -> float:
    if k == 0 or not retrieved_ids:
        return 0.0
    retrieved_k = set(retrieved_ids[:k])
    found = len(relevant_ids.intersection(retrieved_k))
    return found / min(k, len(retrieved_ids))

def reciprocal_rank(relevant_ids: Set[str], retrieved_ids: List[str]) -> float:
    for i, chunk_id in enumerate(retrieved_ids, 1):
        if chunk_id in relevant_ids:
            return 1.0 / i
    return 0.0

def average_precision(relevant_ids: Set[str], retrieved_ids: List[str]) -> float:
    if not relevant_ids:
        return 0.0
    precisions = []
    relevant_found = 0
    for i, chunk_id in enumerate(retrieved_ids, 1):
        if chunk_id in relevant_ids:
            relevant_found += 1
            precisions.append(relevant_found / i)
    return sum(precisions) / len(relevant_ids) if precisions else 0.0

def calculate_metrics(relevant_ids: Set[str], retrieved_ids: List[str]) -> Dict[str, float]:
    return {
        'recall_at_5': recall_at_k(relevant_ids, retrieved_ids, 5),
        'recall_at_10': recall_at_k(relevant_ids, retrieved_ids, 10),
        'precision_at_5': precision_at_k(relevant_ids, retrieved_ids, 5),
        'precision_at_10': precision_at_k(relevant_ids, retrieved_ids, 10),
        'reciprocal_rank': reciprocal_rank(relevant_ids, retrieved_ids),
        'average_precision': average_precision(relevant_ids, retrieved_ids)
    }

def aggregate_metrics(all_metrics: List[Dict[str, float]]) -> Dict[str, float]:
    if not all_metrics:
        return {}
    aggregated = {}
    for metric_name in all_metrics[0].keys():
        values = [m[metric_name] for m in all_metrics]
        if metric_name == 'reciprocal_rank':
            aggregated['mrr'] = statistics.mean(values)
        elif metric_name == 'average_precision':
            aggregated['map'] = statistics.mean(values)
        else:
            aggregated[metric_name] = statistics.mean(values)
    return aggregated