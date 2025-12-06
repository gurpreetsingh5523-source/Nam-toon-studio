# 🎯 MASTER TRAINING ORCHESTRATOR GUIDE
## ਮਾਸਟਰ ਟ੍ਰੇਨਿੰਗ ਸਿਸਟਮ - ਪੂਰੀ ਗਾਈਡ

📅 **Date**: December 4, 2025

---

## 🌟 ਕੀ ਬਣਾਇਆ? / WHAT'S CREATED?

### ✅ **MASTER_TRAINING_ORCHESTRATOR.py**
ਸਭ ਤੋਂ ਵੱਡਾ ਸਿਸਟਮ ਜੋ ਸਾਰੇ agents ਨੂੰ ਮੈਨੇਜ ਕਰੇ!

**Features:**
1. ✅ **Different Patterns for Each Agent**
   - 4 agents, ਹਰ ਇੱਕ ਨੂੰ ਵੱਖਰੇ patterns
   - Agent 1: Gurbani + Spiritual (30 videos)
   - Agent 2: Culture + Family (30 videos)
   - Agent 3: History + Daily Life (20 videos)
   - Agent 4: Technology (20 videos)

2. ✅ **Uses Your Existing Data**
   - Brain files (brain_*.txt)
   - Gurbani knowledge (gurbani_knowledge.json)
   - Photos library
   - Audio library
   - **ਸਾਰਾ ਡਾਟਾ ਵਰਤੇਗਾ!**

3. ✅ **Auto Cleanup**
   - Keeps max 100 training videos
   - When 150+ videos, deletes oldest
   - **Space ਸਾਫ਼ ਰਹੇਗੀ!**

4. ✅ **Rahbar AI Guidance**
   - Every 6 hours checks system
   - Gets AI guidance
   - **ਸਮਾਰਟ ਫੈਸਲੇ!**

5. ✅ **24/7 Auto Operation**
   - Runs continuously
   - Monitors all agents
   - Restarts if needed
   - **ਖੁਦ ਕੰਮ ਕਰੇਗਾ!**

---

## 🚀 HOW TO START / ਕਿਵੇਂ ਚਾਲੂ ਕਰਨਾ

### Option 1: **Simple Start (Recommended)**
```bash
cd ~/Nam-toon-studio
./start_orchestrator.sh
```

### Option 2: **Custom Settings**
```bash
cd ~/Nam-toon-studio
source .venv/bin/activate

# Run with custom settings:
python3 MASTER_TRAINING_ORCHESTRATOR.py \
  --hours 48 \
  --max-videos 200 \
  --cleanup-threshold 250
```

### Option 3: **Background Mode (24/7)**
```bash
cd ~/Nam-toon-studio
nohup ./start_orchestrator.sh > orchestrator.log 2>&1 &

# Check if running:
ps aux | grep MASTER_TRAINING_ORCHESTRATOR
```

---

## 📊 WHAT HAPPENS? / ਕੀ ਹੋਵੇਗਾ?

### 🔄 **Cycle 1 (30 min):**
```
1. Check video count
2. Delete old videos if >150
3. Consult Rahbar AI (if time)
4. Assign patterns to 4 agents
5. Start agents
6. Monitor progress
7. Sleep 30 minutes
```

### 🔄 **Cycle 2-48 (Next 24 hours):**
```
Repeat same process...
```

### 📈 **Expected Results After 24 Hours:**
```
✅ Agent 1 (Spiritual):  30 videos
✅ Agent 2 (Culture):    30 videos
✅ Agent 3 (Life):       20 videos
✅ Agent 4 (Tech):       20 videos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total New Videos:        100 videos
Old Videos Deleted:      Auto (keeps 100 max)
Data Used:               All brain files, Gurbani, etc.
```

---

## 🎯 PATTERN LIBRARY / ਪੈਟਰਨ ਲਾਇਬ੍ਰੇਰੀ

### 📿 **Gurbani Patterns:**
```python
From: brain_01_sggs_core.txt
From: gurbani_knowledge.json
Examples:
  - ਜਪੁਜੀ ਸਾਹਿਬ ਦਾ ਪਾਠ
  - ਰਹਿਰਾਸ ਸਾਹਿਬ
  - Morning prayer scenes
  - Evening ardas
```

### 🎨 **Punjabi Culture:**
```python
Scenarios:
  - Village morning (ਪਿੰਡ ਦੀ ਸਵੇਰ)
  - Gurdwara seva (ਗੁਰਦੁਆਰੇ ਦੀ ਸੇਵਾ)
  - Wedding celebration (ਵਿਆਹ)
  - Harvest festival (ਵਿਸਾਖੀ)
  - Grandma stories (ਦਾਦੀ ਦੀਆਂ ਕਹਾਣੀਆਂ)
```

### 👨‍👩‍👧‍👦 **Family Stories:**
```python
From: brain_04_family_relationships.txt
Examples:
  - Family gathering
  - Parent-child relationships
  - Elder wisdom
```

### 📚 **Historical:**
```python
From: brain_03_punjab_history.txt
Examples:
  - Punjab history
  - Sikh Gurus
  - Cultural heritage
```

### 🏠 **Daily Life:**
```python
From: brain_05_daily_life.txt
Examples:
  - Daily routines
  - Common activities
  - Social interactions
```

---

## 🗑️ AUTO CLEANUP SYSTEM

### How It Works:
```
Video Count Check:
├─ <100 videos  → ✅ Nothing happens
├─ 100-150      → ⚠️ Warning logged
└─ >150 videos  → 🗑️ Delete oldest

Delete Process:
1. Sort videos by age (oldest first)
2. Keep newest 100
3. Delete rest
4. Log results
```

### Example:
```
Current: 175 videos
Action:  Delete 75 oldest
Result:  100 videos remain
Space:   ~30 MB freed
```

---

## 🧠 RAHBAR AI INTEGRATION

### What Rahbar AI Does:
```
Every 6 hours:
1. Scans all systems
2. Checks for gaps
3. Suggests improvements
4. Updates pattern library
5. Optimizes agent assignments
```

### Rahbar AI Commands:
```bash
# Manual check:
python3 RAHBAR_AI_DEVELOPER.py --scan

# Full analysis:
python3 RAHBAR_AI_DEVELOPER.py --analyze

# Build new code:
python3 RAHBAR_AI_DEVELOPER.py --build
```

---

## 📋 MONITORING / ਮਾਨੀਟਰਿੰਗ

### Check Running Status:
```bash
# See orchestrator logs:
tail -f master_orchestrator.log

# See agent logs:
tail -f agent_training_log.json

# Check processes:
ps aux | grep MASTER_TRAINING_ORCHESTRATOR
ps aux | grep autonomous_learning_agent
```

### Check Video Count:
```bash
cd ~/Nam-toon-studio
ls training_video*.mp4 | wc -l
du -sh training_video*.mp4 | tail -1
```

### Check Disk Space:
```bash
df -h ~
```

---

## 🛑 HOW TO STOP / ਕਿਵੇਂ ਬੰਦ ਕਰਨਾ

### Stop Orchestrator:
```bash
# Find process:
ps aux | grep MASTER_TRAINING_ORCHESTRATOR

# Kill by name:
pkill -f MASTER_TRAINING_ORCHESTRATOR

# Or by PID:
kill <PID>
```

### Stop All Agents:
```bash
pkill -f autonomous_learning_agent
```

### Emergency Stop:
```bash
# Kill everything:
pkill -f MASTER_TRAINING_ORCHESTRATOR
pkill -f autonomous_learning_agent
pkill -f RAHBAR_AI
```

---

## 🔧 CONFIGURATION / ਸੈਟਿੰਗਾਂ

### Config File: `orchestrator_config.json`
```json
{
  "max_training_videos": 100,
  "cleanup_threshold": 150,
  "auto_cleanup": true,
  "video_retention_days": 7,
  "agents": {
    "autonomous_learning_agent": {
      "enabled": true,
      "patterns": ["punjabi_culture", "gurbani", "family"],
      "max_videos_per_session": 20
    }
  },
  "rahbar_ai": {
    "enabled": true,
    "check_interval_hours": 6
  },
  "data_sources": {
    "brain_files": true,
    "gurbani_data": true,
    "photos_library": true,
    "audio_library": true
  }
}
```

### Customize Settings:
```bash
# Edit config:
nano orchestrator_config.json

# Restart orchestrator:
pkill -f MASTER_TRAINING_ORCHESTRATOR
./start_orchestrator.sh
```

---

## 📊 EXPECTED RESULTS / ਨਤੀਜੇ

### After 24 Hours:
```
✅ Videos Created:        100 diverse videos
✅ Patterns Used:         20+ different patterns
✅ Data Sources:          All brain files + Gurbani
✅ Old Videos Deleted:    Auto-cleaned
✅ Disk Space:            ~40-50 MB used
✅ AI Learning:           Continuous improvement
✅ Rahbar Guidance:       4 consultations
```

### Quality Improvements:
```
✅ More variety (not same videos)
✅ Better cultural representation
✅ Gurbani integration
✅ Family story diversity
✅ Technical learning content
```

---

## 🎬 AGENT ASSIGNMENTS

| Agent | Focus | Patterns | Max Videos |
|-------|-------|----------|------------|
| **Agent 1** | Spiritual | Gurbani + Prayer | 30 |
| **Agent 2** | Culture | Village + Family | 30 |
| **Agent 3** | Life | History + Daily | 20 |
| **Agent 4** | Tech | Computer + Learning | 20 |

---

## 💡 TIPS / ਟਿੱਪਸ

### 1. **First Run:**
```bash
# Start in foreground to monitor:
./start_orchestrator.sh

# Watch for 1 hour, then Ctrl+C
# If working well, restart in background:
nohup ./start_orchestrator.sh &
```

### 2. **Check Progress:**
```bash
# Every few hours:
tail -f master_orchestrator.log
ls training_video*.mp4 | wc -l
```

### 3. **Optimize:**
```bash
# After 24 hours, check what worked:
python3 -c "
import json
log = json.load(open('agent_training_log.json'))
print(f'Success rate: {log.get(\"success_rate\", 0)*100:.1f}%')
"
```

---

## 🚨 TROUBLESHOOTING

### Problem: Orchestrator not starting
```bash
# Check Python:
source .venv/bin/activate
python3 --version

# Check dependencies:
pip install pydub pillow numpy

# Try manual:
python3 MASTER_TRAINING_ORCHESTRATOR.py --hours 1
```

### Problem: Agents not creating videos
```bash
# Check agent file:
ls -lh autonomous_learning_agent.py

# Check video maker:
python3 -c "from integrated_smart_video_maker import IntegratedSmartVideoMaker; print('OK')"

# Check logs:
tail -50 master_orchestrator.log
```

### Problem: Too many videos
```bash
# Lower limits in config:
{
  "max_training_videos": 50,
  "cleanup_threshold": 75
}

# Or manual cleanup:
rm training_video*.mp4
```

---

## 📝 SUMMARY / ਸੰਖੇਪ

```
✅ Created: MASTER_TRAINING_ORCHESTRATOR.py
✅ Modified: autonomous_learning_agent.py (added limited mode)
✅ Created: start_orchestrator.sh (easy starter)
✅ Features: 
   - 4 agents with different patterns
   - Uses all your existing data
   - Auto-deletes old videos
   - Rahbar AI guidance
   - 24/7 operation

🚀 To Start:
   ./start_orchestrator.sh

🛑 To Stop:
   pkill -f MASTER_TRAINING_ORCHESTRATOR
```

---

**ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ! 🙏**

**ਹੁਣ ਸਿਸਟਮ ਖੁਦ ਸਿੱਖੇਗਾ ਤੇ ਵਧੀਆ ਵੀਡੀਓ ਬਣਾਵੇਗਾ!** 🌟
