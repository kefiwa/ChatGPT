from datetime import datetime, timedelta


class NewsService:
    def latest_market_news(self, symbol: str) -> list[dict]:
        now = datetime.utcnow()
        return [
            {
                "headline": f"Macro flows impacting {symbol}",
                "impact": "medium",
                "sentiment": "neutral",
                "published_at": now - timedelta(minutes=45),
                "tags": ["inflation", "usd", "risk_sentiment"],
            },
            {
                "headline": "US yields stabilize after policy remarks",
                "impact": "high",
                "sentiment": "bullish_usd",
                "published_at": now - timedelta(hours=2),
                "tags": ["yields", "fed"],
            },
        ]
