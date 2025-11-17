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
