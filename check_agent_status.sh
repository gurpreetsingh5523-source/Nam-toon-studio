#!/bin/bash
# 📊 CHECK AGENT STATUS & PROGRESS
# ਏਜੰਟ ਸਥਿਤੀ ਤੇ ਤਰੱਕੀ ਦੇਖੋ

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 AGENT STATUS & PROGRESS CHECK"
echo "   ਏਜੰਟ ਸਥਿਤੀ ਤੇ ਤਰੱਕੀ"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd /Users/gurpreetdhillon/Nam-toon-studio

# Check if agents are running
echo "🤖 AGENT STATUS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

AGENT_RUNNING=$(ps aux | grep "[a]utonomous_learning_agent.py" | wc -l)
if [ $AGENT_RUNNING -gt 0 ]; then
    AGENT_PID=$(ps aux | grep "[a]utonomous_learning_agent.py" | awk '{print $2}')
    echo "✅ Autonomous Agent: RUNNING (PID: $AGENT_PID)"
else
    echo "❌ Autonomous Agent: NOT RUNNING"
fi

echo ""

# Count videos
echo "🎬 VIDEOS CREATED:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
TOTAL_VIDEOS=$(ls -1 training_video_*.mp4 2>/dev/null | wc -l)
echo "   Total: $TOTAL_VIDEOS videos"

if [ $TOTAL_VIDEOS -gt 0 ]; then
    echo ""
    echo "   Latest 5 videos:"
    ls -lht training_video_*.mp4 2>/dev/null | head -5 | awk '{print "   📹", $9, "-", $5}'
fi

echo ""

# AI Learning Status
echo "🧠 AI LEARNING STATUS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "ai_memory.json" ]; then
    python3 << 'PYTHON_SCRIPT'
import json
try:
    with open('ai_memory.json', 'r') as f:
        data = json.load(f)
    
    total = data.get('total_videos_created', 0)
    success = data.get('successful_renders', 0)
    failed = data.get('failed_renders', 0)
    patterns = len(data.get('learned_patterns', {}))
    
    print(f"   Videos created: {total}")
    print(f"   Successful: {success}")
    print(f"   Failed: {failed}")
    
    if total > 0:
        rate = (success / total) * 100
        print(f"   Success rate: {rate:.1f}%")
    
    print(f"   Patterns learned: {patterns}")
    
    if patterns > 0:
        print("\n   📊 Top patterns:")
        for name, info in list(data['learned_patterns'].items())[:3]:
            count = info.get('count', 1)
            print(f"      • {name}: {count}x")
            
except Exception as e:
    print(f"   ❌ Could not read AI memory: {e}")
PYTHON_SCRIPT
else
    echo "   ⚠️  No AI memory file found"
fi

echo ""

# Disk space
echo "💾 DISK USAGE:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
VIDEOS_SIZE=$(du -sh training_video_*.mp4 2>/dev/null | tail -1 | awk '{print $1}')
if [ ! -z "$VIDEOS_SIZE" ]; then
    echo "   Training videos: $VIDEOS_SIZE"
else
    echo "   Training videos: 0 B"
fi

echo ""

# Latest log
echo "📋 LATEST AGENT LOG (last 10 lines):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
LATEST_LOG=$(ls -t agent_logs/autonomous_agent_*.log 2>/dev/null | head -1)
if [ ! -z "$LATEST_LOG" ]; then
    tail -10 "$LATEST_LOG" 2>/dev/null | sed 's/^/   /'
else
    echo "   ⚠️  No log file found"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Status check complete!"
echo ""
echo "💡 USEFUL COMMANDS:"
echo "   Start agents:  ./start_all_agents_background.sh"
echo "   Stop agents:   ./stop_all_agents.sh"
echo "   View logs:     tail -f agent_logs/autonomous_agent_*.log"
echo "   AI stats:      python integrated_smart_video_maker.py --stats"
echo ""
