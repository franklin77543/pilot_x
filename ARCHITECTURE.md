# Backend Architecture

PilotX 後端採用 **Layered Architecture (分層架構)**,遵循 Clean Architecture 原則,確保程式碼的可維護性、可測試性和可擴展性。

## 🏗️ 架構設計

### 分層結構

```
┌─────────────────────────────────────┐
│      API Layer (HTTP Endpoints)     │  ← conversation_api.py, message_api.py
├─────────────────────────────────────┤
│      Service Layer (Business Logic) │  ← conversation_service.py, message_service.py
├─────────────────────────────────────┤
│   Repository Layer (Database CRUD)  │  ← conversation_repository.py, message_repository.py
├─────────────────────────────────────┤
│      Model Layer (ORM Models)       │  ← conversation_model.py, message_model.py
└─────────────────────────────────────┘
```

### 依賴方向

```
API Layer → Service Layer → Repository Layer → Model Layer → Database
```

**原則**: 每一層只能依賴下一層,不能跨層或反向依賴。

## 📁 檔案結構

```
backend/app/
├── models/                          # Model Layer
│   ├── conversation_model.py        # Conversation ORM model
│   └── message_model.py             # Message ORM model
│
├── repositories/                    # Repository Layer
│   ├── conversation_repository.py   # Conversation CRUD operations
│   └── message_repository.py        # Message CRUD operations
│
├── services/                        # Service Layer
│   ├── conversation_service.py      # Conversation business logic
│   ├── message_service.py           # Message & Chat business logic
│   └── ollama.py                    # Ollama AI integration
│
├── api/                             # API Layer
│   ├── conversation_api.py          # Conversation HTTP endpoints
│   └── message_api.py               # Message & Chat HTTP endpoints
│
├── schemas/                         # Pydantic Schemas
│   ├── conversation_schema.py       # Conversation Request/Response models
│   └── message_schema.py            # Message & Chat Request/Response models
│
├── core/                            # Core Configuration
│   └── config.py                    # Settings & Environment
│
├── db/                              # Database
│   └── session.py                   # Database session & Base
│
├── dependencies.py                  # Dependency Injection
└── main.py                          # FastAPI Application
```

## 🔄 資料流向

### 1. Conversation Management Flow

```
GET /api/v1/conversations
    ↓
conversation_api.list_conversations()
    ↓
conversation_service.list_conversations()
    ↓
conversation_repository.get_conversations()
    ↓
Database Query (Conversation model)
    ↓
Return Conversation objects
```

### 2. Chat Message Flow

```
POST /api/v1/chat
    ↓
message_api.chat()
    ↓
message_service.chat()
    ├→ conversation_repository.get_conversation_by_id()
    ├→ message_repository.create_message() [user message]
    ├→ ollama_service.chat() [AI response]
    ├→ message_repository.create_message() [assistant message]
    └→ conversation_repository.update_conversation() [update title]
    ↓
Return ChatResponse
```

## 📦 各層職責

### 1. Model Layer (模型層)

**職責**: 定義資料庫表結構

**檔案**:
- `conversation_model.py` - Conversation 表 (id, title, created_at, updated_at)
- `message_model.py` - Message 表 (id, conversation_id, role, content, model, created_at)

**特點**:
- 使用 SQLAlchemy ORM
- 定義表之間的關聯關係
- 不包含業務邏輯

```python
# conversation_model.py
class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    messages = relationship("Message", back_populates="conversation")
```

### 2. Repository Layer (資料庫層)

**職責**: 執行資料庫 CRUD 操作

**檔案**:
- `conversation_repository.py` - Conversation CRUD
- `message_repository.py` - Message CRUD

**特點**:
- 只知道 Database Session 和 Model
- 提供簡單的 CRUD 方法
- 不包含業務邏輯

```python
# conversation_repository.py
class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_conversations(self, skip: int, limit: int):
        return self.db.query(Conversation).offset(skip).limit(limit).all()
    
    def create_conversation(self, title: str):
        conversation = Conversation(title=title)
        self.db.add(conversation)
        self.db.commit()
        return conversation
```

### 3. Service Layer (服務層)

**職責**: 實現業務邏輯

**檔案**:
- `conversation_service.py` - Conversation 業務邏輯
- `message_service.py` - Message & Chat 業務邏輯
- `ollama.py` - Ollama AI 整合

**特點**:
- 只依賴 Repository,不直接操作資料庫
- 處理複雜的業務流程
- 協調多個 Repository

```python
# message_service.py
class MessageService:
    def __init__(self, conversation_repo, message_repo):
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo
    
    def chat(self, request: ChatRequest):
        # 1. Get/create conversation
        conversation = self.conversation_repo.get_conversation_by_id(...)
        
        # 2. Save user message
        user_msg = self.message_repo.create_message(...)
        
        # 3. Call AI
        ai_response = ollama_service.chat(...)
        
        # 4. Save AI message
        ai_msg = self.message_repo.create_message(...)
        
        return ChatResponse(...)
```

### 4. API Layer (API 層)

**職責**: 處理 HTTP 請求和響應

**檔案**:
- `conversation_api.py` - Conversation endpoints
- `message_api.py` - Message & Chat endpoints

**特點**:
- 只依賴 Service,不直接操作資料庫或 Repository
- 處理 HTTP 驗證、錯誤處理
- 轉換 HTTP 請求到 Service 調用

```python
# conversation_api.py
@router.get("/conversations")
def list_conversations(
    service: ConversationService = Depends(get_conversation_service)
):
    result = service.list_conversations(page=1, page_size=20)
    return PaginatedResponse(**result)
```

## 🔌 依賴注入 (Dependency Injection)

使用 `dependencies.py` 統一管理依賴注入:

```python
# dependencies.py
def get_conversation_repository(db: Session = Depends(get_db)):
    return ConversationRepository(db)

def get_message_repository(db: Session = Depends(get_db)):
    return MessageRepository(db)

def get_conversation_service(
    repo: ConversationRepository = Depends(get_conversation_repository)
):
    return ConversationService(repo)

def get_message_service(
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
    msg_repo: MessageRepository = Depends(get_message_repository)
):
    return MessageService(conv_repo, msg_repo)
```

## ✅ 架構優勢

### 1. **單一職責原則 (SRP)**
- 每個類別只負責一件事
- Conversation 和 Message 分開管理

### 2. **依賴反轉原則 (DIP)**
- 高層模組不依賴低層模組
- Service 依賴 Repository 介面,不依賴具體實作

### 3. **開放封閉原則 (OCP)**
- 對擴展開放:新增功能只需添加新的 Service 或 Repository
- 對修改封閉:現有程式碼不需要修改

### 4. **可測試性**
- 每一層都可以獨立測試
- 可以 Mock Repository 來測試 Service
- 可以 Mock Service 來測試 API

### 5. **可維護性**
- 清晰的結構,容易找到程式碼
- 職責分離,修改影響範圍小
- 檔案命名一致,易於理解

## 🔧 擴展指南

### 添加新功能

**例如: 添加用戶管理功能**

1. **Model Layer**: 創建 `user_model.py`
```python
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    username = Column(String, unique=True)
```

2. **Repository Layer**: 創建 `user_repository.py`
```python
class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_user_by_username(self, username: str): ...
```

3. **Service Layer**: 創建 `user_service.py`
```python
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    def authenticate(self, username, password): ...
```

4. **API Layer**: 創建 `user_api.py`
```python
@router.post("/login")
def login(service: UserService = Depends(get_user_service)):
    return service.authenticate(...)
```

5. **Dependencies**: 更新 `dependencies.py`
```python
def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_user_service(repo = Depends(get_user_repository)):
    return UserService(repo)
```

6. **Main**: 註冊路由
```python
app.include_router(user_api.router, prefix="/api/v1", tags=["users"])
```

## 📚 參考資料

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
