from fastapi import APIRouter, Request
from app.services.telegram_bot import handle_update
from app.config import settings

router = APIRouter()

@router.post("/telegram")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        handle_update(update)
    except Exception as e:
        print(f"Webhook error: {e}")
    return {"ok": True}

@router.get("/telegram/health")
def telegram_health():
    return {"status": "ready"}