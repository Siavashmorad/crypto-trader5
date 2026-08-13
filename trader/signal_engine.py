from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Signal:
    side: str
    score: int
    reason: str


def score_signal(h1: dict, m15: dict, m5: dict, orderbook: str = "NEUTRAL", minimum: int = 70) -> Signal:
    long_score = 0
    short_score = 0
    reasons = []

    for data, weight in ((h1, 25), (m15, 20)):
        trend = data.get("trend", "NEUTRAL")
        if trend == "BULLISH": long_score += weight
        if trend == "BEARISH": short_score += weight

    for data in (h1, m15, m5):
        ema20, ema50, ema200 = data.get("ema20"), data.get("ema50"), data.get("ema200")
        if None not in (ema20, ema50, ema200):
            if ema20 > ema50 > ema200: long_score += 5
            if ema20 < ema50 < ema200: short_score += 5

    macd = m5.get("macd")
    macd_signal = m5.get("macd_signal")
    if macd is not None and macd_signal is not None:
        if macd > macd_signal: long_score += 10
        elif macd < macd_signal: short_score += 10

    rsi = m5.get("rsi14")
    if rsi is not None:
        if 50 <= rsi <= 68: long_score += 10
        elif 32 <= rsi <= 50: short_score += 10

    ratio = m5.get("volume_ratio")
    if ratio is not None and ratio >= 1.2:
        if long_score >= short_score: long_score += 5
        else: short_score += 5

    structure = m5.get("structure", "NEUTRAL")
    if structure == "BULLISH": long_score += 10
    elif structure == "BEARISH": short_score += 10

    if orderbook == "BULLISH": long_score += 5
    elif orderbook == "BEARISH": short_score += 5

    if long_score >= short_score and long_score >= minimum:
        return Signal("LONG", min(100, long_score), "Bullish multi-timeframe confirmation")
    if short_score > long_score and short_score >= minimum:
        return Signal("SHORT", min(100, short_score), "Bearish multi-timeframe confirmation")
    return Signal("WAIT", max(long_score, short_score), "Insufficient confirmation")
