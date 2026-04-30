"""基金评分模块。"""

from __future__ import annotations

from typing import Dict, Iterable, List


def _clamp(value: float, min_value: float = 0.0, max_value: float = 100.0) -> float:
    return max(min_value, min(max_value, value))


def score_fund(return_rate: float, max_drawdown: float, volatility: float, sharpe: float) -> float:
    """根据四项指标计算基金总分（0-100）。

    权重：
    - 收益率 30%
    - 最大回撤 30%（越小越好）
    - 波动率 20%（越小越好）
    - 夏普比率 20%

    评分标准（线性映射，超界后截断）：
    - 收益率：0% -> 0分，30% -> 100分
    - 最大回撤：50% -> 0分，0% -> 100分
    - 波动率：50% -> 0分，0% -> 100分
    - 夏普比率：0 -> 0分，3 -> 100分
    """

    return_score = _clamp((return_rate / 0.30) * 100)
    drawdown_score = _clamp((1 - (max_drawdown / 0.50)) * 100)
    volatility_score = _clamp((1 - (volatility / 0.50)) * 100)
    sharpe_score = _clamp((sharpe / 3.0) * 100)

    total = (
        return_score * 0.30
        + drawdown_score * 0.30
        + volatility_score * 0.20
        + sharpe_score * 0.20
    )
    return round(total, 2)


def rank_funds(funds: Iterable[Dict[str, float]]) -> List[Dict[str, float]]:
    """对多个基金进行评分并按得分从高到低排序。"""

    ranked: List[Dict[str, float]] = []
    for fund in funds:
        score = score_fund(
            return_rate=fund["return_rate"],
            max_drawdown=fund["max_drawdown"],
            volatility=fund["volatility"],
            sharpe=fund["sharpe"],
        )
        ranked.append({**fund, "score": score})

    ranked.sort(key=lambda x: x["score"], reverse=True)
    for idx, fund in enumerate(ranked, start=1):
        fund["rank"] = idx
    return ranked
