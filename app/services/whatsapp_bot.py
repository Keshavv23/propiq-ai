import httpx
from app.config import settings
from app.services.ai_agent import PropIQAgent

WHATSAPP_API = "https://graph.facebook.com/v18.0"

user_sessions: dict[str, PropIQAgent] = {}


def send_whatsapp_message(to: str, text: str):
    url = f"{WHATSAPP_API}/{settings.whatsapp_phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {settings.whatsapp_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    try:
        httpx.post(url, json=payload, headers=headers, timeout=10)
    except Exception as e:
        print(f"WhatsApp send error: {e}")


def send_whatsapp_listings(to: str, listings: list):
    if not listings:
        return
    msg = "🏠 *Matching Properties:*\n\n"
    for i, l in enumerate(listings[:3], 1):
        price_l = l["price"] / 100000
        msg += (
            f"*{i}. {l['title']}*\n"
            f"📍 {l['locality']}, {l['city']}\n"
            f"💰 ₹{price_l:.1f} Lakhs\n"
            f"🛏 {l['bedrooms']} BHK | 📐 {l['area_sqft']} sqft\n\n"
        )
    send_whatsapp_message(to, msg)


def handle_whatsapp_message(phone: str, text: str):
    text = text.strip()

    if text.lower() in ["/start", "hi", "hello", "helo", "start"]:
        user_sessions.pop(phone, None)
        send_whatsapp_message(
            phone,
            "👋 Welcome to *PropIQ AI* — your intelligent property assistant!\n\n"
            "I'll help you find the perfect property in India. "
            "Just tell me what you're looking for!\n\n"
            "So, which city are you looking to buy in? 🏙️"
        )
        return

    if phone not in user_sessions:
        user_sessions[phone] = PropIQAgent()

    agent = user_sessions[phone]
    result = agent.chat(text)

    send_whatsapp_message(phone, result["message"])

    if result.get("listings"):
        send_whatsapp_listings(phone, result["listings"])

    if result.get("lead_saved"):
        lead = result["lead_saved"]
        emoji = "🟢" if lead["qualified"] else "🟡"
        send_whatsapp_message(
            phone,
            f"{emoji} *Your details have been saved!*\n"
            f"Lead score: *{lead['score']:.0f}/100*\n"
            f"An agent will contact you shortly. 📞"
        )