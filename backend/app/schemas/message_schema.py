from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageBase(BaseModel):
    content: str
    role: str
    model: Optional[str] = None


class MessageCreate(MessageBase):
    conversation_id: Optional[str] = None


class Message(MessageBase):
    id: str
    conversation_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    model: Optional[str] = None


class ChatResponse(BaseModel):
    message: Message
    conversation: "Conversation"  # Forward reference
    
    class Config:
        from_attributes = True


# Import for forward reference
from app.schemas.conversation_schema import Conversation
ChatResponse.model_rebuild()
