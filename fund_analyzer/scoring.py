"""基金评分模块。"""

from __future__ import annotations

from typing import Any, Dict


class FundScorer:
    """基金评分器。"""

    def score(self, fund_data: Dict[str, Any]) -> float:
        """返回基金评分（空实现占位）。"""
        _ = fund_data
        return 0.0
