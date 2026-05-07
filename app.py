"""基金评分展示应用。"""

from __future__ import annotations

from typing import Dict, List

import pandas as pd
import streamlit as st

from scoring import rank_funds


st.set_page_config(page_title="基金评分系统", layout="wide")
st.title("基金评分系统")

# 示例数据（可替换成数据库/接口数据）
funds: List[Dict[str, float]] = [
    {"name": "基金A", "return_rate": 0.22, "max_drawdown": 0.10, "volatility": 0.16, "sharpe": 1.45},
    {"name": "基金B", "return_rate": 0.18, "max_drawdown": 0.08, "volatility": 0.12, "sharpe": 1.30},
    {"name": "基金C", "return_rate": 0.26, "max_drawdown": 0.14, "volatility": 0.20, "sharpe": 1.60},
    {"name": "基金D", "return_rate": 0.15, "max_drawdown": 0.06, "volatility": 0.10, "sharpe": 1.10},
]

ranked_funds = rank_funds(funds)

st.subheader("基金排名")
ranking_df = pd.DataFrame(ranked_funds)[
    ["rank", "name", "score", "return_rate", "max_drawdown", "volatility", "sharpe"]
].rename(
    columns={
        "rank": "排名",
        "name": "基金",
        "score": "得分",
        "return_rate": "收益率",
        "max_drawdown": "最大回撤",
        "volatility": "波动率",
        "sharpe": "夏普比率",
    }
)

st.dataframe(ranking_df, use_container_width=True, hide_index=True)
