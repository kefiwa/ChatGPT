from datetime import datetime

from app.engines.event_risk_engine import EventRiskEngine
from app.engines.signal_engine import SignalEngine
from app.engines.strategy_engine import StrategyEngine
from app.engines.trade_planner import TradePlanner
from app.models.enums import EventRisk
from app.schemas.setup import ScanResponse, SetupCard
from app.services.calendar_service import CalendarService
from app.services.market_data import MarketDataService
from app.services.news_service import NewsService


DEFAULT_SYMBOLS = [
    "XAUUSD", "XAGUSD", "EURUSD", "GBPUSD", "USDJPY", "GBPJPY", "EURJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD", "EURGBP", "GBPCHF", "AUDJPY",
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT",
]


class ScannerService:
    def __init__(self) -> None:
        self.market_data = MarketDataService()
        self.news = NewsService()
        self.calendar = CalendarService()
        self.signal = SignalEngine()
        self.strategy = StrategyEngine()
        self.risk = EventRiskEngine()
        self.trade_planner = TradePlanner()

    def scan(self, strategy: dict, symbols: list[str] | None = None) -> ScanResponse:
        events = self.calendar.upcoming_events()
        cards: list[SetupCard] = []

        for symbol in symbols or DEFAULT_SYMBOLS:
            candles = self.market_data.get_multi_timeframe_snapshot(symbol)
            structure = self.signal.analyze_structure(symbol, candles)
            strategy_result = self.strategy.evaluate(strategy, structure)
            risk_status = self.risk.assess(symbol, events, pre_news_minutes=strategy.get("risk", {}).get("pre_news_safety_window_minutes", 120))
            trade = self.trade_planner.build_trade_plan(structure, strategy_result.passed, strategy_result.score, risk_status)
            news_items = self.news.latest_market_news(symbol)

            cards.append(
                SetupCard(
                    market=symbol,
                    setup_type=trade["setup_type"],
                    strategy_used=strategy["name"],
                    timeframes_aligned=structure["timeframes_aligned"],
                    higher_timeframe_bias=structure["bias"],
                    entry_price=trade["entry_price"],
                    stop_loss=trade["stop_loss"],
                    take_profit_1=trade["take_profit_1"],
                    take_profit_2=trade["take_profit_2"],
                    take_profit_3=trade["take_profit_3"],
                    risk_to_reward_ratio=trade["risk_to_reward_ratio"],
                    confidence_score=strategy_result.score,
                    event_risk_status=risk_status,
                    news_summary=" | ".join([n["headline"] for n in news_items[:2]]),
                    invalidation_rule=trade["invalidation_rule"],
                    final_action=trade["final_action"],
                    no_trade_reason=trade["no_trade_reason"],
                    context={
                        "findings": structure["findings"],
                        "entry_zone": structure["entry_zone"],
                        "event_count": len(events),
                    },
                )
            )

        return ScanResponse(generated_at=datetime.utcnow(), setups=cards)
