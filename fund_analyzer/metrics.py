"""指标计算模块。"""
from __future__ import annotations

import numpy as np
import pandas as pd


TRADING_DAYS = 252


def calculate_metrics(nav_df: pd.DataFrame) -> dict:
    """根据净值序列计算年化收益率、最大回撤、波动率。"""
    df = nav_df.copy().sort_values("date")
    if len(df) < 2:
        raise ValueError("数据点不足，无法计算指标。")

    nav = df["nav"].astype(float)
    returns = nav.pct_change().dropna()

    # 年化收益率：按区间总收益折算到 1 年
    total_return = nav.iloc[-1] / nav.iloc[0] - 1
    days = max((df["date"].iloc[-1] - df["date"].iloc[0]).days, 1)
    annual_return = (1 + total_return) ** (365 / days) - 1

    # 最大回撤
    running_max = nav.cummax()
    drawdown = nav / running_max - 1
    max_drawdown = drawdown.min()

    # 年化波动率
    annual_volatility = returns.std() * np.sqrt(TRADING_DAYS)

    return {
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
        "annual_volatility": annual_volatility,
    }
