from typing import List, Optional
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.services.ollama import ollama_service
from app.schemas.conversation_schema import Conversation
from app.schemas.message_schema import (
    Message,
    MessageCreate,
)


class MessageService:
    """Service layer for message business logic"""
    
    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository
    ):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository
    
    def list_messages(self, conversation_id: str) -> Optional[List[Message]]:
        """List all messages in a conversation"""
        # Verify conversation exists
        if not self.conversation_repository.get_conversation_by_id(conversation_id):
            return None
        
        messages = self.message_repository.get_messages_by_conversation(conversation_id)
        return [Message(
            id=msg.id,
            conversation_id=msg.conversation_id,
            role=msg.role,
            content=msg.content,
            model=msg.model,
            created_at=msg.created_at
        ) for msg in messages]
    
    def send_message(self, conversation_id: str, message_content: str, model: Optional[str] = None) -> Message:
        """Send a message and get AI response"""
        # Verify conversation exists
        conversation = self.conversation_repository.get_conversation_by_id(conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        
        # Save user message
        user_message = self.message_repository.create_message(
            conversation_id=conversation.id,
            role="user",
            content=message_content
        )
        
        # Get conversation history
        messages = self.message_repository.get_messages_by_conversation(conversation.id)
        
        # Format messages for Ollama
        ollama_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Get AI response
        response = ollama_service.chat(
            messages=ollama_messages,
            model=model
        )
        
        assistant_content = response.get("message", {}).get("content", "")
        
        # Save assistant message
        assistant_message = self.message_repository.create_message(
            conversation_id=conversation.id,
            role="assistant",
            content=assistant_content,
            model=model or "llama3.1:8b"
        )
        
        # Update conversation title if it's the first exchange
        if len(messages) == 1:  # Only user message exists
            self.conversation_repository.update_conversation(
                conversation.id,
                message_content[:50]
            )
        
        return Message(
            id=assistant_message.id,
            conversation_id=assistant_message.conversation_id,
            role=assistant_message.role,
            content=assistant_message.content,
            model=assistant_message.model,
            created_at=assistant_message.created_at
        )
