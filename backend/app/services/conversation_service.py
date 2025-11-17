from typing import List, Optional, Dict, Any
from app.repositories.conversation_repository import ConversationRepository
from app.services.ollama import ollama_service
from app.schemas.conversation import (
    Conversation,
    ConversationCreate,
    ConversationUpdate,
    Message,
    ChatRequest,
    ChatResponse,
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
    
    def list_messages(self, conversation_id: str) -> Optional[List[Message]]:
        """List all messages in a conversation"""
        # Verify conversation exists
        if not self.repository.get_conversation_by_id(conversation_id):
            return None
        
        messages = self.repository.get_messages_by_conversation(conversation_id)
        return [Message(
            id=msg.id,
            conversation_id=msg.conversation_id,
            role=msg.role,
            content=msg.content,
            model=msg.model,
            created_at=msg.created_at
        ) for msg in messages]
    
    def chat(self, request: ChatRequest) -> ChatResponse:
        """Handle chat request with AI"""
        # Get or create conversation
        conversation = None
        if request.conversation_id:
            conversation = self.repository.get_conversation_by_id(request.conversation_id)
            if not conversation:
                raise ValueError("Conversation not found")
        else:
            # Create new conversation
            conversation = self.repository.create_conversation(title="New Chat")
        
        # Save user message
        user_message = self.repository.create_message(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        
        # Get conversation history
        messages = self.repository.get_messages_by_conversation(conversation.id)
        
        # Format messages for Ollama
        ollama_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Get AI response
        response = ollama_service.chat(
            messages=ollama_messages,
            model=request.model
        )
        
        assistant_content = response.get("message", {}).get("content", "")
        
        # Save assistant message
        assistant_message = self.repository.create_message(
            conversation_id=conversation.id,
            role="assistant",
            content=assistant_content,
            model=request.model or "llama3.1:8b"
        )
        
        # Update conversation title if it's the first exchange
        if len(messages) == 1:  # Only user message exists
            conversation = self.repository.update_conversation(
                conversation.id,
                request.message[:50]
            )
        
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
