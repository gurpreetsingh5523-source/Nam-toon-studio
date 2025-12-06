#!/bin/zsh
# 🌙 Start 24/7 Agent Service in Background
# ਇਹ ਸਾਰੀ ਰਾਤ ਚੱਲੇਗੀ - ਤੁਸੀਂ ਸੌਂ ਜਾਓ!

cd /Users/gurpreetdhillon/Nam-toon-studio

echo "🌙 Starting 24/7 Agent Service..."
echo "💤 ਤੁਸੀਂ ਸੌਂ ਜਾਓ - Agents ਸਾਰੀ ਰਾਤ ਕੰਮ ਕਰਨਗੇ!"
echo ""
echo "📋 Service will:"
echo "   • Run every 10 minutes"
echo "   • Auto-fix errors"
echo "   • Auto-upgrade systems"
echo "   • Monitor health"
echo "   • Generate morning report"
echo ""
echo "📝 Logs: 24x7_agent_service.log"
echo "📊 Status: agent_service_status.json"
echo ""
echo "⏹️  To stop: ps aux | grep CONTINUOUS_AGENT_SERVICE"
echo "            kill -9 <PID>"
echo ""

# Run in background
nohup /Users/gurpreetdhillon/Nam-toon-studio/.venv/bin/python \
    /Users/gurpreetdhillon/Nam-toon-studio/CONTINUOUS_AGENT_SERVICE_24x7.py \
    > /Users/gurpreetdhillon/Nam-toon-studio/service_output.log 2>&1 &

SERVICE_PID=$!

echo "✅ Service started!"
echo "🆔 Process ID: $SERVICE_PID"
echo ""
echo "💤 ਹੁਣ ਤੁਸੀਂ ਸੌਂ ਜਾਓ!"
echo "🌅 ਸਵੇਰੇ report ਤਿਆਰ ਹੋਵੇਗੀ!"
echo ""
echo "📄 Service PID saved to: agent_service.pid"

# Save PID
echo $SERVICE_PID > /Users/gurpreetdhillon/Nam-toon-studio/agent_service.pid

echo ""
echo "✅ ALL SET - GOOD NIGHT! 😴"
