from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from app.schemas.message_schema import Message
from app.services.message_service import MessageService
from app.dependencies import get_message_service

router = APIRouter()


class SendMessageRequest(BaseModel):
    content: str
    model: str | None = None


@router.get("/conversations/{conversation_id}/messages", response_model=List[Message])
def list_messages(
    conversation_id: str,
    service: MessageService = Depends(get_message_service)
):
    """List all messages in a conversation"""
    messages = service.list_messages(conversation_id)
    if messages is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return messages


@router.post("/conversations/{conversation_id}/messages", response_model=Message)
def send_message(
    conversation_id: str,
    request: SendMessageRequest,
    service: MessageService = Depends(get_message_service)
):
    """Send a message and get AI response"""
    try:
        return service.send_message(
            conversation_id=conversation_id,
            message_content=request.content,
            model=request.model
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")
