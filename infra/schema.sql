CREATE TYPE asset_class AS ENUM ('forex', 'metal', 'crypto');
CREATE TYPE setup_type AS ENUM ('BUY', 'SELL', 'BUY_LIMIT', 'SELL_LIMIT', 'NO_TRADE');
CREATE TYPE trade_action AS ENUM ('EXECUTE', 'PLACE_LIMIT_ORDER', 'WAIT', 'NO_TRADE');
CREATE TYPE event_risk AS ENUM ('SAFE_TO_TRADE', 'CAUTION', 'DO_NOT_ENTER_BEFORE_NEWS');
CREATE TYPE setup_status AS ENUM ('valid', 'invalidated', 'closed');

CREATE TABLE markets (
  id SERIAL PRIMARY KEY,
  symbol VARCHAR(24) UNIQUE NOT NULL,
  asset_class asset_class NOT NULL,
  is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
  tick_size DOUBLE PRECISION NOT NULL DEFAULT 0.0001
);

CREATE TABLE strategies (
  id SERIAL PRIMARY KEY,
  name VARCHAR(128) UNIQUE NOT NULL,
  description TEXT NOT NULL,
  is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
  rule_json JSONB NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE news_items (
  id SERIAL PRIMARY KEY,
  headline VARCHAR(500) NOT NULL,
  source VARCHAR(100) NOT NULL,
  sentiment VARCHAR(20) NOT NULL,
  impact VARCHAR(20) NOT NULL,
  published_at TIMESTAMP NOT NULL,
  tags JSONB NOT NULL
);

CREATE TABLE event_items (
  id SERIAL PRIMARY KEY,
  event_name VARCHAR(255) NOT NULL,
  currency VARCHAR(12) NOT NULL,
  impact VARCHAR(20) NOT NULL,
  starts_at TIMESTAMP NOT NULL,
  metadata_json JSONB NOT NULL
);

CREATE TABLE trade_setups (
  id SERIAL PRIMARY KEY,
  market_id INTEGER REFERENCES markets(id) NOT NULL,
  strategy_id INTEGER REFERENCES strategies(id) NOT NULL,
  setup_type setup_type NOT NULL,
  action trade_action NOT NULL,
  event_risk event_risk NOT NULL,
  status setup_status NOT NULL DEFAULT 'valid',
  confidence_score DOUBLE PRECISION NOT NULL,
  risk_reward DOUBLE PRECISION,
  entry_price DOUBLE PRECISION,
  stop_loss DOUBLE PRECISION,
  take_profit_1 DOUBLE PRECISION,
  take_profit_2 DOUBLE PRECISION,
  take_profit_3 DOUBLE PRECISION,
  higher_tf_bias VARCHAR(32) NOT NULL,
  aligned_timeframes JSONB NOT NULL,
  invalidation_rule TEXT NOT NULL,
  news_summary TEXT NOT NULL,
  rejection_reason TEXT,
  raw_context JSONB NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
