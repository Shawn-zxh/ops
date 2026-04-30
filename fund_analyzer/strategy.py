"""定投回测模块。"""

from __future__ import annotations

from typing import Any, Dict, List


class DCAEstimator:
    """定投策略回测器。"""

    def backtest(self, price_series: List[float], config: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """回测定投策略（空实现占位）。"""
        _ = (price_series, config)
        return {"status": "not_implemented"}
