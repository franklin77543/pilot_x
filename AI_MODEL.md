# PilotX - AI 模型配置指南

**版本**: 1.0.0  
**最後更新**: 2025-11-17  
**選定模型**: Llama 3.1 (8B) via Ollama

---

## 硬體規格

**HP OMEN Gaming Laptop 16-AM0269T**
- CPU: Intel Core i7-14650HX (16核心/24執行緒)
- RAM: 32GB DDR5 5600 MT/s
- GPU: NVIDIA GeForce RTX 5070 (8GB VRAM)
- 適合運行: 中大型 AI 模型 (8B-70B)

---

## 選定方案：Ollama + Llama 3.1 (8B)

### 為什麼選擇 Llama 3.1 (8B)？

✅ **開發階段完美選擇**
- 模型大小: 4.7GB
- RAM 使用: ~8GB
- 回應速度: 快 (RTX 5070 加速)
- 品質: 優秀，接近 GPT-3.5
- 中文支援: 良好
- 成本: 完全免費

✅ **技術優勢**
- 支援 8K context window
- 多語言能力強
- 程式碼生成優秀
- 推理能力佳

---

## 安裝步驟

### 1. 安裝 Ollama

```powershell
# 方法 1: 使用 winget (推薦)
winget install Ollama.Ollama

# 方法 2: 手動下載
# 訪問: https://ollama.com/download/windows
# 下載 OllamaSetup.exe 並安裝
```

### 2. 驗證安裝

```powershell
# 檢查版本
ollama --version

# 應該顯示類似: ollama version is 0.x.x
```

### 3. 下載 Llama 3.1 (8B) 模型

```powershell
# 下載模型 (約 4.7GB，需要幾分鐘)
ollama pull llama3.1:8b

# 查看已安裝的模型
ollama list
```

### 4. 測試模型

```powershell
# 啟動互動式對話
ollama run llama3.1:8b

# 測試問題
# >>> 你好，請用繁體中文介紹你自己
# >>> 請寫一個 Python FastAPI 的 Hello World 範例

# 退出: /bye 或 Ctrl+D
```

### 5. 啟動 API 服務

```powershell
# Ollama 安裝後會自動在背景運行
# API 端點: http://localhost:11434

# 測試 API (使用 curl)
curl http://localhost:11434/api/generate -d "{\"model\": \"llama3.1:8b\", \"prompt\": \"你好\"}" --json

# 或使用 PowerShell
Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body '{"model":"llama3.1:8b","prompt":"Hello"}' -ContentType "application/json"
```

---

## PilotX 後端整合配置

### 環境變數設定 (backend/.env)

```bash
# AI 提供者設定
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama3.1:8b

# Ollama 專用設定
OLLAMA_TIMEOUT=60
OLLAMA_TEMPERATURE=0.7
OLLAMA_MAX_TOKENS=2000

# 未來擴充 (暫時註解)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
```

### Python 後端整合範例

```python
# backend/app/services/ollama_service.py
import httpx
from app.core.config import settings

async def chat_with_ollama(prompt: str, model: str = None) -> str:
    """與 Ollama 模型對話"""
    if model is None:
        model = settings.DEFAULT_MODEL
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": settings.OLLAMA_TEMPERATURE,
                    "num_predict": settings.OLLAMA_MAX_TOKENS,
                }
            }
        )
        data = response.json()
        return data["response"]
```

---

## GPU 加速設定

### 確認 GPU 使用

```powershell
# 查看 Ollama 是否使用 GPU
ollama ps

# 運行模型時監控 GPU
# 開啟工作管理員 > 效能 > GPU 1 (NVIDIA RTX 5070)
# 應該看到 GPU 使用率上升
```

### 優化建議

Ollama 會自動偵測並使用 NVIDIA GPU，無需額外配置。

如果想手動控制：
```powershell
# 設定環境變數 (可選)
$env:CUDA_VISIBLE_DEVICES = "0"  # 使用第一張 GPU (RTX 5070)
```

---

## 模型對比與升級路徑

### 階段一：開發測試
- ✅ **Llama 3.1 (8B)** - 當前選擇
  - 快速、免費、品質好
  - 適合開發 UI/UX 和功能測試

### 階段二：進階選擇 (可選)

| 模型 | 優勢 | 使用時機 |
|------|------|----------|
| **Qwen 2.5 (14B)** | 中文更強 | 需要更好的中文理解 |
| **Llama 3.1 (70B-Q4)** | 頂級品質 | 展示或高要求場景 |
| **DeepSeek Coder (33B)** | 程式碼專精 | 開發者工具特化版 |

### 階段三：雲端 API (部署時)

| 服務 | 模型 | 優勢 | 成本 |
|------|------|------|------|
| **OpenAI** | GPT-3.5-Turbo | 速度快、穩定 | $0.0005/1K tokens |
| **OpenAI** | GPT-4 Turbo | 品質最佳 | $0.01/1K tokens |
| **Google** | Gemini Pro | 免費額度大 | 免費 (有限制) |
| **Anthropic** | Claude 3 Haiku | 速度快、便宜 | $0.00025/1K tokens |

---

## 常用 Ollama 指令

```powershell
# 列出所有已安裝模型
ollama list

# 下載其他模型
ollama pull qwen2.5:14b
ollama pull deepseek-coder:6.7b

# 刪除模型
ollama rm llama3.1:8b

# 查看運行中的模型
ollama ps

# 停止所有模型
ollama stop --all

# 更新 Ollama
winget upgrade Ollama.Ollama
```

---

## 效能基準測試

### 預期效能 (RTX 5070 + 32GB RAM)

| 指標 | Llama 3.1 (8B) | 備註 |
|------|----------------|------|
| 載入時間 | ~2-3 秒 | 首次載入 |
| Token/秒 | 80-120 | GPU 加速 |
| 回應延遲 | 1-3 秒 | 短問題 |
| 記憶體使用 | ~8GB | 模型 + 運行 |
| GPU VRAM | ~6GB | 使用 RTX 5070 |

---

## 故障排除

### 問題 1: Ollama 服務未啟動
```powershell
# 手動啟動 Ollama
ollama serve

# 或重新安裝服務
ollama uninstall
ollama install
```

### 問題 2: GPU 未被使用
```powershell
# 確認 CUDA 已安裝
nvidia-smi

# 重新安裝 Ollama (會自動偵測 GPU)
```

### 問題 3: 回應速度慢
- 檢查 GPU 使用率
- 確認模型已完全載入到 VRAM
- 減少 `num_predict` 參數

### 問題 4: 中文輸出亂碼
```powershell
# 設定 PowerShell 編碼
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

---

## 下一步

- [x] 安裝 Ollama
- [x] 下載 Llama 3.1 (8B)
- [x] 測試模型運行
- [ ] 整合到 PilotX 後端
- [ ] 實作前端對話介面
- [ ] 效能優化與測試

---

**準備好了嗎？讓我們開始建立 PilotX 專案！** 🚀