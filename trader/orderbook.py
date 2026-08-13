from __future__ import annotations


def _volume(levels) -> float:
    total = 0.0
    for level in levels or []:
        try:
            total += float(level[1])
        except (TypeError, ValueError, IndexError):
            continue
    return total


def imbalance(depth: dict) -> float:
    bids = _volume(depth.get("bids", []))
    asks = _volume(depth.get("asks", []))
    total = bids + asks
    return 0.0 if total == 0 else (bids - asks) / total


def bias(depth: dict, threshold: float = 0.10) -> str:
    value = imbalance(depth)
    if value >= threshold:
        return "BULLISH"
    if value <= -threshold:
        return "BEARISH"
    return "NEUTRAL"
