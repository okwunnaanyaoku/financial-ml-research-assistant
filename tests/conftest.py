import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents.models import Entities, QueryAnalyzerMetadata


@pytest.fixture()
def sample_query_metadata() -> QueryAnalyzerMetadata:
    return QueryAnalyzerMetadata(
        complexity="moderate",
        entities=Entities(models=["lstm"], metrics=["sharpe"], concepts=["trading"]),
        query_type="factual",
        financial_focus="trading",
    )
