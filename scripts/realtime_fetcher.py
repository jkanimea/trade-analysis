#!/usr/bin/env python3
import sys
import json
try:
    import yfinance as yf
except ImportError:
    print("Error: yfinance is required. Install with: pip install yfinance")
    sys.exit(1)

def get_realtime_data(ticker_symbol):
    """Fetches near real-time data for a ticker using yfinance."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # Get 1-day history with 1-minute intervals for the most recent data
        df = ticker.history(period="1d", interval="1m")
        
        if df.empty:
            # Fallback to info for metadata if no intraday data
            info = ticker.info
            return {
                "symbol": ticker_symbol,
                "price": info.get("currentPrice") or info.get("regularMarketPrice"),
                "change": info.get("regularMarketChange"),
                "change_percent": info.get("regularMarketChangePercent"),
                "market_cap": info.get("marketCap"),
                "volume": info.get("regularMarketVolume"),
                "avg_volume": info.get("averageVolume"),
                "52w_high": info.get("fiftyTwoWeekHigh"),
                "52w_low": info.get("fiftyTwoWeekLow"),
                "source": "info_fallback"
            }

        last_quote = df.iloc[-1]
        prev_close = ticker.info.get("previousClose")
        
        price = last_quote['Close']
        change = price - prev_close if prev_close else 0
        change_percent = (change / prev_close) * 100 if prev_close else 0
        
        return {
            "symbol": ticker_symbol,
            "price": round(price, 2),
            "change": round(change, 2),
            "change_percent": round(change_percent, 2),
            "open": round(last_quote['Open'], 2),
            "high": round(df['High'].max(), 2),
            "low": round(df['Low'].min(), 2),
            "volume": int(df['Volume'].sum()),
            "timestamp": str(df.index[-1]),
            "source": "intraday_1m"
        }
    except Exception as e:
        return {"error": str(e), "symbol": ticker_symbol}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python realtime_fetcher.py <TICKER>")
        sys.exit(1)
        
    symbol = sys.argv[1].upper()
    data = get_realtime_data(symbol)
    
    # Output as JSON for skill ingestion
    print(json.dumps(data, indent=2))
