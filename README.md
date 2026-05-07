# ops
运维平台

## AI 分析模式

### 投资建议模式

升级后的 AI 分析支持“投资建议模式”，输入用户持仓组合和每个基金指标，输出结构化投资建议报告。

#### 输入
- 用户持仓组合（基金名称、持仓金额、持仓占比）
- 每个基金指标（近一年收益率、波动率、最大回撤、夏普比率、行业/风格暴露）

#### 输出（结构化报告）

```yaml
report_type: investment_advisory
portfolio_assessment:
  conclusion: 合理 | 基本合理 | 不合理
  key_findings:
    - 组合分散度评估
    - 风险收益匹配评估
    - 单一基金集中度评估
rebalancing_recommendation:
  needed: true | false
  reason:
    - 偏离目标配置
    - 风险超出用户承受能力
    - 资产相关性过高
risk_alerts:
  level: 低 | 中 | 高
  items:
    - 市场波动风险
    - 行业集中风险
    - 流动性风险
optimization_suggestions:
  increase_positions:
    - fund: 基金A
      suggested_change_pct: "+5%"
      rationale: 提升防御性与回撤控制
  decrease_positions:
    - fund: 基金B
      suggested_change_pct: "-8%"
      rationale: 降低高波动与风格过度暴露
  maintain_positions:
    - fund: 基金C
      rationale: 风险收益比稳定
notes:
  - 本建议不构成保本或收益承诺
  - 调仓前请结合交易成本与税务影响
```

#### 规则说明
- 必须先判断组合合理性，再决定是否调仓。
- 调仓建议需给出“增减仓方向 + 建议幅度 + 依据”。
- 风险提示至少覆盖：波动、回撤、集中度三类风险。
- 输出必须为结构化报告，不使用纯自然段描述。
