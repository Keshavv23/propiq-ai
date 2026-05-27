import httpx
from app.config import settings
from app.services.ai_agent import PropIQAgent

TELEGRAM_API = f"https://api.telegram.org/bot{settings.telegram_bot_token}"

# store one agent per telegram user
user_sessions: dict[int, PropIQAgent] = {}


def send_message(chat_id: int, text: str):
    """Send a message to a Telegram user."""
    httpx.post(
        f"{TELEGRAM_API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
        },
        timeout=10,
    )


def send_listings(chat_id: int, listings: list):
    """Send matched listings as formatted messages."""
    if not listings:
        return
    msg = "🏠 *Here are matching properties:*\n\n"
    for i, l in enumerate(listings[:3], 1):
        price_l = l["price"] / 100000
        msg += (
            f"*{i}. {l['title']}*\n"
            f"📍 {l['locality']}, {l['city']}\n"
            f"💰 ₹{price_l:.1f} Lakhs\n"
            f"🛏 {l['bedrooms']} BHK | 📐 {l['area_sqft']} sqft\n\n"
        )
    send_message(chat_id, msg)


def handle_update(update: dict):
    """Process an incoming Telegram update."""
    message = update.get("message")
    if not message:
        return

    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()

    if not text:
        return

    # handle /start command
    if text == "/start":
        user_sessions.pop(chat_id, None)
        send_message(
            chat_id,
            "👋 Welcome to *PropIQ AI* — your intelligent property assistant!\n\n"
            "I'll help you find the perfect property in India. "
            "Just tell me what you're looking for and I'll guide you through it.\n\n"
            "So, which city are you looking to buy in? 🏙️"
        )
        return

    # handle /reset command
    if text == "/reset":
        user_sessions.pop(chat_id, None)
        send_message(chat_id, "🔄 Conversation reset. Send /start to begin again.")
        return

    # get or create agent for this user
    if chat_id not in user_sessions:
        user_sessions[chat_id] = PropIQAgent()

    agent = user_sessions[chat_id]

    # typing indicator
    httpx.post(
        f"{TELEGRAM_API}/sendChatAction",
        json={"chat_id": chat_id, "action": "typing"},
        timeout=5,
    )

    # get AI response
    result = agent.chat(text)

    # send the message
    send_message(chat_id, result["message"])

    # send listings if found
    if result.get("listings"):
        send_listings(chat_id, result["listings"])

    # send lead confirmation if saved
    if result.get("lead_saved"):
        lead = result["lead_saved"]
        emoji = "🟢" if lead["qualified"] else "🟡"
        send_message(
            chat_id,
            f"{emoji} *Your details have been saved!*\n"
            f"Lead score: *{lead['score']:.0f}/100*\n"
            f"An agent will contact you shortly. 📞"
        )