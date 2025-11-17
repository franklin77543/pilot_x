// ==================== DOM Elements ====================
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const messagesContainer = document.getElementById('messagesContainer');
const messages = document.getElementById('messages');
const newChatBtn = document.getElementById('newChatBtn');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const sidebar = document.getElementById('sidebar');
const conversationList = document.getElementById('conversationList');

// ==================== State ====================
let currentConversationId = 1;
let messageHistory = [];

// ==================== Initialize ====================
document.addEventListener('DOMContentLoaded', () => {
    // Highlight code blocks
    highlightCode();
    
    // Setup event listeners
    setupEventListeners();
    
    // Auto resize textarea
    autoResizeTextarea();
});

// ==================== Event Listeners ====================
function setupEventListeners() {
    // Send message
    sendBtn.addEventListener('click', sendMessage);
    
    // Enter to send, Shift+Enter for new line
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Enable/disable send button based on input
    messageInput.addEventListener('input', () => {
        const hasText = messageInput.value.trim().length > 0;
        sendBtn.disabled = !hasText;
        autoResizeTextarea();
    });
    
    // New chat button
    newChatBtn.addEventListener('click', createNewChat);
    
    // Mobile menu toggle
    mobileMenuBtn.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });
    
    // Click outside sidebar to close on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth < 1024 && 
            sidebar.classList.contains('active') && 
            !sidebar.contains(e.target) && 
            !mobileMenuBtn.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    });
    
    // Conversation item clicks
    conversationList.addEventListener('click', (e) => {
        const item = e.target.closest('.conversation-item');
        if (item && !e.target.closest('.btn-icon')) {
            switchConversation(item.dataset.id);
        }
        
        // Handle delete button
        if (e.target.closest('.btn-icon[title="刪除"]')) {
            e.stopPropagation();
            if (confirm('確定要刪除這個對話嗎？')) {
                item.remove();
            }
        }
        
        // Handle rename button
        if (e.target.closest('.btn-icon[title="重新命名"]')) {
            e.stopPropagation();
            const titleEl = item.querySelector('.conversation-title');
            const newTitle = prompt('輸入新標題：', titleEl.textContent);
            if (newTitle) {
                titleEl.textContent = newTitle;
            }
        }
    });
    
    // Copy button in messages
    messages.addEventListener('click', (e) => {
        if (e.target.closest('.copy-btn')) {
            const messageText = e.target.closest('.message-content').querySelector('.message-text');
            copyToClipboard(messageText.textContent);
            showNotification('已複製！');
        }
    });
}

// ==================== Functions ====================

function sendMessage() {
    const text = messageInput.value.trim();
    if (!text) return;
    
    // Add user message
    addMessage('user', text);
    
    // Clear input
    messageInput.value = '';
    sendBtn.disabled = true;
    autoResizeTextarea();
    
    // Show loading
    const loadingId = addLoadingMessage();
    
    // Simulate AI response (replace with actual API call)
    setTimeout(() => {
        removeLoadingMessage(loadingId);
        
        // Generate mock response
        const response = generateMockResponse(text);
        addMessage('ai', response);
    }, 1500);
    
    // Scroll to bottom
    scrollToBottom();
}

function addMessage(role, content) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}-message`;
    
    const avatarEl = document.createElement('div');
    avatarEl.className = 'message-avatar';
    
    if (role === 'user') {
        avatarEl.textContent = 'U';
    } else {
        avatarEl.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                <path d="M2 17l10 5 10-5"></path>
                <path d="M2 12l10 5 10-5"></path>
            </svg>
        `;
    }
    
    const contentEl = document.createElement('div');
    contentEl.className = 'message-content';
    
    const textEl = document.createElement('div');
    textEl.className = role === 'ai' ? 'message-text markdown-content' : 'message-text';
    
    if (role === 'ai') {
        // Render markdown
        textEl.innerHTML = marked.parse(content);
        // Highlight code
        setTimeout(() => {
            textEl.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });
        }, 0);
    } else {
        textEl.textContent = content;
    }
    
    const timeEl = document.createElement('div');
    timeEl.className = 'message-time';
    timeEl.textContent = new Date().toLocaleTimeString('zh-TW', { hour: '2-digit', minute: '2-digit' });
    
    contentEl.appendChild(textEl);
    
    if (role === 'ai') {
        const actionsEl = document.createElement('div');
        actionsEl.className = 'message-actions';
        actionsEl.innerHTML = `
            <button class="btn-icon copy-btn" title="複製">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
            </button>
        `;
        contentEl.appendChild(actionsEl);
    }
    
    contentEl.appendChild(timeEl);
    
    messageEl.appendChild(avatarEl);
    messageEl.appendChild(contentEl);
    
    messages.appendChild(messageEl);
    
    messageHistory.push({ role, content, timestamp: new Date() });
    
    scrollToBottom();
}

function addLoadingMessage() {
    const loadingId = 'loading-' + Date.now();
    const messageEl = document.createElement('div');
    messageEl.className = 'message ai-message';
    messageEl.id = loadingId;
    
    messageEl.innerHTML = `
        <div class="message-avatar">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                <path d="M2 17l10 5 10-5"></path>
                <path d="M2 12l10 5 10-5"></path>
            </svg>
        </div>
        <div class="message-content">
            <div class="message-text">
                <div class="loading">
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                </div>
                <span style="margin-left: 8px; color: var(--text-secondary);">AI 正在思考...</span>
            </div>
        </div>
    `;
    
    messages.appendChild(messageEl);
    scrollToBottom();
    
    return loadingId;
}

function removeLoadingMessage(loadingId) {
    const loadingEl = document.getElementById(loadingId);
    if (loadingEl) {
        loadingEl.remove();
    }
}

function generateMockResponse(userMessage) {
    const responses = {
        'hello': 'Hello! How can I assist you today?',
        'hi': 'Hi there! What can I help you with?',
        '你好': '你好！有什麼我可以幫忙的嗎？',
        'default': `我收到了您的訊息：「${userMessage}」

這是一個 **靜態原型**，所以我無法真正回答您的問題。在實際應用中，我會連接到 **Ollama + Llama 3.1 (8B)** 模型來提供真實的回應。

### 支援的功能
- ✅ Markdown 格式化
- ✅ 程式碼語法高亮
- ✅ 對話歷史
- ✅ 響應式設計

試試看輸入「code」來看程式碼範例！`
    };
    
    if (userMessage.toLowerCase().includes('code') || userMessage.includes('程式')) {
        return `好的！這是一個 Python 範例：

\`\`\`python
def fibonacci(n):
    """生成費氏數列"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

# 測試
print(fibonacci(10))
# 輸出: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
\`\`\`

這個函數會生成前 n 個費氏數列的數字！`;
    }
    
    const key = Object.keys(responses).find(k => 
        userMessage.toLowerCase().includes(k.toLowerCase())
    );
    
    return responses[key] || responses['default'];
}

function highlightCode() {
    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });
}

function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 200) + 'px';
}

function scrollToBottom() {
    setTimeout(() => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 100);
}

function createNewChat() {
    if (confirm('開始新對話？當前對話將被保存。')) {
        // Clear messages (keep welcome message)
        const welcomeMsg = messages.querySelector('.message');
        messages.innerHTML = '';
        if (welcomeMsg) {
            messages.appendChild(welcomeMsg.cloneNode(true));
        }
        
        messageHistory = [];
        
        // Add new conversation to list
        const newId = Date.now();
        const newItem = document.createElement('div');
        newItem.className = 'conversation-item active';
        newItem.dataset.id = newId;
        newItem.innerHTML = `
            <div class="conversation-content">
                <div class="conversation-title">新對話</div>
                <div class="conversation-time">剛剛</div>
            </div>
        `;
        
        // Remove active from others
        conversationList.querySelectorAll('.conversation-item').forEach(item => {
            item.classList.remove('active');
        });
        
        conversationList.insertBefore(newItem, conversationList.firstChild);
        currentConversationId = newId;
        
        // Close mobile menu
        sidebar.classList.remove('active');
    }
}

function switchConversation(id) {
    conversationList.querySelectorAll('.conversation-item').forEach(item => {
        item.classList.toggle('active', item.dataset.id === id);
    });
    
    currentConversationId = id;
    
    // In real app, load conversation history here
    
    // Close mobile menu
    sidebar.classList.remove('active');
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).catch(err => {
        console.error('複製失敗:', err);
    });
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--success);
        color: white;
        padding: 12px 20px;
        border-radius: var(--radius-md);
        font-size: 0.875rem;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Configure marked.js
marked.setOptions({
    breaks: true,
    gfm: true,
    highlight: function(code, lang) {
        if (lang && hljs.getLanguage(lang)) {
            return hljs.highlight(code, { language: lang }).value;
        }
        return hljs.highlightAuto(code).value;
    }
});
