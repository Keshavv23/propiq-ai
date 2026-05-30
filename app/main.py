from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import listings, agencies, leads, chat, search, webhook

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not create tables: {e}")

app = FastAPI(title="PropIQ AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://propiq-ai-eta.vercel.app",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(listings.router, prefix="/listings", tags=["listings"])
app.include_router(agencies.router, prefix="/agencies", tags=["agencies"])
app.include_router(leads.router, prefix="/leads", tags=["leads"])
app.include_router(chat.router, prefix="/chat", tags=["ai-agent"])
app.include_router(search.router, prefix="/search", tags=["semantic-search"])
app.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
@app.get("/health")
def health():
    return {"status": "ok", "service": "PropIQ AI"}