import { SetupCard } from "@/components/setup-card";
import { getSetups } from "@/lib/api";

export default async function HomePage() {
  const data = await getSetups();
  const actionable = data.setups.filter((s) => s.setup_type !== "NO_TRADE").length;

  return (
    <main className="mx-auto max-w-7xl p-6">
      <section className="mb-6 rounded-xl border border-slate-700 bg-panel p-5">
        <h1 className="text-2xl font-bold">Market Bias Intelligence System</h1>
        <p className="mt-1 text-sm text-slate-300">AI-powered multi-asset setup filtering and trade planning.</p>
        <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
          <div className="rounded bg-slate-900 p-3">Generated: {new Date(data.generated_at).toLocaleString()}</div>
          <div className="rounded bg-slate-900 p-3">Markets scanned: {data.setups.length}</div>
          <div className="rounded bg-slate-900 p-3">Actionable setups: {actionable}</div>
        </div>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {data.setups.map((setup) => (
          <SetupCard key={setup.market} setup={setup} />
        ))}
      </section>
    </main>
  );
}
