import os
from fastapi import FastAPI
from supabase import create_client, Client

app = FastAPI()

# Read Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client | None = None

if SUPABASE_URL and SUPABASE_ANON_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


@app.get("/")
def root():
    return {"message": "AI Market Intelligence Copilot API"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/supabase-check")
def supabase_check():
    if supabase is None:
        return {
            "ok": False,
            "message": "Supabase client not initialized"
        }

    return {
        "ok": True,
        "message": "Supabase client initialized"
    }


@app.get("/supabase-ping")
def supabase_ping():
    if supabase is None:
        return {
            "ok": False,
            "message": "Supabase client not initialized"
        }

    try:
        # This validates API key + connectivity (no tables needed)
        supabase.auth.get_user()
        return {
            "ok": True,
            "message": "Supabase reachable (auth endpoint ok)"
        }
    except Exception as e:
        return {
            "ok": False,
            "message": "Supabase ping failed",
            "error": str(e)
        }

@app.get("/env-check")
def env_check():
    return {
        "SUPABASE_URL_set": bool(SUPABASE_URL),
        "SUPABASE_ANON_KEY_set": bool(SUPABASE_ANON_KEY),
    }
@app.get("/api/v1/status")
def api_status():
    return {
        "service": "ai-market-intelligence-copilot",
        "version": "v1",
        "status": "ready"
    }

