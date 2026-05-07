from __future__ import annotations


def score_fund(metrics: dict[str, float]) -> float:
    """综合打分：收益越高越好，回撤/波动越低越好，夏普越高越好。"""
    annual_return = metrics.get("annual_return", 0.0)
    max_drawdown = metrics.get("max_drawdown", 0.0)
    volatility = metrics.get("volatility", 0.0)
    sharpe = metrics.get("sharpe", 0.0)

    # 简单线性打分，权重可按策略调整
    return (
        annual_return * 100.0 * 0.40
        + sharpe * 0.30
        - abs(max_drawdown) * 100.0 * 0.20
        - volatility * 100.0 * 0.10
    )
