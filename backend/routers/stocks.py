from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/stocks",
    tags=["stocks"]
)

@router.get("/{ticker}/meta")
def stock_meta(ticker: str):
    normalized_ticker = ticker.upper()

    return {
        "asset_class": "stocks",
        "ticker": ticker,
        "normalized_ticker": normalized_ticker,
        "exchange": "US",
        "status": "ok"
    }