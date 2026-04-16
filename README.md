# AI Trading Analyst: Research & Verification Tool

A professional-grade trading intelligence suite designed for multi-agent market analysis, institutional-style reporting, and historical performance verification.

---

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install yfinance reportlab pandas numpy
   ```

2. **Run a Full Analysis**:
   Use the `/trade analyze` command to launch 5 parallel agents for Technical, Fundamental, Sentiment, Risk, and Thesis analysis.
   ```bash
   # Example (inside your AI assistant)
   /trade analyze DE40
   ```

3. **Generate a PDF Report**:
   Compile your markdown analyses into a professional 6-page investment report.
   ```bash
   /trade report-pdf
   ```

---

## 🛠️ Core Features

### 1. Multi-Agent Analysis
The tool orchestrates specialized agents to score stocks across 5 dimensions:
- **Technical**: EMA/RSI trends, support/resistance, and volume profiles.
- **Fundamental**: Valuation, growth, profitability, and moat strength.
- **Sentiment**: News tone, social buzz, and institutional positioning.
- **Risk**: Volatility profiling and position sizing (Kelly Criterion).
- **Thesis**: Bull/Bear case synthesis and catalyst calendars.

### 2. PDF Report Generator
Located in `scripts/generate_trade_pdf.py`. It converts `TRADE-*.md` files into a structured PDF with score gauges and professional formatting.
```bash
python scripts/generate_trade_pdf.py data.json  # Or use the /trade report-pdf skill
```

### 3. Verification & Backtesting
Ensuring the AI's analysis is logically sound and historically accurate.

#### **Trade Consistency Checker**
Verifies that trade parameters (Entry/Stop/Target) are logically consistent and grounded in recent price action.
```bash
python scripts/backtest_analysis.py TRADE-ANALYSIS-DE40.md
```

#### **3-Year Multi-Metric Engine**
Simulates a strategy over 3 years to calculate professional ratios:
- **Sharpe Ratio**: Risk-adjusted performance.
- **Max Drawdown**: Capital protection assessment.
- **Profit Factor**: Strategy efficiency.
- **Buy & Hold Benchmark**: Comparison against the raw index.
```bash
python scripts/backtest_engine.py ^GDAXI
```

---

## 🧭 Skill Command Reference

| Command | Description |
| :--- | :--- |
| `/trade analyze <TICKER>` | Full 5-agent deep dive analysis. |
| `/trade report-pdf` | Generate comprehensive PDF investment report. |
| `/trade technical <TICKER>` | Technical-only chart and level analysis. |
| `/trade fundamental <TICKER>` | Valuation and balance sheet deep dive. |
| `/trade portfolio` | Review current holdings and concentration risk. |
| `/trade watchlist` | Manage and score your stock watchlist. |
| `/trade quick <TICKER>` | Rapid snapshot of current market state. |

---

## 📁 Repository Structure

- `.claude/skills/`: Core AI logic and command triggers.
- `scripts/`: Python utilities for PDF generation and backtesting.
- `BACKTEST_RESULTS_TEMPLATE.md`: Template for performance reports.
- `TRADE-ANALYSIS-DE40.md`: Example of a verified analyst report.

---

> **DISCLAIMER:** This tool is for educational and research purposes only. It is NOT financial advice. Trading involves significant risk of loss. Always consult a licensed financial advisor.
