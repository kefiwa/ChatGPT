from app.models.enums import EventRisk, SetupType, TradeAction


class TradePlanner:
    MIN_RR = 1.8

    def build_trade_plan(self, structure: dict, strategy_passed: bool, score: float, event_risk: EventRisk) -> dict:
        if not strategy_passed:
            return self._no_trade(structure, score, event_risk, "Strategy confluences incomplete")

        if event_risk == EventRisk.DO_NOT_ENTER_BEFORE_NEWS:
            return self._no_trade(structure, score, event_risk, "Major high-impact event is too close")

        zone = structure["entry_zone"]
        bias = structure["bias"]

        if bias == "bullish":
            setup_type = SetupType.BUY_LIMIT
            entry = zone["mid"]
            sl = zone["low"] * 0.999
            risk = entry - sl
            tp1 = entry + risk * 2.0
            tp2 = entry + risk * 3.0
            tp3 = entry + risk * 4.0
            invalidation = "Invalidate if H1 closes below the protected low / order block base."
            action = TradeAction.PLACE_LIMIT_ORDER
        else:
            setup_type = SetupType.SELL_LIMIT
            entry = zone["mid"]
            sl = zone["high"] * 1.001
            risk = sl - entry
            tp1 = entry - risk * 2.0
            tp2 = entry - risk * 3.0
            tp3 = entry - risk * 4.0
            invalidation = "Invalidate if H1 closes above the protected high / order block ceiling."
            action = TradeAction.PLACE_LIMIT_ORDER

        rr = abs((tp1 - entry) / (entry - sl if bias == "bullish" else sl - entry))

        if risk <= 0 or rr < self.MIN_RR:
            return self._no_trade(structure, score, event_risk, "No logical or acceptable risk/reward profile")

        if event_risk == EventRisk.CAUTION:
            action = TradeAction.WAIT

        return {
            "setup_type": setup_type,
            "entry_price": round(entry, 6),
            "stop_loss": round(sl, 6),
            "take_profit_1": round(tp1, 6),
            "take_profit_2": round(tp2, 6),
            "take_profit_3": round(tp3, 6),
            "risk_to_reward_ratio": round(rr, 2),
            "invalidation_rule": invalidation,
            "final_action": action,
            "no_trade_reason": None,
        }

    def _no_trade(self, structure: dict, score: float, event_risk: EventRisk, reason: str) -> dict:
        return {
            "setup_type": SetupType.NO_TRADE,
            "entry_price": None,
            "stop_loss": None,
            "take_profit_1": None,
            "take_profit_2": None,
            "take_profit_3": None,
            "risk_to_reward_ratio": None,
            "invalidation_rule": "No setup - wait for cleaner structure.",
            "final_action": TradeAction.NO_TRADE,
            "no_trade_reason": reason,
        }
