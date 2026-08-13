# Tabdeal Analysis Engine

This module is an analysis-only backend foundation for the existing crypto-trader5 project.

## Safety

`LIVE_TRADING=false` is mandatory. This release does not submit orders.

## Market data

The client uses the documented public market endpoints for ping, server time, exchange information, trades, and depth. Standard candle endpoints are not assumed. Candles are aggregated from trade data into 5m, 15m, and 1h intervals.

## Analysis

The engine includes EMA20/50/200, RSI14, MACD 12/26/9, Bollinger Bands, ATR14, volume ratio, weighted multi-timeframe scoring, and risk-based position sizing.

## Run

```bash
cd trader
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Do not put credentials in source control.
