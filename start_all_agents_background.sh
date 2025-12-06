#!/bin/bash
# 🤖 AUTO AGENT LAUNCHER - 24x7 Background Service
# ਆਟੋ ਏਜੰਟ ਲਾਂਚਰ - 24x7 ਬੈਕਗਰਾਉਂਡ ਸੇਵਾ

echo "🤖 STARTING ALL AGENTS IN BACKGROUND..."
echo "========================================"

# Workspace
WORKSPACE="/Users/gurpreetdhillon/Nam-toon-studio"
cd "$WORKSPACE"

# Activate virtual environment
source .venv/bin/activate

# Create logs directory
mkdir -p agent_logs

# Kill any existing agents
pkill -f "autonomous_learning_agent.py" 2>/dev/null
pkill -f "data_collection_agent.py" 2>/dev/null

echo ""
echo "1️⃣ Starting Autonomous Learning Agent..."
nohup python autonomous_learning_agent.py --mode continuous \
    > agent_logs/autonomous_agent_$(date +%Y%m%d_%H%M%S).log 2>&1 &
AGENT1_PID=$!
echo "   ✅ PID: $AGENT1_PID"
echo "   📋 Log: agent_logs/autonomous_agent_*.log"

sleep 2

echo ""
echo "2️⃣ Agent Status:"
if ps -p $AGENT1_PID > /dev/null; then
    echo "   ✅ Autonomous Agent: RUNNING (PID: $AGENT1_PID)"
else
    echo "   ❌ Autonomous Agent: FAILED TO START"
fi

echo ""
echo "========================================"
echo "✅ ALL AGENTS RUNNING IN BACKGROUND!"
echo ""
echo "📊 MONITORING COMMANDS:"
echo ""
echo "Check agent status:"
echo "   ps aux | grep 'autonomous_learning_agent'"
echo ""
echo "View live logs:"
echo "   tail -f agent_logs/autonomous_agent_*.log"
echo ""
echo "Check AI progress:"
echo "   python integrated_smart_video_maker.py --stats"
echo ""
echo "Stop all agents:"
echo "   pkill -f 'autonomous_learning_agent.py'"
echo ""
echo "Check videos created:"
echo "   ls -lh training_video_*.mp4 | wc -l"
echo ""
echo "========================================"
echo "🙏 ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫ਼ਤਿਹ!"
echo ""
echo "💤 Now sleep! Agent will work all night!"
echo "🌅 Check in morning: python integrated_smart_video_maker.py --stats"
echo ""
