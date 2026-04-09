from fastapi import APIRouter

from app.schemas.setup import ScanResponse
from app.services.scanner import ScannerService

router = APIRouter(prefix="/v1")
scanner = ScannerService()

DEFAULT_STRATEGY = {
    "name": "ICT_SMC_Continuation_v1",
    "required_confluences": [
        "liquidity_sweep",
        "bos",
        "fvg",
        "order_block",
        "session_liquidity",
    ],
    "weights": {
        "liquidity_sweep": 1.4,
        "bos": 1.2,
        "mss": 1.0,
        "fvg": 1.2,
        "order_block": 1.1,
        "session_liquidity": 0.8,
        "premium_discount": 0.8,
    },
    "risk": {
        "min_rr": 1.8,
        "pre_news_safety_window_minutes": 120,
    },
}


@router.get("/scan", response_model=ScanResponse)
def scan_markets() -> ScanResponse:
    return scanner.scan(DEFAULT_STRATEGY)


@router.post("/scan", response_model=ScanResponse)
def scan_markets_custom(strategy: dict) -> ScanResponse:
    return scanner.scan(strategy)
