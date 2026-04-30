"""绘图模块。"""
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_nav_curve(nav_df: pd.DataFrame):
    """生成净值曲线图对象。"""
    df = nav_df.sort_values("date")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["nav"], label="净值", color="#1f77b4")
    ax.set_title("最近1年基金净值曲线")
    ax.set_xlabel("日期")
    ax.set_ylabel("净值")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    return fig
