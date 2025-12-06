#!/bin/bash
# 🚀 AUTO START ORCHESTRATOR
# ਆਟੋਮੈਟਿਕ ਸਿਸਟਮ ਸਟਾਰਟਰ

echo "🎯 Starting Master Training Orchestrator..."
echo "ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ! 🙏"
echo ""

cd ~/Nam-toon-studio
source .venv/bin/activate

# Run orchestrator
python3 MASTER_TRAINING_ORCHESTRATOR.py \
  --hours 24 \
  --max-videos 100 \
  --cleanup-threshold 150

echo ""
echo "✅ Orchestrator finished!"
