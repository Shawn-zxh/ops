"""Streamlit 基金分析工具入口。"""
from __future__ import annotations

import streamlit as st

from fund_analyzer.data_source import get_last_year_nav
from fund_analyzer.metrics import calculate_metrics
from fund_analyzer.visualization import plot_nav_curve


st.set_page_config(page_title="基金分析工具", layout="wide")
st.title("📈 基金分析工具")
st.caption("输入基金代码，自动抓取最近1年净值并计算关键指标")

fund_code = st.text_input("请输入基金代码", value="161725")

if st.button("开始分析"):
    if not fund_code.strip():
        st.warning("请先输入基金代码")
    else:
        try:
            with st.spinner("正在获取数据并计算..."):
                nav_df = get_last_year_nav(fund_code.strip())
                metrics = calculate_metrics(nav_df)
                fig = plot_nav_curve(nav_df)

            c1, c2, c3 = st.columns(3)
            c1.metric("年化收益率", f"{metrics['annual_return']:.2%}")
            c2.metric("最大回撤", f"{metrics['max_drawdown']:.2%}")
            c3.metric("年化波动率", f"{metrics['annual_volatility']:.2%}")

            st.subheader("净值曲线")
            st.pyplot(fig)

            st.subheader("原始净值数据")
            st.dataframe(nav_df, use_container_width=True)
        except Exception as e:
            st.error(f"分析失败：{e}")
