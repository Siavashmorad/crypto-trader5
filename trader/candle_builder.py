from __future__ import annotations

import pandas as pd

INTERVAL_MS = {"5m": 300000, "15m": 900000, "1h": 3600000}


def build_candles(items, interval):
    if interval not in INTERVAL_MS:
        raise ValueError("unsupported interval")
    if not items:
        return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
    step = INTERVAL_MS[interval]
    rows = []
    for item in items:
        ts = item.get("timestamp", item.get("time", item.get("T")))
        price = item.get("price", item.get("p"))
        qty = item.get("quantity", item.get("qty", item.get("q", item.get("amount"))))
        if ts is None or price is None or qty is None:
            continue
        ts = int(float(ts))
        if ts < 10000000000:
            ts *= 1000
        bucket = ts - ts % step
        rows.append((bucket, float(price), float(qty)))
    if not rows:
        return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
    df = pd.DataFrame(rows, columns=["bucket", "price", "quantity"]).sort_values("bucket")
    out = df.groupby("bucket", sort=True).agg(
        open=("price", "first"), high=("price", "max"), low=("price", "min"),
        close=("price", "last"), volume=("quantity", "sum")
    ).reset_index()
    out["timestamp"] = pd.to_datetime(out.pop("bucket"), unit="ms", utc=True)
    return out[["timestamp", "open", "high", "low", "close", "volume"]]
