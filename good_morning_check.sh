#!/bin/bash
# 🌅 GOOD MORNING CHECK - See what AI did overnight!
# ਸਵੇਰ ਦੀ ਜਾਂਚ - ਦੇਖੋ AI ਨੇ ਰਾਤ ਭਰ ਕੀ ਕੀਤਾ!

clear

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌅 GOOD MORNING! ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ!"
echo "   Let's see what AI did last night..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd /Users/gurpreetdhillon/Nam-toon-studio
source .venv/bin/activate

# Quick stats
echo "📊 OVERNIGHT PROGRESS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Count videos
TOTAL_VIDEOS=$(ls -1 training_video_*.mp4 2>/dev/null | wc -l | tr -d ' ')
echo "   🎬 Total videos: $TOTAL_VIDEOS"

# Last 24 hours videos
YESTERDAY=$(date -v-1d +%Y%m%d)
TODAY=$(date +%Y%m%d)
NEW_VIDEOS=$(ls -1 training_video_${TODAY}*.mp4 training_video_${YESTERDAY}*.mp4 2>/dev/null | wc -l | tr -d ' ')
echo "   🆕 Last 24h: $NEW_VIDEOS new videos"

# Total size
TOTAL_SIZE=$(du -sh training_video_*.mp4 2>/dev/null | tail -1 | awk '{print $1}')
if [ ! -z "$TOTAL_SIZE" ]; then
    echo "   💾 Total size: $TOTAL_SIZE"
fi

echo ""

# AI Learning
echo "🧠 AI LEARNING STATS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 << 'PYTHON_SCRIPT'
import json

try:
    with open('ai_memory.json', 'r') as f:
        data = json.load(f)
    
    total = data.get('total_videos_created', 0)
    success = data.get('successful_renders', 0)
    patterns = len(data.get('learned_patterns', {}))
    scores = data.get('user_satisfaction_scores', [])
    
    print(f"   📹 Videos: {total}")
    print(f"   ✅ Success: {success}/{total} ({(success/total*100):.1f}%)" if total > 0 else "   ✅ Success: 0")
    print(f"   🧠 Patterns: {patterns} learned")
    
    if scores:
        avg = sum(scores) / len(scores)
        print(f"   ⭐ Avg rating: {avg:.1f}/5")
    
    if patterns > 0:
        print("\n   📊 What AI learned:")
        for name, info in list(data['learned_patterns'].items())[:5]:
            count = info.get('count', 1)
            print(f"      • {name}: {count}x")

except:
    print("   ⚠️  Could not read AI stats")
PYTHON_SCRIPT

echo ""

# Agent status
echo "🤖 AGENT STATUS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ps aux | grep -q "[a]utonomous_learning_agent"; then
    AGENT_PID=$(ps aux | grep "[a]utonomous_learning_agent" | awk '{print $2}')
    echo "   ✅ Autonomous Agent: STILL RUNNING! (PID: $AGENT_PID)"
    echo "   💪 Agent is working hard!"
else
    echo "   ⚠️  Agent: STOPPED (may need restart)"
fi

echo ""

# Latest videos
echo "🎬 LATEST 5 VIDEOS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ls -lht training_video_*.mp4 2>/dev/null | head -5 | while read line; do
    filename=$(echo $line | awk '{print $9}')
    size=$(echo $line | awk '{print $5}')
    time=$(echo $line | awk '{print $6, $7, $8}')
    echo "   📹 $filename"
    echo "      Size: $size, Time: $time"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "☕ HAVE A GREAT DAY! ਚੰਗਾ ਦਿਨ ਹੋਵੇ!"
echo ""
echo "💡 COMMANDS:"
echo "   • Stop agent:     ./stop_all_agents.sh"
echo "   • Restart agent:  ./start_all_agents_background.sh"
echo "   • Full stats:     ./check_agent_status.sh"
echo "   • View logs:      tail -f agent_logs/autonomous_agent_*.log"
echo ""
echo "🙏 ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫ਼ਤਿਹ!"
echo ""
