from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.conversation_model import Conversation


class ConversationRepository:
    """Repository for conversation database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_conversations(self, skip: int = 0, limit: int = 20) -> List[Conversation]:
        """Get all conversations with pagination"""
        return self.db.query(Conversation)\
            .order_by(Conversation.updated_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def count_conversations(self) -> int:
        """Count total conversations"""
        return self.db.query(Conversation).count()
    
    def get_conversation_by_id(self, conversation_id: str) -> Optional[Conversation]:
        """Get a conversation by ID"""
        return self.db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
    
    def create_conversation(self, title: str) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(title=title)
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation
    
    def update_conversation(self, conversation_id: str, title: str) -> Optional[Conversation]:
        """Update a conversation title"""
        conversation = self.get_conversation_by_id(conversation_id)
        if not conversation:
            return None
        
        conversation.title = title
        self.db.commit()
        self.db.refresh(conversation)
        return conversation
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        conversation = self.get_conversation_by_id(conversation_id)
        if not conversation:
            return False
        
        self.db.delete(conversation)
        self.db.commit()
        return True
