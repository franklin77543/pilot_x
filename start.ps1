# PilotX Startup Script
# This script starts all required services for PilotX

Write-Host "🚀 Starting PilotX Services..." -ForegroundColor Cyan
Write-Host ""

# Check if Ollama is running
Write-Host "🔍 Checking Ollama..." -ForegroundColor Yellow
try {
    $ollamaCheck = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -Method GET -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ Ollama is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama is not running. Please start Ollama first:" -ForegroundColor Red
    Write-Host "   ollama serve" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Check if Llama 3.1 model is available
Write-Host "🔍 Checking Llama 3.1 model..." -ForegroundColor Yellow
$models = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method GET
$hasLlama = $models.models | Where-Object { $_.name -like "llama3.1*" }
if ($hasLlama) {
    Write-Host "✅ Llama 3.1 model is installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Llama 3.1 model not found. Installing..." -ForegroundColor Yellow
    ollama pull llama3.1
    Write-Host "✅ Llama 3.1 model installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Starting Backend (FastAPI)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; E:/My_Repo/Github/20251117_PilotX/backend/venv/Scripts/python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

Start-Sleep -Seconds 3

Write-Host "🚀 Starting Frontend (Vite)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "✨ PilotX is starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "📌 Services:" -ForegroundColor Cyan
Write-Host "   Frontend:  http://localhost:5173" -ForegroundColor White
Write-Host "   Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host "   Ollama:    http://localhost:11434" -ForegroundColor White
Write-Host ""
Write-Host "⏳ Please wait a few seconds for services to fully start..." -ForegroundColor Yellow
Write-Host "🌐 Opening browser in 5 seconds..." -ForegroundColor Yellow

Start-Sleep -Seconds 5
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "✅ PilotX is ready! Happy chatting! 🎉" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit (this will NOT stop the services)..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
