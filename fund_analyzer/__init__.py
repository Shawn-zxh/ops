"""Fund analyzer package."""

# Core modules expected to already exist in project
from . import data_source, metrics, visualization  # noqa: F401

# Newly added modules
from . import ai_report, portfolio, risk, scoring, strategy  # noqa: F401

__all__ = [
    "data_source",
    "metrics",
    "visualization",
    "portfolio",
    "scoring",
    "risk",
    "strategy",
    "ai_report",
]
