from datetime import datetime, timedelta


class CalendarService:
    def upcoming_events(self) -> list[dict]:
        now = datetime.utcnow()
        return [
            {"name": "US CPI", "impact": "high", "currency": "USD", "starts_at": now + timedelta(hours=6)},
            {"name": "BOE Rate Decision", "impact": "high", "currency": "GBP", "starts_at": now + timedelta(hours=20)},
            {"name": "JOLTS", "impact": "medium", "currency": "USD", "starts_at": now + timedelta(hours=30)},
        ]
