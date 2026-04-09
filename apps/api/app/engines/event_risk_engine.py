from datetime import datetime

from app.models.enums import EventRisk


class EventRiskEngine:
    def assess(self, symbol: str, events: list[dict], pre_news_minutes: int = 120) -> EventRisk:
        now = datetime.utcnow()
        symbol_ccy = {"EUR": "EUR", "GBP": "GBP", "JPY": "JPY", "USD": "USD", "AUD": "AUD", "NZD": "NZD", "CAD": "CAD", "CHF": "CHF"}
        relevant = []

        for e in events:
            if e["currency"] in symbol or symbol.endswith("USDT"):
                delta_min = (e["starts_at"] - now).total_seconds() / 60
                if delta_min > 0:
                    relevant.append((e, delta_min))

        if not relevant:
            return EventRisk.SAFE_TO_TRADE

        nearest, mins = sorted(relevant, key=lambda x: x[1])[0]
        if nearest["impact"] == "high" and mins <= pre_news_minutes:
            return EventRisk.DO_NOT_ENTER_BEFORE_NEWS
        if nearest["impact"] == "high" and mins <= pre_news_minutes * 3:
            return EventRisk.CAUTION
        return EventRisk.SAFE_TO_TRADE
