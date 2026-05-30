from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.config import settings
from app.database import SessionLocal
from app.models.orm import Listing, Lead
import json

# ── LLM setup ────────────────────────────────────────────────
_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGroq(
            api_key=settings.groq_api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.4,
        )
    return _llm

SYSTEM_PROMPT = """You are PropIQ, an intelligent real estate assistant for the Indian property market.
Your job is to help buyers find the right property by having a natural conversation.

You need to collect these details from the buyer:
1. City they want to buy in (Mumbai, Pune, Bangalore, Indore etc)
2. Property type (flat, villa, plot, commercial)
3. Number of bedrooms (1BHK, 2BHK, 3BHK, 4BHK)
4. Budget range (in rupees - understand lakhs and crores)
5. Timeline (immediate, 3 months, 6 months, or just exploring)
6. Their name and phone number (collect this last, naturally)

Rules:
- Be conversational and friendly, like a helpful agent
- Understand Indian real estate terms (BHK, lakh, crore, society, flat, plot)
- Ask one or two questions at a time, not all at once
- Once you have all details, output a special JSON block like this:
  <LEAD_DATA>{"name":"...","phone":"...","city":"...","property_type":"...","bedrooms":2,"budget_min":3000000,"budget_max":6000000,"timeline":"immediate"}</LEAD_DATA>
- Convert lakhs to rupees (50 lakhs = 5000000, 1 crore = 10000000)
- Only output the LEAD_DATA block when you have name, phone, city, and budget
- Keep responses short and natural, max 3 sentences
- Always respond in English unless user writes in Hindi"""


def parse_lead_data(response_text: str) -> dict | None:
    """Extract lead data from AI response if present."""
    if "<LEAD_DATA>" in response_text and "</LEAD_DATA>" in response_text:
        start = response_text.index("<LEAD_DATA>") + len("<LEAD_DATA>")
        end = response_text.index("</LEAD_DATA>")
        try:
            return json.loads(response_text[start:end])
        except json.JSONDecodeError:
            return None
    return None


def search_listings(city: str = None, property_type: str = None,
                    bedrooms: int = None, budget_min: float = None,
                    budget_max: float = None, limit: int = 5) -> list:
    """Search listings based on lead preferences."""
    db = SessionLocal()
    try:
        q = db.query(Listing).filter(Listing.is_active == True)
        if city:
            q = q.filter(Listing.city.ilike(f"%{city}%"))
        if property_type:
            q = q.filter(Listing.property_type == property_type)
        if bedrooms:
            q = q.filter(Listing.bedrooms == bedrooms)
        if budget_min:
            q = q.filter(Listing.price >= budget_min)
        if budget_max:
            q = q.filter(Listing.price <= budget_max)
        results = q.limit(limit).all()
        return [
            {
                "id": str(r.id),
                "title": r.title,
                "city": r.city,
                "locality": r.locality,
                "price": r.price,
                "bedrooms": r.bedrooms,
                "area_sqft": r.area_sqft,
                "property_type": r.property_type,
            }
            for r in results
        ]
    finally:
        db.close()


def format_price(price: float) -> str:
    """Convert rupees to readable format."""
    if price >= 10000000:
        return f"₹{price/10000000:.1f} Cr"
    elif price >= 100000:
        return f"₹{price/100000:.1f} L"
    return f"₹{price:,.0f}"


def save_lead(lead_data: dict, listing_id: str = None) -> dict:
    """Save lead to database with auto scoring."""
    db = SessionLocal()
    try:
        score = 0.0
        timeline = lead_data.get("timeline", "exploring")
        if timeline == "immediate":
            score += 40
        elif timeline == "3months":
            score += 25
        elif timeline == "6months":
            score += 10

        if lead_data.get("budget_min") and lead_data.get("budget_max"):
            score += 30
        elif lead_data.get("budget_max"):
            score += 15

        if lead_data.get("phone"):
            score += 20
        if lead_data.get("email"):
            score += 10

        lead = Lead(
            listing_id=listing_id,
            name=lead_data.get("name"),
            phone=lead_data.get("phone"),
            email=lead_data.get("email"),
            budget_min=lead_data.get("budget_min"),
            budget_max=lead_data.get("budget_max"),
            timeline=timeline,
            score=score,
            qualified=score >= 50,
            notes=f"AI collected: city={lead_data.get('city')}, "
                  f"type={lead_data.get('property_type')}, "
                  f"bedrooms={lead_data.get('bedrooms')}",
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)
        return {"id": str(lead.id), "score": score, "qualified": lead.qualified}
    finally:
        db.close()


class PropIQAgent:
    """Conversational AI agent for PropIQ."""

    def __init__(self):
        self.conversation_history: list = []
        self.lead_collected = False
        self.lead_id = None

    def chat(self, user_message: str) -> dict:
        """Process a user message and return agent response."""

        # build message list
        messages = [SystemMessage(content=SYSTEM_PROMPT)]
        for msg in self.conversation_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        messages.append(HumanMessage(content=user_message))

        # call Groq
        response = get_llm().invoke(messages)
        response_text = response.content

        # save to history
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": response_text})

        # check if lead data was collected
        lead_data = parse_lead_data(response_text)
        listings = []
        lead_saved = None

        if lead_data and not self.lead_collected:
            self.lead_collected = True

            # search matching listings
            listings = search_listings(
                city=lead_data.get("city"),
                property_type=lead_data.get("property_type"),
                bedrooms=lead_data.get("bedrooms"),
                budget_min=lead_data.get("budget_min"),
                budget_max=lead_data.get("budget_max"),
            )

            # save lead, link to first matching listing if found
            listing_id = listings[0]["id"] if listings else None
            lead_saved = save_lead(lead_data, listing_id)
            self.lead_id = lead_saved["id"]

            # clean response — remove the JSON block from display
            clean_response = response_text.replace(
                response_text[response_text.index("<LEAD_DATA>"):
                              response_text.index("</LEAD_DATA>") + len("</LEAD_DATA>")],
                ""
            ).strip()
        else:
            clean_response = response_text

        return {
            "message": clean_response,
            "listings": listings,
            "lead_saved": lead_saved,
            "turn": len(self.conversation_history) // 2,
        }
