import yaml
import os
from pathlib import Path
from typing import Dict, Any

class Config:
    _instance = None
    _config_data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load_config()
        return cls._instance

    @classmethod
    def _load_config(cls):
        config_path = Path(__file__).parent.parent / "config.yaml"
        with open(config_path, 'r') as f:
            cls._config_data = yaml.safe_load(f)

    @property
    def data_dir(self) -> str:
        return self._config_data['data_dir']

    @property
    def chroma_db_path(self) -> str:
        return self._config_data['chroma_db_path']

    @property
    def bm25_index_path(self) -> str:
        return self._config_data['bm25_index_path']

    @property
    def processed_papers_path(self) -> str:
        return self._config_data['processed_papers_path']

    @property
    def embedding_model_name(self) -> str:
        return self._config_data['embeddings']['model_name']

    @property
    def semantic_weight(self) -> float:
        return self._config_data['retrieval']['semantic_weight']

    @property
    def max_tokens(self) -> int:
        return self._config_data['chunking']['max_tokens']

    @property
    def overlap(self) -> int:
        return self._config_data['chunking']['overlap']

    @property
    def confidence_high(self) -> float:
        return self._config_data['confidence_thresholds']['high']

    @property
    def confidence_medium(self) -> float:
        return self._config_data['confidence_thresholds']['medium']

    @property
    def confidence_scaling(self) -> float:
        return self._config_data['confidence_thresholds']['scaling_factor']

    @property
    def eval_recall_weight(self) -> float:
        return self._config_data['evaluation_weights']['recall_weight']

    @property
    def eval_mrr_weight(self) -> float:
        return self._config_data['evaluation_weights']['mrr_weight']

    @property
    def eval_precision_weight(self) -> float:
        return self._config_data['evaluation_weights']['precision_weight']

    @property
    def eval_retrieval_weight(self) -> float:
        return self._config_data['evaluation_weights']['retrieval_vs_qa']

    @property
    def api_base_url(self) -> str:
        return self._config_data['api']['base_url']

    @property
    def collection_name(self) -> str:
        return self._config_data['api']['collection_name']

    @property
    def llm_provider(self) -> str:
        return self._config_data['llm']['provider']

    @property
    def llm_model(self) -> str:
        return self._config_data['llm']['model']

    @property
    def llm_api_key_env(self) -> str:
        return self._config_data['llm']['api_key_env']

    @property
    def llm_timeout(self) -> int:
        return self._config_data['llm']['timeout']

    @property
    def llm_temperature(self) -> float:
        return self._config_data['llm']['temperature']

config = Config()