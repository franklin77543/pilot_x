# PilotX - UI/UX 設計規格

**版本**: 1.0.0  
**最後更新**: 2025-11-17  
**狀態**: Draft  
**設計理念**: 簡潔、高效、專業

---

## 目錄
- [設計原則](#設計原則)
- [色彩系統](#色彩系統)
- [字體系統](#字體系統)
- [間距系統](#間距系統)
- [頁面架構](#頁面架構)
- [組件設計](#組件設計)
- [互動設計](#互動設計)
- [響應式設計](#響應式設計)
- [無障礙設計](#無障礙設計)

---

## 設計原則

### 核心價值
1. **簡潔優先** - 減少視覺噪音，聚焦對話本身
2. **效率至上** - 快速載入，流暢互動
3. **專業感** - 現代化設計，適合工作場景
4. **易用性** - 無需學習即可上手

### 設計靈感
- ChatGPT - 簡潔的對話介面
- GitHub Copilot - 專業的開發者工具感
- Linear - 現代化的 UI 設計
- Vercel - 乾淨的視覺風格

---

## 色彩系統

### 主色調 (Primary)
```css
/* 深色主題 (推薦，階段一主要使用) */
--bg-primary: #0A0A0A;        /* 主背景 */
--bg-secondary: #1A1A1A;      /* 次要背景 */
--bg-tertiary: #2A2A2A;       /* 卡片、輸入框背景 */
--bg-hover: #333333;          /* Hover 狀態 */

/* 文字顏色 */
--text-primary: #FFFFFF;      /* 主要文字 */
--text-secondary: #A0A0A0;    /* 次要文字 */
--text-tertiary: #707070;     /* 輔助文字 */

/* 強調色 */
--accent-primary: #3B82F6;    /* 主要按鈕、連結 */
--accent-hover: #2563EB;      /* Hover 狀態 */
--accent-active: #1D4ED8;     /* Active 狀態 */

/* 語意色 */
--success: #10B981;           /* 成功狀態 */
--warning: #F59E0B;           /* 警告 */
--error: #EF4444;             /* 錯誤 */
--info: #3B82F6;              /* 資訊 */

/* 邊框 */
--border-primary: #2A2A2A;    /* 主要邊框 */
--border-secondary: #333333;  /* 次要邊框 */
```

### 淺色主題 (階段二)
```css
/* 淺色主題 (未來擴充) */
--bg-primary-light: #FFFFFF;
--bg-secondary-light: #F9FAFB;
--bg-tertiary-light: #F3F4F6;
--text-primary-light: #111827;
--text-secondary-light: #6B7280;
```

---

## 字體系統

### 字體族
```css
/* 主要字體 */
--font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', 
             Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji';

/* 等寬字體 (程式碼) */
--font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco', 
             'Courier New', monospace;

/* 中文字體優化 */
--font-zh: 'Microsoft JhengHei', '微軟正黑體', 'PingFang TC', 
           'Noto Sans TC', sans-serif;
```

### 字體大小
```css
--text-xs: 0.75rem;    /* 12px - 輔助文字 */
--text-sm: 0.875rem;   /* 14px - 次要文字 */
--text-base: 1rem;     /* 16px - 基礎大小 */
--text-lg: 1.125rem;   /* 18px - 訊息內容 */
--text-xl: 1.25rem;    /* 20px - 標題 */
--text-2xl: 1.5rem;    /* 24px - 大標題 */
```

### 行高
```css
--leading-tight: 1.25;   /* 緊湊 */
--leading-normal: 1.5;   /* 正常 */
--leading-relaxed: 1.75; /* 寬鬆 */
```

---

## 間距系統

### Spacing Scale (8px 基準)
```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

### 圓角
```css
--radius-sm: 0.25rem;   /* 4px - 小元素 */
--radius-md: 0.5rem;    /* 8px - 按鈕、輸入框 */
--radius-lg: 0.75rem;   /* 12px - 卡片 */
--radius-xl: 1rem;      /* 16px - Modal */
--radius-full: 9999px;  /* 圓形 */
```

### 陰影
```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
```

---

## 頁面架構

### 整體佈局

```
┌─────────────────────────────────────────────────┐
│ Header (Optional - 階段二)                       │
├──────────┬──────────────────────────────────────┤
│          │                                      │
│ Sidebar  │       Main Chat Area                │
│          │                                      │
│ (對話列表) │   ┌──────────────────────────────┐   │
│          │   │                              │   │
│          │   │   Messages                   │   │
│  - 新對話  │   │                              │   │
│  - 對話1  │   │   ┌──────────────────────┐   │   │
│  - 對話2  │   │   │ User Message         │   │   │
│  - 對話3  │   │   └──────────────────────┘   │   │
│          │   │                              │   │
│          │   │   ┌──────────────────────┐   │   │
│          │   │   │ AI Response          │   │   │
│          │   │   │ (Markdown + Code)    │   │   │
│          │   │   └──────────────────────┘   │   │
│          │   │                              │   │
│          │   └──────────────────────────────┘   │
│          │                                      │
│          │   ┌──────────────────────────────┐   │
│          │   │ Input Area                   │   │
│          │   │ [輸入訊息...]        [發送]   │   │
│          │   └──────────────────────────────┘   │
│          │                                      │
└──────────┴──────────────────────────────────────┘
```

### 尺寸規格

#### 桌面版 (> 1024px)
- Sidebar 寬度: 280px (可收合)
- Main Area: 剩餘空間，最大 900px (置中)
- Header 高度: 60px (可選)
- Input Area 最小高度: 56px (可擴展至 200px)

#### 平板版 (640px - 1024px)
- Sidebar: 預設收合，點擊展開 (Overlay)
- Main Area: 100% 寬度

#### 手機版 (< 640px)
- Sidebar: 全螢幕 Overlay
- Main Area: 100% 寬度
- Input Area: 固定在底部

---

## 組件設計

### 1. Sidebar (對話列表)

#### 結構
```jsx
<Sidebar>
  <Header>
    <Logo>PilotX</Logo>
    <NewChatButton>+ 新對話</NewChatButton>
  </Header>
  
  <ConversationList>
    <ConversationItem active>
      <Title>FastAPI 開發討論</Title>
      <Timestamp>2 小時前</Timestamp>
      <Actions>
        <RenameButton />
        <DeleteButton />
      </Actions>
    </ConversationItem>
    {/* More items... */}
  </ConversationList>
  
  <Footer>
    <ModelIndicator>
      <Icon />
      <Text>Llama 3.1 (本地)</Text>
    </ModelIndicator>
  </Footer>
</Sidebar>
```

#### 樣式規格
- 背景: `var(--bg-secondary)`
- 項目 Padding: `12px 16px`
- 項目間距: `4px`
- Hover 效果: 背景變為 `var(--bg-hover)`
- Active 狀態: 左側 3px 藍色邊框

#### 互動
- 點擊項目: 切換對話
- Hover 顯示操作按鈕 (重新命名、刪除)
- 長按拖曳: 排序 (階段二)

---

### 2. Message List (訊息列表)

#### User Message (使用者訊息)
```jsx
<UserMessage>
  <Avatar>U</Avatar>
  <Content>
    <Text>請幫我解釋什麼是 FastAPI</Text>
    <Timestamp>10:30</Timestamp>
  </Content>
</UserMessage>
```

**樣式:**
- 背景: `var(--bg-tertiary)`
- 圓角: `var(--radius-lg)`
- Padding: `12px 16px`
- 靠右對齊 (可選，或統一靠左)
- 最大寬度: 80%

#### AI Message (AI 回應)
```jsx
<AIMessage>
  <Avatar>
    <AIIcon />
  </Avatar>
  <Content>
    <MarkdownContent>
      {/* Rendered Markdown */}
    </MarkdownContent>
    <Actions>
      <CopyButton />
      <RegenerateButton />
    </Actions>
    <Timestamp>10:30</Timestamp>
  </Content>
</AIMessage>
```

**樣式:**
- 背景: `var(--bg-primary)` (無背景色，與主背景融合)
- 邊框: 1px `var(--border-primary)` (可選)
- Padding: `16px`
- 靠左對齊
- 最大寬度: 100%

#### Loading State
```jsx
<AIMessage>
  <Avatar>
    <Spinner />
  </Avatar>
  <Content>
    <LoadingDots>AI 正在思考...</LoadingDots>
  </Content>
</AIMessage>
```

---

### 3. Code Block (程式碼區塊)

#### 結構
```jsx
<CodeBlock>
  <Header>
    <Language>python</Language>
    <CopyButton>複製</CopyButton>
  </Header>
  <Pre>
    <Code className="language-python">
      {/* Syntax highlighted code */}
    </Code>
  </Pre>
</CodeBlock>
```

#### 樣式
- 背景: `#1E1E1E` (VS Code Dark)
- 字體: `var(--font-mono)`
- 字體大小: `14px`
- 行高: `1.6`
- Padding: `16px`
- 圓角: `var(--radius-md)`
- 語法高亮主題: **GitHub Dark** 或 **VS Code Dark+**

#### 功能
- 支援 50+ 程式語言
- 一鍵複製
- 行號顯示 (可選)
- 程式碼折疊 (階段二)

---

### 4. Input Area (輸入區域)

#### 結構
```jsx
<InputArea>
  <TextArea 
    placeholder="輸入訊息... (Enter 發送, Shift+Enter 換行)"
    autoResize
    maxHeight="200px"
  />
  <Actions>
    <AttachButton /> {/* 階段二 */}
    <SendButton disabled={!hasText}>
      <SendIcon />
    </SendButton>
  </Actions>
</InputArea>
```

#### 樣式
- 背景: `var(--bg-tertiary)`
- 邊框: `1px solid var(--border-primary)`
- Focus 邊框: `1px solid var(--accent-primary)`
- 圓角: `var(--radius-lg)`
- Padding: `12px 16px`
- 最小高度: `56px`
- 最大高度: `200px` (超過則捲動)

#### 互動
- 自動 Focus
- Enter 發送訊息
- Shift+Enter 換行
- 自動調整高度
- 發送後清空並保持 Focus
- 字元數限制: 4000 (顯示剩餘字數於 > 3500 時)

---

### 5. Button (按鈕)

#### 主要按鈕
```css
.btn-primary {
  background: var(--accent-primary);
  color: white;
  padding: 8px 16px;
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: var(--accent-hover);
}

.btn-primary:disabled {
  background: var(--bg-hover);
  color: var(--text-tertiary);
  cursor: not-allowed;
}
```

#### 次要按鈕
```css
.btn-secondary {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-primary);
  padding: 8px 16px;
  border-radius: var(--radius-md);
}

.btn-secondary:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}
```

#### 圖示按鈕
```css
.btn-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  color: var(--text-secondary);
  transition: all 0.2s;
}

.btn-icon:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}
```

---

## 互動設計

### 動畫與過渡

#### 頁面切換
```css
.fade-enter {
  opacity: 0;
}
.fade-enter-active {
  opacity: 1;
  transition: opacity 200ms ease-in;
}
.fade-exit {
  opacity: 1;
}
.fade-exit-active {
  opacity: 0;
  transition: opacity 200ms ease-out;
}
```

#### 訊息進入
- 新訊息從下方淡入 + 輕微上移
- 動畫時長: 300ms
- Easing: ease-out

#### Hover 效果
- 過渡時間: 150ms
- Easing: ease-in-out
- 屬性: background, color, border-color

#### Loading 狀態
```jsx
<LoadingDots>
  <Dot style={{animationDelay: '0ms'}} />
  <Dot style={{animationDelay: '150ms'}} />
  <Dot style={{animationDelay: '300ms'}} />
</LoadingDots>
```

### 鍵盤快捷鍵 (階段二)

| 快捷鍵 | 功能 |
|--------|------|
| `Ctrl/Cmd + K` | 開始新對話 |
| `Ctrl/Cmd + /` | 顯示快捷鍵列表 |
| `Ctrl/Cmd + B` | 切換 Sidebar |
| `Esc` | 關閉 Modal/清除輸入 |
| `↑` | 編輯上一則訊息 (在空白輸入框) |

---

## 響應式設計

### 斷點 (Breakpoints)
```css
/* Mobile */
@media (max-width: 639px) { /* sm */ }

/* Tablet */
@media (min-width: 640px) and (max-width: 1023px) { /* md */ }

/* Desktop */
@media (min-width: 1024px) { /* lg */ }

/* Large Desktop */
@media (min-width: 1280px) { /* xl */ }
```

### 行動裝置優化

#### 佈局調整
- Sidebar: 全螢幕 Overlay，從左側滑入
- 輸入框: 固定在底部 (Safe Area 支援)
- 訊息: 100% 寬度，減少左右 Padding

#### 觸控優化
- 按鈕最小尺寸: 44x44px
- 點擊區域: 足夠大，避免誤觸
- 滑動手勢: 左滑顯示操作選單 (階段二)

#### 效能優化
- 虛擬捲動: 長對話使用虛擬列表
- 圖片懶載入
- 程式碼區塊按需渲染

---

## 無障礙設計 (Accessibility)

### ARIA 標籤
```jsx
<button 
  aria-label="發送訊息"
  aria-disabled={!hasText}
>
  <SendIcon aria-hidden="true" />
</button>

<div role="alert" aria-live="polite">
  {errorMessage}
</div>
```

### 鍵盤導航
- 所有互動元素可用 Tab 聚焦
- Focus 狀態有明確視覺指示
- 支援 Enter/Space 觸發按鈕

### 對比度
- 文字與背景對比度 ≥ 4.5:1 (WCAG AA)
- 重要元素對比度 ≥ 7:1 (WCAG AAA)

### 螢幕閱讀器
- 語意化 HTML 標籤
- Alt 文字描述
- 動態內容變更通知

---

## 設計檢查清單

### 階段一必須完成
- [ ] 深色主題完整實作
- [ ] 響應式佈局 (手機/平板/桌面)
- [ ] Markdown 完整渲染
- [ ] 程式碼語法高亮
- [ ] Loading 狀態動畫
- [ ] 錯誤提示樣式
- [ ] 基本 Hover/Focus 效果

### 階段二進階功能
- [ ] 淺色主題
- [ ] 主題切換動畫
- [ ] 進階鍵盤快捷鍵
- [ ] 滑動手勢
- [ ] 訊息操作選單
- [ ] 虛擬捲動優化
- [ ] 完整無障礙支援

---

## 設計資源

### 參考網站
- [ChatGPT](https://chat.openai.com) - 對話介面設計
- [Claude](https://claude.ai) - Markdown 渲染
- [Linear](https://linear.app) - 現代化 UI
- [Vercel](https://vercel.com) - 簡潔風格

### 設計工具
- Figma: 原型設計 (可選)
- Tailwind CSS: 快速樣式開發
- Lucide Icons: 圖示系統
- React Syntax Highlighter: 程式碼高亮

### 字體資源
- [JetBrains Mono](https://www.jetbrains.com/lp/mono/) - 程式碼字體
- [Inter](https://rsms.me/inter/) - UI 字體 (可選替代)

---

**下一步: 開始前端開發，按照此規格實作 UI！** 🎨
