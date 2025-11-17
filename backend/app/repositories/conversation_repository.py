from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.conversation import Conversation, Message


class ConversationRepository:
    """Repository for conversation and message database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Conversation CRUD operations
    
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
    
    # Message CRUD operations
    
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
