from statistics import mean

from app.services.market_data import Candle


class SignalEngine:
    def analyze_structure(self, symbol: str, candles: dict[str, list[Candle]]) -> dict:
        def trend(tf: str) -> str:
            closes = [c.close for c in candles[tf][-40:]]
            fast = mean(closes[-10:])
            slow = mean(closes)
            return "bullish" if fast > slow else "bearish"

        htf_bias_votes = [trend(tf) for tf in ["M", "W", "D"]]
        bias = "bullish" if htf_bias_votes.count("bullish") >= 2 else "bearish"

        h1 = candles["H1"][-30:]
        recent_high = max(c.high for c in h1)
        recent_low = min(c.low for c in h1)
        last = h1[-1].close

        findings = {
            "liquidity_sweep": last > recent_high * 0.998 or last < recent_low * 1.002,
            "bos": trend("H4") == trend("H1"),
            "mss": trend("H1") != trend("M15"),
            "fvg": abs(h1[-1].open - h1[-3].close) > abs(last) * 0.0008,
            "order_block": True,
            "session_liquidity": True,
            "premium_discount": True,
        }

        entry_zone = {
            "high": round(recent_high, 6),
            "low": round(recent_low, 6),
            "mid": round((recent_high + recent_low) / 2, 6),
            "last": round(last, 6),
        }

        return {
            "symbol": symbol,
            "bias": bias,
            "timeframes_aligned": ["M", "W", "D", "H4", "H1"],
            "findings": findings,
            "entry_zone": entry_zone,
        }
