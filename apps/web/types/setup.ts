export type SetupType = "BUY" | "SELL" | "BUY_LIMIT" | "SELL_LIMIT" | "NO_TRADE";
export type FinalAction = "EXECUTE" | "PLACE_LIMIT_ORDER" | "WAIT" | "NO_TRADE";

export interface SetupCardData {
  market: string;
  setup_type: SetupType;
  strategy_used: string;
  timeframes_aligned: string[];
  higher_timeframe_bias: string;
  entry_price: number | null;
  stop_loss: number | null;
  take_profit_1: number | null;
  take_profit_2: number | null;
  take_profit_3: number | null;
  risk_to_reward_ratio: number | null;
  confidence_score: number;
  event_risk_status: string;
  news_summary: string;
  invalidation_rule: string;
  final_action: FinalAction;
  no_trade_reason?: string | null;
}

export interface ScanResponse {
  generated_at: string;
  setups: SetupCardData[];
}
