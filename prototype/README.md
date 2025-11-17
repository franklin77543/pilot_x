# PilotX - HTML/CSS 靜態原型

這是 PilotX 的可互動靜態原型，用於預覽 UI/UX 設計。

## 功能展示

### ✅ 已實作功能
- **深色主題** - 專業的深色介面設計
- **響應式設計** - 支援桌面、平板、手機
- **對話列表** - Sidebar 顯示歷史對話
- **訊息輸入** - 自動調整高度的輸入框
- **Markdown 渲染** - 完整支援 Markdown 格式
- **程式碼高亮** - 使用 Highlight.js
- **互動功能**:
  - 發送訊息 (Enter 或點擊按鈕)
  - 新增對話
  - 切換對話
  - 重新命名對話
  - 刪除對話
  - 複製訊息
  - Loading 動畫

### 📱 響應式測試
- **桌面** (> 1024px): Sidebar 固定顯示
- **平板** (640-1024px): Sidebar 可收合
- **手機** (< 640px): Sidebar 全螢幕 Overlay

## 使用方式

### 方法 1: 直接開啟 (推薦)
1. 在檔案總管中找到 `index.html`
2. 雙擊開啟
3. 在瀏覽器中瀏覽

### 方法 2: 使用 VS Code Live Server
1. 在 VS Code 中開啟此資料夾
2. 安裝 "Live Server" 擴充功能
3. 右鍵點擊 `index.html` → "Open with Live Server"

### 方法 3: 使用 Python HTTP Server
```bash
# 在此目錄執行
python -m http.server 8080

# 訪問 http://localhost:8080
```

## 測試項目

### 基本功能測試
- [ ] 輸入訊息並發送
- [ ] 查看 AI 回應
- [ ] Markdown 格式正確顯示
- [ ] 程式碼高亮正常
- [ ] 複製訊息功能
- [ ] 新增對話
- [ ] 切換對話
- [ ] 重新命名對話
- [ ] 刪除對話

### 響應式測試
- [ ] 桌面版佈局正常
- [ ] 平板版 Sidebar 可收合
- [ ] 手機版操作流暢
- [ ] 不同螢幕尺寸文字清晰

### 互動測試
- [ ] Enter 發送訊息
- [ ] Shift+Enter 換行
- [ ] 輸入框自動調整高度
- [ ] Hover 效果正常
- [ ] 按鈕點擊回饋
- [ ] 捲動流暢

## 特殊測試指令

在輸入框中輸入以下內容測試特定功能：

- **"code"** 或 **"程式"** - 顯示程式碼範例
- **"hello"** - 簡單問候回應
- **其他文字** - 顯示預設回應

## 檔案結構

```
prototype/
├── index.html      # 主 HTML 檔案
├── styles.css      # 樣式表
├── script.js       # JavaScript 互動邏輯
└── README.md       # 本說明檔
```

## 技術細節

### 使用的套件 (CDN)
- **Marked.js** - Markdown 解析器
- **Highlight.js** - 程式碼語法高亮
- **GitHub Dark** - 程式碼高亮主題

### CSS 變數系統
所有顏色、間距、字體都使用 CSS 變數定義，方便調整。

### 響應式斷點
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

## 與實際應用的差異

這是**靜態原型**，與實際應用的差異：
- ❌ 無真實 AI 回應 (使用模擬回應)
- ❌ 無後端連接
- ❌ 對話不會持久化
- ❌ 無真正的 Ollama 整合

實際應用會：
- ✅ 連接 Ollama API
- ✅ 使用 FastAPI 後端
- ✅ SQLite 資料庫儲存對話
- ✅ 真實的 Llama 3.1 回應

## 下一步

原型驗證完成後，可以：
1. 根據測試結果調整設計
2. 開始實作前端 (React + Vite)
3. 開始實作後端 (FastAPI)
4. 整合 Ollama API

## 意見回饋

測試時如發現任何問題或有改進建議，請記錄下來以便後續調整。

---

**建立日期**: 2025-11-17  
**版本**: 1.0.0  
**狀態**: ✅ 可測試
