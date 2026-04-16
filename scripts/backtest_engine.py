#!/usr/bin/env python3
import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

try:
    import yfinance as yf
except ImportError:
    print("Error: yfinance is required. Install with: pip install yfinance")
    sys.exit(1)

# Fix for Windows terminal encoding issues
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def calculate_metrics(df, account_history, trades):
    """Calculates professional trading metrics."""
    if not trades:
        return None

    # Account metrics
    returns = pd.Series(account_history).pct_change().dropna()
    total_return = (account_history[-1] / account_history[0]) - 1
    
    # Sharpe Ratio (annualized, assuming 0% risk-free rate)
    sharpe = (returns.mean() / returns.std()) * np.sqrt(252) if len(returns) > 1 and returns.std() != 0 else 0
    
    # Max Drawdown
    peak = pd.Series(account_history).expanding(min_periods=1).max()
    drawdowns = (pd.Series(account_history) - peak) / peak
    max_drawdown = drawdowns.min()

    # Trade metrics
    trade_pnls = [t['pnl'] for t in trades]
    wins = [p for p in trade_pnls if p > 0]
    losses = [p for p in trade_pnls if p <= 0]
    
    win_rate = len(wins) / len(trades) if trades else 0
    profit_factor = abs(sum(wins) / sum(losses)) if losses and sum(losses) != 0 else float('inf')
    
    return {
        "total_return": total_return,
        "sharpe_ratio": sharpe,
        "max_drawdown": max_drawdown,
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "total_trades": len(trades),
        "avg_trade_pnl": np.mean(trade_pnls) if trades else 0,
        "trades": trades
    }

def run_backtest(symbol, start_date, end_date, initial_capital=100000, risk_per_trade=0.02):
    """Simulates a 3-year technical strategy."""
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date, end=end_date)
    
    if df.empty:
        return f"No data found for {symbol}"

    # Indicators
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['EMA200'] = df['Close'].ewm(span=200, adjust=False).mean()
    
    # Simple RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # ATR for stop loss
    high_low = df['High'] - df['Low']
    high_cp = np.abs(df['High'] - df['Close'].shift())
    low_cp = np.abs(df['Low'] - df['Close'].shift())
    df['ATR'] = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1).rolling(14).mean()

    # Simulation Variables
    capital = initial_capital
    account_history = [capital]
    trades = []
    position = None # {entry_price, stop_loss, target, shares}
    
    # Optimization: Iterate days
    for i in range(200, len(df)): # Start after EMA200 warmup
        current_date = df.index[i]
        current_price = df.iloc[i]['Close']
        current_atr = df.iloc[i]['ATR']
        
        # Benchmarking - Track account value daily even if no trade
        if position is None:
            account_history.append(capital)
        else:
            current_value = capital + (current_price - position['entry_price']) * position['shares']
            account_history.append(current_value)

            # Check Exit Conditions
            if df.iloc[i]['Low'] <= position['stop_loss']:
                # Exit at Stop
                pnl = (position['stop_loss'] - position['entry_price']) * position['shares']
                capital += pnl
                trades.append({
                    "ticker": symbol,
                    "type": "LONG",
                    "entry_date": position['entry_date'],
                    "entry_price": position['entry_price'],
                    "exit_date": current_date,
                    "exit_price": position['stop_loss'],
                    "pnl": pnl,
                    "reason": "STOP"
                })
                position = None
            elif df.iloc[i]['High'] >= position['target']:
                # Exit at Target
                pnl = (position['target'] - position['entry_price']) * position['shares']
                capital += pnl
                trades.append({
                    "ticker": symbol,
                    "type": "LONG",
                    "entry_date": position['entry_date'],
                    "entry_price": position['entry_price'],
                    "exit_date": current_date,
                    "exit_price": position['target'],
                    "pnl": pnl,
                    "reason": "TARGET"
                })
                position = None

        # Check Entry Conditions (Long only)
        if position is None and i < len(df) - 1:
            # Bullish Regime: EMA 50 > EMA 200
            if df.iloc[i]['EMA50'] > df.iloc[i]['EMA200']:
                # Pullback Entry: RSI drops below 50
                if df.iloc[i]['RSI'] < 50:
                    risk_amount = capital * risk_per_trade
                    stop_dist = max(2 * current_atr, current_price * 0.01) # Min 1% stop
                    if stop_dist > 0:
                        shares = risk_amount / stop_dist
                        position = {
                            "ticker": symbol,
                            "entry_date": current_date,
                            "entry_price": current_price,
                            "stop_loss": current_price - stop_dist,
                            "target": current_price + (2 * stop_dist), # 2:1 R/R
                            "shares": shares
                        }

    # Final stats
    metrics = calculate_metrics(df, account_history, trades)
    
    # Buy & Hold Benchmark
    bh_return = (df.iloc[-1]['Close'] / df.iloc[0]['Close']) - 1
    
    return metrics, bh_return

if __name__ == "__main__":
    symbol = sys.argv[1] if len(sys.argv) > 1 else "^GDAXI"
    period_years = 3
    end_date = datetime.now()
    start_date = end_date - timedelta(days=period_years*365 + 200) # +200 for indicator warmup
    
    print(f"🚀 Running 3-Year Backtest for {symbol}...")
    print(f"Period: {start_date.date()} to {end_date.date()}")
    
    metrics, bh_return = run_backtest(symbol, start_date, end_date)
    
    if isinstance(metrics, str):
        print(metrics)
    elif metrics is None:
        print("No trades were triggered by the strategy logic.")
    else:
        print("\n--- PERFORMANCE SUMMARY ---")
        print(f"Total Strategy Return: {metrics['total_return']*100:.2f}%")
        print(f"Buy & Hold Return:     {bh_return*100:.2f}%")
        print(f"Alpha Generated:       {(metrics['total_return'] - bh_return)*100:.2f}%")
        print("-" * 30)
        print(f"Sharpe Ratio:          {metrics['sharpe_ratio']:.2f}")
        print(f"Max Drawdown:          {metrics['max_drawdown']*100:.2f}%")
        print(f"Profit Factor:         {metrics['profit_factor']:.2f}")
        print(f"Win Rate:              {metrics['win_rate']*100:.2f}%")
        print(f"Total Trades:          {metrics['total_trades']}")
        print(f"Avg PnL per Trade:     ${metrics['avg_trade_pnl']:.2f}")
        print("-" * 30)

        print("\n--- DETAILED TRADE LOG ---")
        print(f"{'Date':<12} | {'Type':<4} | {'Entry':<8} | {'Exit':<8} | {'PnL':<8} | {'Reason':<6}")
        print("-" * 60)
        for t in metrics['trades']:
            date_str = str(t['entry_date'].date())
            pnl_str = f"${t['pnl']:>8.2f}"
            print(f"{date_str:<12} | {t['type']:<4} | {t['entry_price']:>8.1f} | {t['exit_price']:>8.1f} | {pnl_str} | {t['reason']:<6}")
        print("-" * 60)
