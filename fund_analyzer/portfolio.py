"""持仓管理模块。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Position:
    """单只基金持仓信息。"""

    fund_code: str
    amount: float
    cost: float = 0.0


@dataclass
class Portfolio:
    """持仓组合。"""

    positions: Dict[str, Position] = field(default_factory=dict)

    def add_position(self, fund_code: str, amount: float, cost: float = 0.0) -> None:
        """新增或更新持仓。"""
        self.positions[fund_code] = Position(fund_code=fund_code, amount=amount, cost=cost)

    def remove_position(self, fund_code: str) -> None:
        """删除持仓。"""
        self.positions.pop(fund_code, None)

    def list_positions(self) -> List[Position]:
        """列出全部持仓。"""
        return list(self.positions.values())
