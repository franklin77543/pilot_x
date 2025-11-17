# 🚀 PilotX Quick Start Guide

## Current Status

✅ **Frontend**: Running on http://localhost:5173  
✅ **Backend**: Running on http://localhost:8000  
✅ **Ollama**: Should be running on http://localhost:11434  

## Quick Commands

### Start Backend
```powershell
cd backend
E:/My_Repo/Github/20251117_PilotX/backend/venv/Scripts/python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend
```powershell
cd frontend
npm run dev
```

### Test Ollama
```powershell
ollama list
curl http://localhost:11434/api/tags
```

## Using PilotX

1. **Open Browser**: Navigate to http://localhost:5173
2. **Create Chat**: Click "New Chat" button in sidebar
3. **Send Message**: Type your message and press Enter
4. **View Response**: AI response appears with Markdown formatting
5. **Manage Chats**: 
   - Click on any chat to switch to it
   - Hover over chat and click Edit icon to rename
   - Hover over chat and click Delete icon to remove

## Features Working

- ✅ Create new conversations
- ✅ Send messages to AI (Ollama + Llama 3.1)
- ✅ View conversation history
- ✅ Markdown rendering in messages
- ✅ Code syntax highlighting with copy button
- ✅ Rename conversations
- ✅ Delete conversations
- ✅ Sidebar toggle
- ✅ Responsive design
- ✅ Error handling

## API Endpoints Available

- `GET /api/v1/conversations` - List all conversations
- `POST /api/v1/conversations` - Create new conversation
- `PUT /api/v1/conversations/{id}` - Update conversation title
- `DELETE /api/v1/conversations/{id}` - Delete conversation
- `GET /api/v1/conversations/{id}/messages` - Get messages
- `POST /api/v1/chat` - Send message and get AI response

## Testing the API

View API documentation at: http://localhost:8000/docs

Or use the test script:
```powershell
cd e:\My_Repo\Github\20251117_PilotX
E:/My_Repo/Github/20251117_PilotX/backend/venv/Scripts/python.exe test_api.py
```

## Troubleshooting

### Backend not starting
- Make sure you're in the `backend` directory
- Check that port 8000 is not in use
- Verify Python virtual environment is activated

### Frontend not starting
- Make sure you're in the `frontend` directory
- Check that port 5173 is not in use
- Try `npm install` if dependencies are missing

### No AI response
- Check if Ollama is running: `ollama list`
- Verify Llama 3.1 model is installed: `ollama pull llama3.1`
- Check backend logs for errors

### CORS errors
- Verify frontend URL (http://localhost:5173) is in backend .env BACKEND_CORS_ORIGINS
- Restart backend after .env changes

## Next Steps

1. **Test the application** - Send some messages and verify AI responses
2. **Check error handling** - Try invalid inputs to see error messages
3. **Test conversation management** - Create, rename, delete conversations
4. **Verify persistence** - Restart backend and check if conversations persist

## Project Structure Summary

```
PilotX/
├── frontend/          # React + TypeScript + Vite + Tailwind
├── backend/           # FastAPI + SQLAlchemy + Ollama (Layered Architecture)
│   ├── models/        # Database ORM models
│   ├── repositories/  # Database operations
│   ├── services/      # Business logic
│   └── api/           # HTTP endpoints
├── prototype/         # Static HTML prototype (reference)
├── README.md          # Full documentation
├── SPEC.md            # Complete specification
├── USER_STORIES.md    # User stories
├── UI_UX_SPEC.md      # Design system
└── AI_MODEL.md        # Ollama setup guide
```

## Have Fun! 🎉

You now have a fully functional AI chat assistant running locally!
