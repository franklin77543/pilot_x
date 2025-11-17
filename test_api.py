"""
Quick test script for PilotX API
Tests basic functionality without closing the server
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test health endpoint"""
    response = requests.get("http://localhost:8000/health")
    print(f"✅ Health Check: {response.json()}")
    return response.status_code == 200

def test_create_conversation():
    """Test creating a conversation"""
    response = requests.post(f"{BASE_URL}/conversations", json={"title": "Test Chat"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Created Conversation: {data['id']} - {data['title']}")
        return data['id']
    else:
        print(f"❌ Failed to create conversation: {response.text}")
        return None

def test_list_conversations():
    """Test listing conversations"""
    response = requests.get(f"{BASE_URL}/conversations")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Listed {len(data['items'])} conversations")
        return True
    else:
        print(f"❌ Failed to list conversations: {response.text}")
        return False

def test_chat(conversation_id=None):
    """Test sending a chat message"""
    payload = {
        "message": "Hello! Can you tell me what is 2+2?",
        "conversation_id": conversation_id
    }
    
    print(f"📤 Sending message to Ollama...")
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Chat Response:")
        print(f"   Conversation: {data['conversation']['id']}")
        print(f"   Message: {data['message']['content'][:100]}...")
        return data['conversation']['id']
    else:
        print(f"❌ Failed to send chat: {response.text}")
        return None

if __name__ == "__main__":
    print("🧪 Testing PilotX API...\n")
    
    # Test health
    if not test_health():
        print("❌ Health check failed!")
        exit(1)
    
    print()
    
    # Test list conversations
    test_list_conversations()
    
    print()
    
    # Test create conversation
    conv_id = test_create_conversation()
    
    print()
    
    # Test chat
    if conv_id:
        test_chat(conv_id)
    else:
        # Create new conversation via chat
        test_chat()
    
    print()
    print("✅ All tests completed!")
