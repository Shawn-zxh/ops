"""数据获取模块：优先使用 akshare，失败时回退到 yfinance。"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

import pandas as pd


def _fetch_with_akshare(fund_code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """使用 akshare 获取基金净值历史数据。"""
    try:
        import akshare as ak

        df = ak.fund_open_fund_info_em(
            symbol=fund_code,
            indicator="单位净值走势",
        )
        if df is None or df.empty:
            return None

        # 兼容不同版本 akshare 的列名
        date_col = "净值日期" if "净值日期" in df.columns else "x"
        nav_col = "单位净值" if "单位净值" in df.columns else "y"

        out = df[[date_col, nav_col]].copy()
        out.columns = ["date", "nav"]
        out["date"] = pd.to_datetime(out["date"])
        out["nav"] = pd.to_numeric(out["nav"], errors="coerce")
        out = out.dropna().sort_values("date")

        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        out = out[(out["date"] >= start) & (out["date"] <= end)]
        return out.reset_index(drop=True)
    except Exception:
        return None


def _fetch_with_yfinance(fund_code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """使用 yfinance 获取历史收盘价并视作净值。"""
    try:
        import yfinance as yf

        ticker = yf.Ticker(fund_code)
        hist = ticker.history(start=start_date, end=end_date)
        if hist is None or hist.empty:
            return None

        out = hist[["Close"]].reset_index()
        out = out.rename(columns={"Date": "date", "Close": "nav"})
        out["date"] = pd.to_datetime(out["date"]).dt.tz_localize(None)
        out["nav"] = pd.to_numeric(out["nav"], errors="coerce")
        out = out.dropna().sort_values("date")
        return out.reset_index(drop=True)
    except Exception:
        return None


def get_last_year_nav(fund_code: str) -> pd.DataFrame:
    """获取最近 1 年净值数据。

    参数:
        fund_code: 基金代码（如 161725 或 ETF 代码）

    返回:
        DataFrame，包含 date/nav 两列
    """
    end = datetime.today().date()
    start = end - timedelta(days=365)

    start_date = start.strftime("%Y-%m-%d")
    end_date = end.strftime("%Y-%m-%d")

    df = _fetch_with_akshare(fund_code, start_date, end_date)
    if df is not None and not df.empty:
        return df

    df = _fetch_with_yfinance(fund_code, start_date, end_date)
    if df is not None and not df.empty:
        return df

    raise ValueError("无法获取数据，请检查基金代码或网络连接。")
