from fastapi import APIRouter

router = APIRouter()

chat_sessions = {}

@router.post("/api/chat/session")
def start_chat_session(client_id: str):
    """
    Start a new chat session.
    """
    if client_id not in chat_sessions:
        chat_sessions[client_id] = []
    return {"message": f"Chat session started for client {client_id}"}

@router.get("/api/chat/history")
def get_chat_history(client_id: str):
    """
    Retrieve the chat history for a client.
    """
    if client_id not in chat_sessions:
        return {"error": "Chat session not found for client"}, 404

    return {"chat_history": chat_sessions[client_id]}
