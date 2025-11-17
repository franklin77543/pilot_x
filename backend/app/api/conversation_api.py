from fastapi import APIRouter, Depends, HTTPException
from app.schemas.conversation_schema import (
    Conversation,
    ConversationCreate,
    ConversationUpdate,
    PaginatedResponse,
)
from app.services.conversation_service import ConversationService
from app.dependencies import get_conversation_service

router = APIRouter()


@router.get("/conversations", response_model=PaginatedResponse)
def list_conversations(
    page: int = 1,
    page_size: int = 20,
    service: ConversationService = Depends(get_conversation_service)
):
    """List all conversations with pagination"""
    result = service.list_conversations(page=page, page_size=page_size)
    return PaginatedResponse(**result)


@router.get("/conversations/{conversation_id}", response_model=Conversation)
def get_conversation(
    conversation_id: str,
    service: ConversationService = Depends(get_conversation_service)
):
    """Get a specific conversation"""
    conversation = service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post("/conversations", response_model=Conversation)
def create_conversation(
    conversation: ConversationCreate,
    service: ConversationService = Depends(get_conversation_service)
):
    """Create a new conversation"""
    return service.create_conversation(conversation)


@router.put("/conversations/{conversation_id}", response_model=Conversation)
def update_conversation(
    conversation_id: str,
    conversation: ConversationUpdate,
    service: ConversationService = Depends(get_conversation_service)
):
    """Update a conversation"""
    result = service.update_conversation(conversation_id, conversation)
    if not result:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return result


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    service: ConversationService = Depends(get_conversation_service)
):
    """Delete a conversation"""
    success = service.delete_conversation(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"message": "Conversation deleted successfully"}
