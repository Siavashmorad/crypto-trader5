from __future__ import annotations


def position_size(balance: float, risk_percent: float, entry: float, stop: float, leverage: float = 1.0) -> float:
    if balance <= 0 or risk_percent <= 0 or entry <= 0 or stop <= 0 or leverage <= 0:
        raise ValueError("invalid risk inputs")
    distance = abs(entry - stop)
    if distance == 0:
        raise ValueError("entry and stop must differ")
    risk_cash = balance * risk_percent / 100.0
    raw_qty = risk_cash / distance
    max_notional_qty = (balance * leverage) / entry
    return min(raw_qty, max_notional_qty)


def risk_reward(side: str, entry: float, stop: float, target: float) -> float:
    risk = abs(entry - stop)
    if risk == 0:
        return 0.0
    reward = (target - entry) if side == "LONG" else (entry - target)
    return reward / risk
