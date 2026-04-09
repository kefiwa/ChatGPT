# MARKET BIAS INTELLIGENCE SYSTEM (MBIS)

Production-oriented full-stack scaffold for disciplined multi-asset setup generation (BUY / SELL / BUY LIMIT / SELL LIMIT / NO TRADE) with strict risk gating.

## 1) Architecture

### High-level services
- **Frontend (Next.js + TypeScript + Tailwind)**: Dashboard for setup cards, event risk state, actionable status, and NO TRADE reasons.
- **Backend (FastAPI)**: Strategy engine, signal engine, event-risk engine, trade planner, and scan API.
- **Data layer**: PostgreSQL schema for markets, strategies, setups, news, and events.
- **Caching / jobs**: Redis-ready architecture and worker hooks for scanner + alerts.
- **Provider abstractions**:
  - `MarketDataService` for candle provider swapping.
  - `NewsService` for market-moving news feeds.
  - `CalendarService` for economic event feeds.

### Analysis pipeline
1. Pull multi-timeframe candles (M/W/D/H4/H1/M15/M5).
2. Build higher timeframe bias + structure findings (ICT/SMC-compatible primitives).
3. Evaluate user strategy JSON rules.
4. Assess high-impact event proximity.
5. Generate full trade plan (Entry/SL/TP1/TP2/TP3 + RR + invalidation) **or** NO TRADE.
6. Return normalized setup cards for UI/API.

## 2) Data models / schema
- SQL schema: `infra/schema.sql`
- SQLAlchemy entities: `apps/api/app/models/entities.py`
- Core enums: `apps/api/app/models/enums.py`

## 3) Backend API design
- `GET /health` → liveness.
- `GET /v1/scan` → run scan using default ICT/SMC strategy.
- `POST /v1/scan` → run scan with custom strategy JSON body.

Response model includes:
- Market, Setup Type, Strategy, Timeframes, Bias
- Entry, SL, TP1/TP2/TP3, RR
- Confidence, Event Risk, News Summary, Invalidation rule
- Final Action and NO TRADE reason when filtered out

## 4) Frontend UI structure
- `apps/web/app/page.tsx`: Dashboard shell, summary metrics, setup grid.
- `apps/web/components/setup-card.tsx`: Actionable and NO TRADE cards.
- `apps/web/lib/api.ts`: API client abstraction.
- `apps/web/types/setup.ts`: strict typed contracts.

## 5) Signal engine logic
- File: `apps/api/app/engines/signal_engine.py`
- Implements top-down structure pass:
  - HTF directional vote from M/W/D moving-mean trend snapshots.
  - H4/H1 alignment checks.
  - Findings map for liquidity sweep, BOS, MSS, FVG, OB, session liquidity, premium/discount.
  - Entry zone extraction (high/low/mid/last) for planner consumption.

## 6) Trade planner logic
- File: `apps/api/app/engines/trade_planner.py`
- Strictly emits complete plans or NO TRADE.
- BUY bias → `BUY_LIMIT`; SELL bias → `SELL_LIMIT`.
- Computes:
  - Entry at zone midpoint
  - SL beyond protected swing
  - TP1/TP2/TP3 via R-multiples
  - RR validation against minimum threshold
- Blocks execution if:
  - strategy confluences fail
  - high-impact event window is too close
  - risk math is invalid or RR insufficient

## 7) News + event-risk logic
- News ingestion: `apps/api/app/services/news_service.py`
- Calendar ingestion: `apps/api/app/services/calendar_service.py`
- Event risk classification: `apps/api/app/engines/event_risk_engine.py`
  - SAFE_TO_TRADE
  - CAUTION
  - DO_NOT_ENTER_BEFORE_NEWS

## 8) Folder structure

```text
apps/
  api/
    app/
      api/
      core/
      db/
      engines/
      models/
      schemas/
      services/
      workers/
  web/
    app/
    components/
    lib/
    types/
infra/
examples/
```

## 9) Initial production-ready codebase
Included in this repository as a clean modular baseline with clear extension points for real provider integration and persistence wiring.

## 10) Setup instructions

### Backend
```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd apps/web
npm install
NEXT_PUBLIC_API_BASE=http://localhost:8000 npm run dev
```

### Database
- Apply `infra/schema.sql` to PostgreSQL.
- Configure `.env` for `DB_URL` and `REDIS_URL` as needed.

## 11) Example strategy JSON format
See `examples/strategy.ict-smc.json`.

## 12) Example valid setup response
See `examples/response.valid.json`.

## 13) Example NO TRADE response
See `examples/response.no-trade.json`.

## 14) Future upgrades
- Real exchange/broker connectivity and order staging.
- Replay/backtest mode with walk-forward validation.
- Regime-aware volatility filters (ATR/range compression).
- ML-assisted confluence weighting from historical outcomes.
- User/org auth + role-based strategy governance.
- Push alerts (Telegram/Slack/Email/Webhooks) with deduping.
- Chart snapshots + annotation overlays for each setup.
