from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.message_model import Message


class MessageRepository:
    """Repository for message database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_messages_by_conversation(self, conversation_id: str) -> List[Message]:
        """Get all messages in a conversation"""
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).all()
    
    def create_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        model: Optional[str] = None
    ) -> Message:
        """Create a new message"""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            model=model
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def get_message_count(self, conversation_id: str) -> int:
        """Get message count for a conversation"""
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).count()
