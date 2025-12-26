from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["status"]
)

@router.get("/status")
def api_status():
    return {
        "service": "ai-market-intelligence-copilot",
        "version": "v1",
        "status": "ready"
    }