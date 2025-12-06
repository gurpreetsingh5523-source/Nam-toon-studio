#!/bin/zsh
# 🚀 Auto-Start Script for macOS
# This makes the agent start automatically when laptop boots

AGENT_PATH="/Users/gurpreetdhillon/Nam-toon-studio/LIVE_SMART_AGENT.py"
PYTHON_PATH="/Users/gurpreetdhillon/Nam-toon-studio/.venv/bin/python"
LOG_PATH="/Users/gurpreetdhillon/Nam-toon-studio/auto_start.log"

echo "🚀 Auto-starting Live Smart Agent..." >> "$LOG_PATH"
echo "⏰ $(date)" >> "$LOG_PATH"

# Wait for system to be ready
sleep 10

# Start agent
cd /Users/gurpreetdhillon/Nam-toon-studio
$PYTHON_PATH $AGENT_PATH >> "$LOG_PATH" 2>&1 &

echo "✅ Agent started with PID: $!" >> "$LOG_PATH"
