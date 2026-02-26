#!/bin/bash
# 🛑 STOP ALL AGENTS
# ਸਾਰੇ ਏਜੰਟ ਬੰਦ ਕਰੋ

echo "🛑 STOPPING ALL AGENTS..."
echo "========================="

# Kill autonomous agent
pkill -f "autonomous_learning_agent.py"
KILLED1=$?

# Kill data collection agent (if running)
pkill -f "data_collection_agent.py"
KILLED2=$?

sleep 1

echo ""
if [ $KILLED1 -eq 0 ]; then
    echo "✅ Autonomous Learning Agent: STOPPED"
else
    echo "⚠️  Autonomous Learning Agent: NOT RUNNING"
fi

if [ $KILLED2 -eq 0 ]; then
    echo "✅ Data Collection Agent: STOPPED"
else
    echo "⚠️  Data Collection Agent: NOT RUNNING"
fi

echo ""
echo "========================="
echo "✅ All agents stopped!"
echo ""
