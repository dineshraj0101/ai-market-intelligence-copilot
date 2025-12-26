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