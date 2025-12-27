import os
import re
import requests
from typing import List, Optional, Literal

from fastapi import FastAPI, Body
from pydantic import BaseModel
from supabase import create_client, Client

from routers.status import router as status_router
from routers.stocks import router as stocks_router

# --------------------------------------------------
# App init
# --------------------------------------------------

app = FastAPI()

# --------------------------------------------------
# Supabase setup
# --------------------------------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client | None = None

if SUPABASE_URL and SUPABASE_ANON_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# --------------------------------------------------
# Polygon setup (STEP 3.1)
# --------------------------------------------------

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
POLYGON_SEARCH_URL = "https://api.polygon.io/v3/reference/tickers"

TICKER_REGEX = re.compile(r"^[A-Z]{1,5}(\.[A-Z]{1,2})?$")

# --------------------------------------------------
# Health & base routes
# --------------------------------------------------

@app.get("/")
def root():
    return {"message": "AI Market Intelligence Copilot API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/env-check")
def env_check():
    return {
        "SUPABASE_URL_set": bool(SUPABASE_URL),
        "SUPABASE_ANON_KEY_set": bool(SUPABASE_ANON_KEY),
        "POLYGON_API_KEY_set": bool(POLYGON_API_KEY),
    }

@app.get("/supabase-check")
def supabase_check():
    if supabase is None:
        return {"ok": False, "message": "Supabase client not initialized"}
    return {"ok": True, "message": "Supabase client initialized"}

# --------------------------------------------------
# STEP 3.1 – Ticker / Company Name Validation
# --------------------------------------------------

class ValidateTickerRequest(BaseModel):
    ticker: str

class ErrorItem(BaseModel):
    code: str
    message: str

class SuggestionItem(BaseModel):
    symbol: str
    name: str
    exchange: Optional[str]
    currency: str = "USD"

class Field(BaseModel):
    value: Optional[str]
    missing: bool

class TickerBlock(BaseModel):
    input: str
    normalized: Optional[str]
    is_valid_format: bool
    asset_scope_allowed: bool
    asset_type: Field
    exchange: Field
    currency: Field
    name: Field
    validation_status: Literal["PASS", "FAIL", "NEEDS_LOOKUP"]
    errors: List[ErrorItem]
    suggestions: List[SuggestionItem]

class ValidateTickerResponse(BaseModel):
    ticker: TickerBlock

def search_company_name(name: str) -> List[SuggestionItem]:
    if not POLYGON_API_KEY:
        return []

    params = {
        "search": name,
        "market": "stocks",
        "active": "true",
        "limit": 10,
        "apiKey": POLYGON_API_KEY,
    }

    r = requests.get(POLYGON_SEARCH_URL, params=params, timeout=5)
    r.raise_for_status()
    data = r.json()

    results = []
    for item in data.get("results", []):
        if item.get("locale") == "us":
            results.append(
                SuggestionItem(
                    symbol=item.get("ticker"),
                    name=item.get("name"),
                    exchange=item.get("primary_exchange"),
                )
            )
    return results

@app.post("/api/v1/ticker/validate", response_model=ValidateTickerResponse)
def validate_ticker(payload: ValidateTickerRequest = Body(...)):
    raw = payload.ticker.strip()

    # Empty input
    if raw == "":
        return ValidateTickerResponse(
            ticker=TickerBlock(
                input=raw,
                normalized=None,
                is_valid_format=False,
                asset_scope_allowed=False,
                asset_type=Field(value=None, missing=True),
                exchange=Field(value=None, missing=True),
                currency=Field(value="USD", missing=False),
                name=Field(value=None, missing=True),
                validation_status="FAIL",
                errors=[ErrorItem(code="EMPTY", message="Ticker or company name required")],
                suggestions=[]
            )
        )

    upper = raw.upper()

    # Looks like a ticker
    if TICKER_REGEX.match(upper):
        return ValidateTickerResponse(
            ticker=TickerBlock(
                input=raw,
                normalized=upper,
                is_valid_format=True,
                asset_scope_allowed=True,
                asset_type=Field(value="EQUITY", missing=False),
                exchange=Field(value=None, missing=True),
                currency=Field(value="USD", missing=False),
                name=Field(value=None, missing=True),
                validation_status="PASS",
                errors=[],
                suggestions=[]
            )
        )

    # Otherwise treat as company name
    suggestions = search_company_name(raw)

    return ValidateTickerResponse(
        ticker=TickerBlock(
            input=raw,
            normalized=None,
            is_valid_format=False,
            asset_scope_allowed=False,
            asset_type=Field(value=None, missing=True),
            exchange=Field(value=None, missing=True),
            currency=Field(value="USD", missing=False),
            name=Field(value=None, missing=True),
            validation_status="NEEDS_LOOKUP" if suggestions else "FAIL",
            errors=[
                ErrorItem(code="NAME_LOOKUP", message="Select a ticker from suggestions")
            ] if suggestions else [
                ErrorItem(code="NOT_FOUND", message="No US-listed company found")
            ],
            suggestions=suggestions
        )
    )

# --------------------------------------------------
# Include routers (existing)
# --------------------------------------------------

app.include_router(status_router)
app.include_router(stocks_router)