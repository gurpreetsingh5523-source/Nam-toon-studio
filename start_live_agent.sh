#!/bin/zsh
# 🔴 Start Live Agent in Background

cd /Users/gurpreetdhillon/Nam-toon-studio

# Kill old if running
pkill -f "LIVE_SMART_AGENT.py" 2>/dev/null

# Start new
nohup /Users/gurpreetdhillon/Nam-toon-studio/.venv/bin/python LIVE_SMART_AGENT.py > live_agent_output.log 2>&1 &

PID=$!
echo $PID > live_agent.pid

echo "🔴 Live Agent Started!"
echo "📍 PID: $PID"
echo "📄 Logs: live_agent.log"
echo "📊 Progress: live_progress.json"
echo ""
echo "⏹️  Stop: kill $PID"
