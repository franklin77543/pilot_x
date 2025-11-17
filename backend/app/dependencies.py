"""FastAPI dependencies for dependency injection"""
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService


def get_conversation_repository(db: Session = Depends(get_db)) -> ConversationRepository:
    """Dependency injection for conversation repository"""
    return ConversationRepository(db)


def get_message_repository(db: Session = Depends(get_db)) -> MessageRepository:
    """Dependency injection for message repository"""
    return MessageRepository(db)


def get_conversation_service(
    repository: ConversationRepository = Depends(get_conversation_repository)
) -> ConversationService:
    """Dependency injection for conversation service"""
    return ConversationService(repository)


def get_message_service(
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
    message_repository: MessageRepository = Depends(get_message_repository)
) -> MessageService:
    """Dependency injection for message service"""
    return MessageService(conversation_repository, message_repository)

