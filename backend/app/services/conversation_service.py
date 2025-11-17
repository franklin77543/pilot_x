from typing import List, Optional, Dict, Any
from app.repositories.conversation_repository import ConversationRepository
from app.schemas.conversation_schema import (
    Conversation,
    ConversationCreate,
    ConversationUpdate,
)


class ConversationService:
    """Service layer for conversation business logic"""
    
    def __init__(self, repository: ConversationRepository):
        self.repository = repository
    
    def list_conversations(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """List all conversations with pagination"""
        skip = (page - 1) * page_size
        
        conversations = self.repository.get_conversations(skip=skip, limit=page_size)
        total = self.repository.count_conversations()
        
        # Convert to schema objects
        items = []
        for conv in conversations:
            items.append(Conversation(
                id=conv.id,
                title=conv.title,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                message_count=len(conv.messages)
            ))
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a specific conversation"""
        conv = self.repository.get_conversation_by_id(conversation_id)
        if not conv:
            return None
        
        return Conversation(
            id=conv.id,
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=len(conv.messages)
        )
    
    def create_conversation(self, data: ConversationCreate) -> Conversation:
        """Create a new conversation"""
        conv = self.repository.create_conversation(title=data.title)
        
        return Conversation(
            id=conv.id,
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=0
        )
    
    def update_conversation(
        self,
        conversation_id: str,
        data: ConversationUpdate
    ) -> Optional[Conversation]:
        """Update a conversation"""
        conv = self.repository.update_conversation(conversation_id, data.title)
        if not conv:
            return None
        
        return Conversation(
            id=conv.id,
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=len(conv.messages)
        )
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        return self.repository.delete_conversation(conversation_id)
