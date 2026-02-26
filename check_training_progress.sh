#!/bin/bash
# 📊 TRAINING MONITOR - Check progress anytime
# Usage: ./check_training_progress.sh

cd ~/Nam-toon-studio

echo "🌙 OVERNIGHT TRAINING MONITOR"
echo "======================================================================"
echo ""

# Check if running
if [ -f full_training_pid.txt ]; then
    PID=$(cat full_training_pid.txt)
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ Training is RUNNING (PID: $PID)"
    else
        echo "✅ Training COMPLETED"
    fi
else
    echo "⚠️  Training not started"
fi

echo ""
echo "📊 CURRENT PROGRESS:"
echo "----------------------------------------------------------------------"

# Show last 40 lines of log
if [ -f full_overnight_training.log ]; then
    tail -40 full_overnight_training.log
else
    echo "⏳ Log file not found yet..."
fi

echo ""
echo "======================================================================"
echo ""
echo "📁 Imported Data So Far:"
echo "   Photos: $(ls training_photos/ 2>/dev/null | wc -l | xargs) files"
echo "   Audio:  $(ls training_audio/ 2>/dev/null | wc -l | xargs) files"
echo "   Videos: $(ls training_video/ 2>/dev/null | wc -l | xargs) files"
echo "   PDFs:   $(ls training_pdfs/ 2>/dev/null | wc -l | xargs) files"
echo ""
echo "💡 To check again: ./check_training_progress.sh"
echo "🛑 To stop: kill $(cat full_training_pid.txt 2>/dev/null)"
