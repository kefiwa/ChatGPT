from enum import Enum


class AssetClass(str, Enum):
    FOREX = "forex"
    METAL = "metal"
    CRYPTO = "crypto"


class SetupType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    BUY_LIMIT = "BUY_LIMIT"
    SELL_LIMIT = "SELL_LIMIT"
    NO_TRADE = "NO_TRADE"


class TradeAction(str, Enum):
    EXECUTE = "EXECUTE"
    PLACE_LIMIT_ORDER = "PLACE_LIMIT_ORDER"
    WAIT = "WAIT"
    NO_TRADE = "NO_TRADE"


class EventRisk(str, Enum):
    SAFE_TO_TRADE = "SAFE_TO_TRADE"
    CAUTION = "CAUTION"
    DO_NOT_ENTER_BEFORE_NEWS = "DO_NOT_ENTER_BEFORE_NEWS"


class SetupStatus(str, Enum):
    VALID = "valid"
    INVALIDATED = "invalidated"
    CLOSED = "closed"


class NewsImpact(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
