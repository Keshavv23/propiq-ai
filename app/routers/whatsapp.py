@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    try:
        body = await request.body()
        if not body:
            return {"status": "ok"}
        data = await request.json()
        entry = data.get("entry", [])
        for e in entry:
            for change in e.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                for msg in messages:
                    if msg.get("type") == "text":
                        phone = msg["from"]
                        text = msg["text"]["body"]
                        print(f"WhatsApp message from {phone}: {text}")
                        handle_whatsapp_message(phone, text)
    except Exception as ex:
        print(f"WhatsApp webhook error: {ex}")
    return {"status": "ok"}