from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable

import numpy as np
import pandas as pd

from scoring import score_fund


TRADING_DAYS = 252


@dataclass
class FundMeta:
    code: str
    name: str
    risk_level: str


def fetch_fund_list(limit: int = 50) -> pd.DataFrame:
    """
    从 akshare 获取基金列表；若不可用则返回模拟列表。
    """
    try:
        import akshare as ak  # type: ignore

        df = ak.fund_name_em()
        if df.empty:
            raise ValueError("akshare 返回空基金列表")

        # 兼容常见列名
        code_col = "基金代码" if "基金代码" in df.columns else "基金代码"
        name_col = "基金简称" if "基金简称" in df.columns else "基金简称"

        out = df[[code_col, name_col]].copy().head(limit)
        out.columns = ["code", "name"]
    except Exception:
        # 模拟列表，保障一键运行
        out = pd.DataFrame(
            {
                "code": [f"MOCK{i:04d}" for i in range(1, limit + 1)],
                "name": [f"模拟基金{i:04d}" for i in range(1, limit + 1)],
            }
        )

    # 随机分配风险等级，示例用途
    risk_levels = ["低", "中", "高"]
    out["risk_level"] = [risk_levels[i % 3] for i in range(len(out))]
    return out


def fetch_price_series(fund_code: str, days: int = TRADING_DAYS) -> pd.Series:
    """
    获取单只基金净值序列；若不可用则模拟价格序列。
    """
    try:
        import akshare as ak  # type: ignore

        end = datetime.now().date()
        start = end - timedelta(days=int(days * 1.8))
        hist = ak.fund_open_fund_info_em(
            symbol=fund_code,
            indicator="单位净值走势",
        )

        if hist is None or hist.empty:
            raise ValueError(f"未获取到 {fund_code} 历史净值")

        date_col = "净值日期"
        value_col = "单位净值"
        if date_col not in hist.columns or value_col not in hist.columns:
            raise ValueError(f"{fund_code} 历史净值列结构不匹配")

        ser = (
            hist[[date_col, value_col]]
            .assign(**{date_col: lambda x: pd.to_datetime(x[date_col])})
            .sort_values(date_col)
            .set_index(date_col)[value_col]
            .astype(float)
            .dropna()
        )
        ser = ser[ser.index >= pd.Timestamp(start)]
        if len(ser) < 30:
            raise ValueError(f"{fund_code} 可用净值点过少")
        return ser
    except Exception:
        rng = np.random.default_rng(abs(hash(fund_code)) % (2**32))
        drift = rng.uniform(0.03, 0.25) / TRADING_DAYS
        vol = rng.uniform(0.08, 0.35) / np.sqrt(TRADING_DAYS)
        rets = rng.normal(drift, vol, size=days)
        prices = 1.0 * np.cumprod(1 + rets)
        idx = pd.date_range(end=pd.Timestamp.today().normalize(), periods=days, freq="B")
        return pd.Series(prices, index=idx, name=fund_code)


def calculate_metrics(nav: pd.Series, risk_free_rate: float = 0.02) -> dict[str, float]:
    returns = nav.pct_change().dropna()
    if returns.empty:
        return {"annual_return": 0.0, "max_drawdown": 0.0, "volatility": 0.0, "sharpe": 0.0}

    total_return = nav.iloc[-1] / nav.iloc[0] - 1
    years = max(len(returns) / TRADING_DAYS, 1 / TRADING_DAYS)
    annual_return = (1 + total_return) ** (1 / years) - 1

    cummax = nav.cummax()
    drawdown = nav / cummax - 1
    max_drawdown = drawdown.min()

    volatility = returns.std() * np.sqrt(TRADING_DAYS)
    sharpe = (annual_return - risk_free_rate) / volatility if volatility > 1e-12 else 0.0

    return {
        "annual_return": float(annual_return),
        "max_drawdown": float(max_drawdown),
        "volatility": float(volatility),
        "sharpe": float(sharpe),
    }


def filter_funds(
    df: pd.DataFrame,
    risk_levels: Iterable[str] | None = None,
    min_return: float | None = None,
    max_return: float | None = None,
) -> pd.DataFrame:
    out = df.copy()
    if risk_levels:
        out = out[out["risk_level"].isin(set(risk_levels))]
    if min_return is not None:
        out = out[out["annual_return"] >= min_return]
    if max_return is not None:
        out = out[out["annual_return"] <= max_return]
    return out


def run(limit: int, top_n: int, risk_levels: list[str], min_return: float | None, max_return: float | None) -> pd.DataFrame:
    fund_df = fetch_fund_list(limit=limit)
    records: list[dict[str, float | str]] = []

    for _, row in fund_df.iterrows():
        code = str(row["code"])
        name = str(row["name"])
        risk_level = str(row["risk_level"])

        nav = fetch_price_series(code)
        metrics = calculate_metrics(nav)
        score = score_fund(metrics)

        records.append(
            {
                "code": code,
                "name": name,
                "risk_level": risk_level,
                **metrics,
                "score": score,
            }
        )

    result = pd.DataFrame(records)
    result = filter_funds(result, risk_levels=risk_levels, min_return=min_return, max_return=max_return)
    result = result.sort_values("score", ascending=False).head(top_n)
    return result.reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="自动选基工具（支持 akshare / 模拟数据）")
    parser.add_argument("--limit", type=int, default=50, help="扫描基金数量")
    parser.add_argument("--top", type=int, default=10, help="输出 Top N")
    parser.add_argument("--risk", nargs="*", default=[], help="风险等级筛选：低 中 高")
    parser.add_argument("--min-return", type=float, default=None, help="年化收益下限，例如 0.08")
    parser.add_argument("--max-return", type=float, default=None, help="年化收益上限，例如 0.30")
    parser.add_argument("--output", default="top_funds.csv", help="结果输出文件")
    args = parser.parse_args()

    top = run(
        limit=args.limit,
        top_n=args.top,
        risk_levels=args.risk,
        min_return=args.min_return,
        max_return=args.max_return,
    )

    if top.empty:
        print("无符合条件的基金。")
        return

    show = top.copy()
    for col in ["annual_return", "max_drawdown", "volatility"]:
        show[col] = (show[col] * 100).map(lambda x: f"{x:.2f}%")
    show["sharpe"] = show["sharpe"].map(lambda x: f"{x:.3f}")
    show["score"] = show["score"].map(lambda x: f"{x:.3f}")

    print("\nTop 基金：")
    print(show.to_string(index=False))

    top.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(f"\n已输出到: {args.output}")


if __name__ == "__main__":
    main()
