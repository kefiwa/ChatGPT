from datetime import datetime
from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.enums import AssetClass, EventRisk, SetupStatus, SetupType, TradeAction


class Market(Base):
    __tablename__ = "markets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(24), unique=True, index=True)
    asset_class: Mapped[AssetClass] = mapped_column(Enum(AssetClass))
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    tick_size: Mapped[float] = mapped_column(Float, default=0.0001)


class Strategy(Base):
    __tablename__ = "strategies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    description: Mapped[str] = mapped_column(Text)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    rule_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class NewsItem(Base):
    __tablename__ = "news_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    headline: Mapped[str] = mapped_column(String(500))
    source: Mapped[str] = mapped_column(String(100))
    sentiment: Mapped[str] = mapped_column(String(20))
    impact: Mapped[str] = mapped_column(String(20))
    published_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    tags: Mapped[dict] = mapped_column(JSON)


class EventItem(Base):
    __tablename__ = "event_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_name: Mapped[str] = mapped_column(String(255))
    currency: Mapped[str] = mapped_column(String(12))
    impact: Mapped[str] = mapped_column(String(20))
    starts_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    metadata_json: Mapped[dict] = mapped_column(JSON)


class TradeSetup(Base):
    __tablename__ = "trade_setups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    market_id: Mapped[int] = mapped_column(ForeignKey("markets.id"), index=True)
    strategy_id: Mapped[int] = mapped_column(ForeignKey("strategies.id"), index=True)

    setup_type: Mapped[SetupType] = mapped_column(Enum(SetupType))
    action: Mapped[TradeAction] = mapped_column(Enum(TradeAction))
    event_risk: Mapped[EventRisk] = mapped_column(Enum(EventRisk))
    status: Mapped[SetupStatus] = mapped_column(Enum(SetupStatus), default=SetupStatus.VALID)

    confidence_score: Mapped[float] = mapped_column(Float)
    risk_reward: Mapped[float] = mapped_column(Float, nullable=True)

    entry_price: Mapped[float] = mapped_column(Float, nullable=True)
    stop_loss: Mapped[float] = mapped_column(Float, nullable=True)
    take_profit_1: Mapped[float] = mapped_column(Float, nullable=True)
    take_profit_2: Mapped[float] = mapped_column(Float, nullable=True)
    take_profit_3: Mapped[float] = mapped_column(Float, nullable=True)

    higher_tf_bias: Mapped[str] = mapped_column(String(32))
    aligned_timeframes: Mapped[list] = mapped_column(JSON)
    invalidation_rule: Mapped[str] = mapped_column(Text)
    news_summary: Mapped[str] = mapped_column(Text)
    rejection_reason: Mapped[str] = mapped_column(Text, nullable=True)

    raw_context: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    market: Mapped[Market] = relationship(Market)
    strategy: Mapped[Strategy] = relationship(Strategy)
