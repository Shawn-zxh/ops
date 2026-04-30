"""风险评级模块。"""

from __future__ import annotations

from typing import Any, Dict


class RiskRater:
    """风险评级器。"""

    def rate(self, fund_data: Dict[str, Any]) -> str:
        """返回风险评级（空实现占位）。"""
        _ = fund_data
        return "UNRATED"
