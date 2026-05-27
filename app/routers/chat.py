from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ai_agent import PropIQAgent

router = APIRouter()

# in-memory session store (good enough for now)
sessions: dict[str, PropIQAgent] = {}


class ChatMessage(BaseModel):
    session_id: str
    message: str


@router.post("/")
def chat(data: ChatMessage):
    # get or create session
    if data.session_id not in sessions:
        sessions[data.session_id] = PropIQAgent()

    agent = sessions[data.session_id]
    result = agent.chat(data.message)
    return result


@router.delete("/{session_id}")
def clear_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
    return {"message": "Session cleared"}


@router.get("/{session_id}/history")
def get_history(session_id: str):
    if session_id not in sessions:
        return {"history": []}
    agent = sessions[session_id]
    return {"history": agent.conversation_history}