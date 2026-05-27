from fastapi import APIRouter, Request, HTTPException
from app.services.telegram_bot import handle_update
from app.config import settings

router = APIRouter()

@router.post("/telegram")
async def telegram_webhook(request: Request):
    """Receive updates from Telegram."""
    try:
        update = await request.json()
        handle_update(update)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/telegram/health")
def telegram_health():
    token_set = bool(settings.telegram_bot_token and
                     settings.telegram_bot_token != "your-bot-token")
    return {
        "telegram_configured": token_set,
        "status": "ready" if token_set else "token not set"
    }