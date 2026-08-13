from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("TABDEAL_BASE_URL", "https://api1.tabdeal.org").rstrip("/")
    api_key: str = os.getenv("TABDEAL_API_KEY", "")
    api_secret: str = os.getenv("TABDEAL_API_SECRET", "")
    symbol: str = os.getenv("SYMBOL", "BTC_USDT")
    min_signal_score: int = int(os.getenv("MIN_SIGNAL_SCORE", "70"))
    risk_percent: float = float(os.getenv("RISK_PERCENT", "1"))
    leverage: float = float(os.getenv("LEVERAGE", "5"))
    live_trading: bool = _bool(os.getenv("LIVE_TRADING"), False)
    trade_poll_seconds: float = float(os.getenv("TRADE_POLL_SECONDS", "2"))

    def __post_init__(self) -> None:
        if self.live_trading:
            raise ValueError("LIVE_TRADING must remain false in the analysis-only release")
        if not 0 < self.risk_percent <= 100:
            raise ValueError("RISK_PERCENT must be between 0 and 100")
        if self.leverage <= 0:
            raise ValueError("LEVERAGE must be positive")
        if not 0 <= self.min_signal_score <= 100:
            raise ValueError("MIN_SIGNAL_SCORE must be between 0 and 100")
