from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.conversation import Conversation as ConversationModel, Message as MessageModel
from app.schemas.conversation import (
    Conversation,
    ConversationCreate,
    ConversationUpdate,
    Message,
    ChatRequest,
    ChatResponse,
    PaginatedResponse,
)
from app.services.ollama import ollama_service

router = APIRouter()


@router.get("/conversations", response_model=PaginatedResponse)
def list_conversations(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    """List all conversations with pagination"""
    skip = (page - 1) * page_size
    
    conversations = db.query(ConversationModel)\
        .order_by(ConversationModel.updated_at.desc())\
        .offset(skip)\
        .limit(page_size)\
        .all()
    
    total = db.query(ConversationModel).count()
    
    # Add message count to each conversation
    items = []
    for conv in conversations:
        conv_dict = {
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at,
            "message_count": len(conv.messages)
        }
        items.append(Conversation(**conv_dict))
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/conversations/{conversation_id}", response_model=Conversation)
def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Get a specific conversation"""
    conversation = db.query(ConversationModel).filter(
        ConversationModel.id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return Conversation(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=len(conversation.messages)
    )


@router.post("/conversations", response_model=Conversation)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db)
):
    """Create a new conversation"""
    db_conversation = ConversationModel(title=conversation.title)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    
    return Conversation(
        id=db_conversation.id,
        title=db_conversation.title,
        created_at=db_conversation.created_at,
        updated_at=db_conversation.updated_at,
        message_count=0
    )


@router.put("/conversations/{conversation_id}", response_model=Conversation)
def update_conversation(
    conversation_id: str,
    conversation: ConversationUpdate,
    db: Session = Depends(get_db)
):
    """Update a conversation"""
    db_conversation = db.query(ConversationModel).filter(
        ConversationModel.id == conversation_id
    ).first()
    
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db_conversation.title = conversation.title
    db.commit()
    db.refresh(db_conversation)
    
    return Conversation(
        id=db_conversation.id,
        title=db_conversation.title,
        created_at=db_conversation.created_at,
        updated_at=db_conversation.updated_at,
        message_count=len(db_conversation.messages)
    )


@router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Delete a conversation"""
    db_conversation = db.query(ConversationModel).filter(
        ConversationModel.id == conversation_id
    ).first()
    
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db.delete(db_conversation)
    db.commit()
    
    return {"message": "Conversation deleted successfully"}


@router.get("/conversations/{conversation_id}/messages", response_model=List[Message])
def list_messages(conversation_id: str, db: Session = Depends(get_db)):
    """List all messages in a conversation"""
    conversation = db.query(ConversationModel).filter(
        ConversationModel.id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(MessageModel).filter(
        MessageModel.conversation_id == conversation_id
    ).order_by(MessageModel.created_at.asc()).all()
    
    return messages


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Send a message and get AI response"""
    # Create or get conversation
    conversation = None
    if request.conversation_id:
        conversation = db.query(ConversationModel).filter(
            ConversationModel.id == request.conversation_id
        ).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        # Create new conversation
        conversation = ConversationModel(title="New Chat")
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    
    # Save user message
    user_message = MessageModel(
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    db.add(user_message)
    db.commit()
    
    # Get conversation history
    messages = db.query(MessageModel).filter(
        MessageModel.conversation_id == conversation.id
    ).order_by(MessageModel.created_at.asc()).all()
    
    # Format messages for Ollama
    ollama_messages = [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]
    
    try:
        # Get AI response
        response = ollama_service.chat(
            messages=ollama_messages,
            model=request.model
        )
        
        assistant_content = response.get("message", {}).get("content", "")
        
        # Save assistant message
        assistant_message = MessageModel(
            conversation_id=conversation.id,
            role="assistant",
            content=assistant_content,
            model=request.model or "llama3.1"
        )
        db.add(assistant_message)
        
        # Update conversation title if it's the first message
        if len(messages) == 1:  # Only user message exists
            # Use first 50 chars of user message as title
            conversation.title = request.message[:50]
        
        db.commit()
        db.refresh(assistant_message)
        
        return ChatResponse(
            message=Message(
                id=assistant_message.id,
                conversation_id=assistant_message.conversation_id,
                role=assistant_message.role,
                content=assistant_message.content,
                model=assistant_message.model,
                created_at=assistant_message.created_at
            ),
            conversation=Conversation(
                id=conversation.id,
                title=conversation.title,
                created_at=conversation.created_at,
                updated_at=conversation.updated_at,
                message_count=len(conversation.messages)
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")
