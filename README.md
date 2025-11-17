# PilotX - AI Chat Assistant

An AI-powered chat assistant supporting multiple models with local Ollama integration.

## 🚀 Features

- ✅ **Multiple AI Models**: Support for Ollama (Llama 3.1) and future cloud providers
- ✅ **Conversation Management**: Create, rename, delete, and switch between conversations
- ✅ **Markdown Rendering**: Full support for Markdown formatting in messages
- ✅ **Code Highlighting**: Syntax highlighting for code blocks with copy functionality
- ✅ **Modern UI**: Dark theme with VS Code-inspired design system
- ✅ **Local-First**: Run completely offline with Ollama

## 📋 Prerequisites

- **Node.js**: v18+ (for frontend)
- **Python**: v3.10+ (for backend)
- **Ollama**: v0.12+ (for AI model)

## 🛠️ Installation

### 1. Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai)

```powershell
# Download Llama 3.1 (8B) model
ollama pull llama3.1
```

### 2. Setup Backend

```powershell
# Navigate to backend directory
cd backend

# Python environment is already configured
# Install dependencies (if not already installed)
pip install -r requirements.txt

# Create .env file (already exists)
# DATABASE_URL=sqlite:///./pilotx.db
# AI_PROVIDER=ollama
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=llama3.1
```

### 3. Setup Frontend

```powershell
# Navigate to frontend directory
cd frontend

# Dependencies are already installed
# npm install

# Create .env file (already exists)
# VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 🚦 Running the Application

### Start All Services

**Terminal 1 - Ollama (if not already running):**
```powershell
ollama serve
```

**Terminal 2 - Backend:**
```powershell
cd backend
E:/My_Repo/Github/20251117_PilotX/backend/venv/Scripts/python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 3 - Frontend:**
```powershell
cd frontend
npm run dev
```

### Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Ollama**: http://localhost:11434

## 📁 Project Structure

```
PilotX/
├── frontend/                 # React + TypeScript + Vite
│   ├── src/
│   │   ├── components/      # Sidebar, Message, MessageList, ChatInput
│   │   ├── pages/           # ChatPage
│   │   ├── services/        # API client
│   │   ├── store/           # Zustand state management
│   │   ├── types/           # TypeScript types
│   │   └── index.css        # Tailwind CSS + Design system
│   └── package.json
│
├── backend/                  # FastAPI + SQLAlchemy (Layered Architecture)
│   ├── app/
│   │   ├── models/          # Model Layer - Database ORM models
│   │   │   ├── conversation_model.py
│   │   │   └── message_model.py
│   │   ├── repositories/    # Repository Layer - Database operations
│   │   │   ├── conversation_repository.py
│   │   │   └── message_repository.py
│   │   ├── services/        # Service Layer - Business logic
│   │   │   ├── conversation_service.py
│   │   │   ├── message_service.py
│   │   │   └── ollama.py
│   │   ├── api/             # API Layer - HTTP endpoints
│   │   │   ├── conversation_api.py
│   │   │   └── message_api.py
│   │   ├── core/            # Config settings
│   │   ├── db/              # Database session
│   │   ├── schemas/         # Pydantic schemas
│   │   │   ├── conversation_schema.py
│   │   │   └── message_schema.py
│   │   ├── dependencies.py  # Dependency injection
│   │   └── main.py          # FastAPI app
│   ├── requirements.txt
│   └── .env
│
├── prototype/                # Static HTML/CSS/JS prototype
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
└── Documentation/
    ├── SPEC.md              # Complete project specification
    ├── USER_STORIES.md      # User stories and requirements
    ├── UI_UX_SPEC.md        # Design system specification
    └── AI_MODEL.md          # Ollama setup guide
```

## 🎯 Usage

1. **Start a New Chat**: Click the "New Chat" button in the sidebar
2. **Send a Message**: Type your message and press Enter (Shift+Enter for new line)
3. **View Response**: AI response appears with Markdown and code highlighting
4. **Manage Conversations**: 
   - Click on a conversation to switch to it
   - Hover and click Edit to rename
   - Hover and click Delete to remove
5. **Copy Code**: Hover over code blocks and click the copy button

## 🔧 API Endpoints

### Conversations
- `GET /api/v1/conversations` - List all conversations
- `GET /api/v1/conversations/{id}` - Get specific conversation
- `POST /api/v1/conversations` - Create new conversation
- `PUT /api/v1/conversations/{id}` - Update conversation
- `DELETE /api/v1/conversations/{id}` - Delete conversation

### Messages
- `GET /api/v1/conversations/{id}/messages` - List messages in conversation

### Chat
- `POST /api/v1/chat` - Send message and get AI response

## 🎨 Design System

- **Colors**: Dark theme with VS Code color palette
- **Typography**: Segoe UI for text, Consolas for code
- **Spacing**: 4px base unit (xs=4, sm=8, md=16, lg=24, xl=32, 2xl=48)
- **Breakpoints**: Mobile <640px, Tablet 640-1024px, Desktop >1024px

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.10+)
- Verify virtual environment is activated
- Check if port 8000 is available

### Frontend won't start
- Check Node.js version: `node --version` (should be 18+)
- Delete `node_modules` and run `npm install` again
- Check if port 5173 is available

### Ollama connection errors
- Ensure Ollama is running: `ollama list`
- Check Ollama base URL in backend `.env`
- Verify Llama 3.1 model is installed: `ollama pull llama3.1`

### CORS errors
- Verify frontend URL is in `BACKEND_CORS_ORIGINS` in backend `.env`
- Check browser console for specific CORS error messages

## 📚 Documentation

- [Complete Specification](SPEC.md)
- [User Stories](USER_STORIES.md)
- [UI/UX Specification](UI_UX_SPEC.md)
- [AI Model Setup](AI_MODEL.md)

## 🎉 Acknowledgments

- Built with FastAPI, React, Vite, Tailwind CSS
- Powered by Ollama and Llama 3.1
- Inspired by ChatGPT and GitHub Copilot
