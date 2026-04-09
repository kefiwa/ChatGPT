from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.models.enums import EventRisk, SetupType, TradeAction


class SetupCard(BaseModel):
    market: str
    setup_type: SetupType
    strategy_used: str
    timeframes_aligned: list[str]
    higher_timeframe_bias: str
    entry_price: float | None = None
    stop_loss: float | None = None
    take_profit_1: float | None = None
    take_profit_2: float | None = None
    take_profit_3: float | None = None
    risk_to_reward_ratio: float | None = None
    confidence_score: float
    event_risk_status: EventRisk
    news_summary: str
    invalidation_rule: str
    final_action: TradeAction
    no_trade_reason: str | None = None
    context: dict[str, Any]


class ScanResponse(BaseModel):
    generated_at: datetime
    setups: list[SetupCard]
