import { SetupCardData } from "@/types/setup";

function value(v: number | null | undefined) {
  return v == null ? "-" : v.toLocaleString();
}

export function SetupCard({ setup }: { setup: SetupCardData }) {
  const noTrade = setup.setup_type === "NO_TRADE";

  return (
    <article className="rounded-xl border border-slate-700 bg-panel p-4 shadow-lg">
      <header className="mb-3 flex items-center justify-between">
        <h3 className="text-lg font-semibold">{setup.market}</h3>
        <span className="rounded px-2 py-1 text-xs font-medium bg-slate-800 text-slate-200">{setup.final_action}</span>
      </header>
      <p className="text-sm text-slate-300">{setup.setup_type} · {setup.strategy_used}</p>
      <p className="mt-1 text-xs text-slate-400">Bias: {setup.higher_timeframe_bias} | TF: {setup.timeframes_aligned.join(", ")}</p>

      {noTrade ? (
        <div className="mt-3 rounded-md bg-amber-900/40 p-3 text-sm text-amber-200">
          NO TRADE — {setup.no_trade_reason ?? "Insufficient confluence"}
        </div>
      ) : (
        <dl className="mt-3 grid grid-cols-2 gap-2 text-sm">
          <div><dt className="text-slate-400">Entry</dt><dd>{value(setup.entry_price)}</dd></div>
          <div><dt className="text-slate-400">Stop Loss</dt><dd>{value(setup.stop_loss)}</dd></div>
          <div><dt className="text-slate-400">TP1</dt><dd>{value(setup.take_profit_1)}</dd></div>
          <div><dt className="text-slate-400">TP2</dt><dd>{value(setup.take_profit_2)}</dd></div>
          <div><dt className="text-slate-400">TP3</dt><dd>{value(setup.take_profit_3)}</dd></div>
          <div><dt className="text-slate-400">R:R</dt><dd>{value(setup.risk_to_reward_ratio)}</dd></div>
        </dl>
      )}

      <p className="mt-3 text-xs text-slate-300">Event Risk: {setup.event_risk_status}</p>
      <p className="mt-1 text-xs text-slate-400">{setup.news_summary}</p>
      <p className="mt-1 text-xs text-slate-500">Invalidation: {setup.invalidation_rule}</p>
    </article>
  );
}
