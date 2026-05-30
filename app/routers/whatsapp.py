from fastapi import APIRouter, Request, Query
from fastapi.responses import PlainTextResponse
from app.services.whatsapp_bot import handle_whatsapp_message
from app.config import settings

router = APIRouter()


@router.get("/whatsapp")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token:
        return PlainTextResponse(content=hub_challenge)
    return PlainTextResponse(content="Verification failed", status_code=403)


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    try:
        body = await request.body()
        print(f"Raw body: {body}")
        if not body:
            print("Empty body received")
            return {"status": "ok"}
        import json
        data = json.loads(body)
        print(f"Parsed data: {data}")
        entry = data.get("entry", [])
        for e in entry:
            for change in e.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                for msg in messages:
                    print(f"Processing message: {msg}")
                    if msg.get("type") == "text":
                        phone = msg["from"]
                        text = msg["text"]["body"]
                        print(f"WhatsApp message from {phone}: {text}")
                        handle_whatsapp_message(phone, text)
    except Exception as ex:
        print(f"WhatsApp webhook error: {ex}")
        import traceback
        traceback.print_exc()
    return {"status": "ok"}