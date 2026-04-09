from dataclasses import dataclass
from random import Random


@dataclass
class Candle:
    open: float
    high: float
    low: float
    close: float


class MarketDataService:
    """Provider abstraction. Swap internals without changing engines."""

    def __init__(self, seed: int = 42) -> None:
        self.rng = Random(seed)

    def get_multi_timeframe_snapshot(self, symbol: str) -> dict[str, list[Candle]]:
        base = {
            "XAUUSD": 2330,
            "XAGUSD": 28,
            "EURUSD": 1.09,
            "GBPUSD": 1.28,
            "USDJPY": 152,
            "BTCUSDT": 68000,
            "ETHUSDT": 3400,
        }.get(symbol, 100)

        def gen(count: int):
            candles: list[Candle] = []
            price = base
            for _ in range(count):
                drift = self.rng.uniform(-0.003, 0.003) * base
                nxt = max(price + drift, 0.0001)
                hi = max(price, nxt) + abs(self.rng.uniform(0, 0.001) * base)
                lo = min(price, nxt) - abs(self.rng.uniform(0, 0.001) * base)
                candles.append(Candle(open=price, high=hi, low=lo, close=nxt))
                price = nxt
            return candles

        return {tf: gen(200) for tf in ["M", "W", "D", "H4", "H1", "M15", "M5"]}
