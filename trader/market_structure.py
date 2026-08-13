from __future__ import annotations


def classify_structure(candles: list[dict], lookback: int = 3) -> str:
    if len(candles) < lookback * 2 + 1:
        return "NEUTRAL"
    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    recent_high = max(highs[-lookback:])
    previous_high = max(highs[-2 * lookback:-lookback])
    recent_low = min(lows[-lookback:])
    previous_low = min(lows[-2 * lookback:-lookback])
    if recent_high > previous_high and recent_low > previous_low:
        return "BULLISH"
    if recent_high < previous_high and recent_low < previous_low:
        return "BEARISH"
    return "NEUTRAL"
