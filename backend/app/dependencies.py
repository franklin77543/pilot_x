"""FastAPI dependencies for dependency injection"""
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db
from app.repositories.conversation_repository import ConversationRepository
from app.services.conversation_service import ConversationService


def get_conversation_repository(db: Session = Depends(get_db)) -> ConversationRepository:
    """Dependency injection for conversation repository"""
    return ConversationRepository(db)


def get_conversation_service(
    repository: ConversationRepository = Depends(get_conversation_repository)
) -> ConversationService:
    """Dependency injection for conversation service"""
    return ConversationService(repository)
