import requests
from typing import Optional, Dict, Any
from app.core.config import settings


class OllamaService:
    """Service for interacting with Ollama API"""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.default_model = settings.OLLAMA_MODEL
    
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a response from Ollama
        
        Args:
            prompt: The prompt to send to the model
            model: The model to use (defaults to settings.OLLAMA_MODEL)
            stream: Whether to stream the response
            **kwargs: Additional parameters to pass to Ollama
        
        Returns:
            Response from Ollama API
        """
        url = f"{self.base_url}/api/generate"
        model_name = model or self.default_model
        
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": stream,
            **kwargs
        }
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    def chat(
        self,
        messages: list[Dict[str, str]],
        model: Optional[str] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Chat with Ollama using conversation history
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: The model to use (defaults to settings.OLLAMA_MODEL)
            stream: Whether to stream the response
            **kwargs: Additional parameters to pass to Ollama
        
        Returns:
            Response from Ollama API
        """
        url = f"{self.base_url}/api/chat"
        model_name = model or self.default_model
        
        payload = {
            "model": model_name,
            "messages": messages,
            "stream": stream,
            **kwargs
        }
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    def list_models(self) -> Dict[str, Any]:
        """List available models in Ollama"""
        url = f"{self.base_url}/api/tags"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API error: {str(e)}")


# Singleton instance
ollama_service = OllamaService()
