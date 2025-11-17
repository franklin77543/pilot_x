from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Conversation Schemas
class ConversationBase(BaseModel):
    title: Optional[str] = "New Conversation"


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(BaseModel):
    title: str


class Conversation(ConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    
    class Config:
        from_attributes = True


# Message Schemas
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


# Chat Schemas
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    model: Optional[str] = None


class ChatResponse(BaseModel):
    message: Message
    conversation: Conversation


# Pagination
class PaginatedResponse(BaseModel):
    items: List[Conversation]
    total: int
    page: int
    page_size: int
