from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


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


class PaginatedResponse(BaseModel):
    items: List[Conversation]
    total: int
    page: int
    page_size: int
