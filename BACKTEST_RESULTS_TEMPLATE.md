# 📊 Backtest Performance Report: {{symbol}}
> Period: {{start_date}} to {{end_date}}

## Executive Summary
The strategy simulated over this {{period}} year period resulted in a **{{status}}** performance. While the strategy maintained a relatively low drawdown, it {{performance_vs_benchmark}} the Buy & Hold benchmark.

---

## 📈 Account Health Metrics

| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| **Total Strategy Return** | {{strategy_return}}% | Total account growth over period |
| **Buy & Hold Return** | {{bh_return}}% | Benchmark index performance |
| **Alpha Generated** | {{alpha}}% | Excess return over benchmark |
| **Sharpe Ratio** | {{sharpe}} | Risk-adjusted return ( > 1.0 is good) |
| **Max Drawdown** | {{drawdown}}% | Maximum peak-to-trough decline |

---

## 🎯 Trade Statistics

| Metric | Value |
| :--- | :--- |
| **Total Trades** | {{total_trades}} |
| **Win Rate** | {{win_rate}}% |
| **Profit Factor** | {{profit_factor}} |
| **Avg PnL / Trade** | ${{avg_pnl}} |

---

## 🔍 Strategy Verdict
{{verdict}}

---

> **DISCLAIMER:** Past performance is not indicative of future results. Backtesting uses historical data and does not account for slippage, commissions, or unexpected market shocks. Always consult a financial advisor.
