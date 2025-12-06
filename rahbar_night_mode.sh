#!/bin/bash
# 🌙 Rahbar AI Night Mode - ਰਾਤੋਂ-ਰਾਤ ਕੰਮ
# ਇਹ script Rahbar Supreme ਨੂੰ ਹਰ ਘੰਟੇ ਚਲਾਏਗਾ

cd ~/Nam-toon-studio

echo "🌙 Rahbar AI Night Mode Starting..."
echo "   ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ"
echo ""

# Run 8 cycles (8 hours overnight)
for i in {1..8}; do
    echo "========================================"
    echo "🔄 Cycle $i/8 - $(date)"
    echo "========================================"
    
    # Run Rahbar Supreme (unbuffered for real-time logs)
    python3 -u rahbar_supreme_controller.py 2>&1
    
    # Wait 1 hour before next cycle
    if [ $i -lt 8 ]; then
        echo ""
        echo "😴 Sleeping 1 hour until next cycle..."
        echo "   Next cycle: $(date -v+1H '+%I:%M %p')"
        sleep 3600
    fi
done

echo ""
echo "🌅 Night mode complete! Morning summary:"
echo "========================================"

# Count total videos created
total_videos=$(find . -name "training_*.mp4" -mtime -1 -type f | wc -l)
echo "📊 Total videos created: $total_videos"

# Show all reports
echo ""
echo "📋 Reports generated:"
ls -lht rahbar_report_*.json | head -3

echo ""
echo "✅ Rahbar AI worked all night!"
echo "   Check rahbar_supreme_log.json for details"
