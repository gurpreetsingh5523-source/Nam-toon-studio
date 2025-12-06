#!/usr/bin/env python3
"""
👨‍👩‍👧‍👦 AI FAMILY SYSTEM - ਪਰਿਵਾਰ ਸਿਸਟਮ
ਸਾਰੇ AI dimaaग ਮਿਲ ਕੇ ਕੰਮ ਕਰਦੇ ਨੇ

Family Members (ਪਰਿਵਾਰ ਦੇ ਮੈਂਬਰ):
1. 🧠 Amrit Main Brain - Supreme controller
2. 👨‍💻 Rahbar AI Developer - Auto fixes code
3. 🤖 Auto Healer - Detects & fixes problems
4. 🎓 Learning Brain - Learns from everything
5. 🎬 Video Maker Brain - Creates videos
6. 📊 Monitor Brain - Watches everything
7. 📚 Teacher Brain - Teaches others

ਜਿਵੇਂ ਪਰਿਵਾਰ ਵਿੱਚ ਹਰ ਕੋਈ ਆਪਣਾ ਕੰਮ ਕਰੇ
Like a family where everyone does their part

ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ! 🙏
"""

import os
import sys
import json
import time
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

WORKSPACE = Path(__file__).parent.absolute()
sys.path.insert(0, str(WORKSPACE))


class AIFamilySystem:
    """
    👨‍👩‍👧‍👦 Complete AI Family
    ਪੂਰਾ AI ਪਰਿਵਾਰ
    """
    
    def __init__(self):
        self.workspace = WORKSPACE
        self.family_log = self.workspace / "ai_family_log.json"
        self.running = False
        
        # Family members
        self.members = {
            "amrit_main": {"status": "active", "role": "Supreme Controller"},
            "rahbar_developer": {"status": "standby", "role": "Auto Developer"},
            "auto_healer": {"status": "standby", "role": "Problem Fixer"},
            "learning_brain": {"status": "standby", "role": "Continuous Learner"},
            "video_maker": {"status": "standby", "role": "Video Creator"},
            "monitor": {"status": "standby", "role": "System Watcher"},
            "teacher": {"status": "standby", "role": "Knowledge Sharer"}
        }
        
        # Communication channel (shared memory)
        self.family_memory = {
            "problems_detected": [],
            "fixes_applied": [],
            "lessons_learned": [],
            "videos_created": [],
            "current_health": "unknown"
        }
        
        print("👨‍👩‍👧‍👦 AI Family System initialized")
        print(f"   Family members: {len(self.members)}")
    
    def start_auto_healer(self):
        """Start auto-healer brain"""
        print("\n🤖 Starting Auto-Healer...")
        
        def healer_loop():
            while self.running:
                try:
                    result = subprocess.run(
                        [sys.executable, str(self.workspace / "rahbar_auto_healer.py"), "--once"],
                        cwd=self.workspace,
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                    
                    # Parse results
                    if "Problems detected:" in result.stdout:
                        for line in result.stdout.split('\n'):
                            if "Problems detected:" in line:
                                count = int(line.split(':')[1].strip())
                                self.family_memory["problems_detected"].append({
                                    "timestamp": datetime.now().isoformat(),
                                    "count": count
                                })
                    
                    self.members["auto_healer"]["status"] = "active"
                    
                except Exception as e:
                    print(f"   ⚠️ Healer error: {e}")
                    self.members["auto_healer"]["status"] = "error"
                
                time.sleep(300)  # Every 5 minutes
        
        thread = threading.Thread(target=healer_loop, daemon=True)
        thread.start()
        self.members["auto_healer"]["status"] = "active"
        print("   ✅ Auto-Healer active")
    
    def start_learning_brain(self):
        """Start learning brain"""
        print("\n🎓 Starting Learning Brain...")
        
        def learning_loop():
            while self.running:
                try:
                    # Run Rahbar auto-learner
                    result = subprocess.run(
                        [sys.executable, str(self.workspace / "rahbar_auto_learner.py")],
                        cwd=self.workspace,
                        capture_output=True,
                        text=True,
                        timeout=180
                    )
                    
                    if "lessons_studied" in result.stdout:
                        self.family_memory["lessons_learned"].append({
                            "timestamp": datetime.now().isoformat(),
                            "session": "completed"
                        })
                    
                    self.members["learning_brain"]["status"] = "active"
                    
                except Exception as e:
                    print(f"   ⚠️ Learning error: {e}")
                    self.members["learning_brain"]["status"] = "error"
                
                time.sleep(3600)  # Every hour
        
        thread = threading.Thread(target=learning_loop, daemon=True)
        thread.start()
        self.members["learning_brain"]["status"] = "active"
        print("   ✅ Learning Brain active")
    
    def start_video_maker(self):
        """Start video maker brain"""
        print("\n🎬 Starting Video Maker...")
        
        def video_loop():
            while self.running:
                try:
                    # Use simple working agent
                    agent_path = self.workspace / "simple_working_agent.py"
                    if not agent_path.exists():
                        print(f"   ⚠️ Agent not found: {agent_path}")
                        time.sleep(60)
                        continue
                    
                    result = subprocess.run(
                        [sys.executable, str(agent_path),
                         "--videos", "5", "--delay", "10"],
                        cwd=self.workspace,
                        capture_output=True,
                        text=True,
                        timeout=600
                    )
                    
                    # Count videos created
                    if "Created:" in result.stdout:
                        for line in result.stdout.split('\n'):
                            if "Created:" in line:
                                created = int(line.split(':')[1].split('/')[0].strip())
                                self.family_memory["videos_created"].append({
                                    "timestamp": datetime.now().isoformat(),
                                    "count": created
                                })
                    
                    self.members["video_maker"]["status"] = "active"
                    
                except Exception as e:
                    print(f"   ⚠️ Video maker error: {e}")
                    self.members["video_maker"]["status"] = "error"
                
                time.sleep(1800)  # Every 30 minutes
        
        thread = threading.Thread(target=video_loop, daemon=True)
        thread.start()
        self.members["video_maker"]["status"] = "active"
        print("   ✅ Video Maker active")
    
    def start_monitor(self):
        """Start monitor brain"""
        print("\n📊 Starting Monitor...")
        
        def monitor_loop():
            while self.running:
                try:
                    # Check system health
                    video_count = len(list(self.workspace.glob("training_*.mp4")))
                    
                    # Check processes
                    result = subprocess.run(
                        ["ps", "aux"],
                        capture_output=True,
                        text=True
                    )
                    
                    active_processes = 0
                    for line in result.stdout.split('\n'):
                        if any(x in line for x in ['rahbar', 'simple_working', 'auto_healer']):
                            active_processes += 1
                    
                    health = "healthy" if active_processes > 0 else "idle"
                    self.family_memory["current_health"] = health
                    
                    self.members["monitor"]["status"] = "active"
                    
                    # Print status
                    print(f"\n📊 System Health: {health}")
                    print(f"   Videos: {video_count}")
                    print(f"   Active processes: {active_processes}")
                    print(f"   Family members active: {sum(1 for m in self.members.values() if m['status'] == 'active')}")
                    
                except Exception as e:
                    print(f"   ⚠️ Monitor error: {e}")
                    self.members["monitor"]["status"] = "error"
                
                time.sleep(180)  # Every 3 minutes
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
        self.members["monitor"]["status"] = "active"
        print("   ✅ Monitor active")
    
    def start_teacher(self):
        """Start teacher brain"""
        print("\n📚 Starting Teacher...")
        
        def teacher_loop():
            while self.running:
                try:
                    # Check if there are new lessons to teach
                    feed_file = self.workspace / "rahbar_learning_feed.json"
                    if feed_file.exists():
                        with open(feed_file, 'r') as f:
                            feed = json.load(f)
                        
                        lesson_count = len(feed.get('lessons_learned', []))
                        healing_count = len(feed.get('auto_healing_lessons', []))
                        
                        print(f"\n📚 Knowledge Base:")
                        print(f"   Lessons: {lesson_count}")
                        print(f"   Healing lessons: {healing_count}")
                        print(f"   Total: {lesson_count + healing_count}")
                    
                    self.members["teacher"]["status"] = "active"
                    
                except Exception as e:
                    print(f"   ⚠️ Teacher error: {e}")
                    self.members["teacher"]["status"] = "error"
                
                time.sleep(600)  # Every 10 minutes
        
        thread = threading.Thread(target=teacher_loop, daemon=True)
        thread.start()
        self.members["teacher"]["status"] = "active"
        print("   ✅ Teacher active")
    
    def family_meeting(self):
        """Family meeting - all brains share status"""
        print("\n" + "="*70)
        print("👨‍👩‍👧‍👦 FAMILY MEETING - ਪਰਿਵਾਰ ਮੀਟਿੰਗ")
        print("="*70)
        
        print("\n📋 Family Members Status:")
        for name, info in self.members.items():
            status_icon = "✅" if info['status'] == 'active' else "⏸️" if info['status'] == 'standby' else "❌"
            print(f"   {status_icon} {info['role']:20s} ({name}): {info['status']}")
        
        print("\n💭 Shared Memory:")
        print(f"   Problems detected: {len(self.family_memory['problems_detected'])}")
        print(f"   Fixes applied: {len(self.family_memory['fixes_applied'])}")
        print(f"   Lessons learned: {len(self.family_memory['lessons_learned'])}")
        print(f"   Videos created: {sum(v['count'] for v in self.family_memory['videos_created'])}")
        print(f"   Current health: {self.family_memory['current_health']}")
        
        print("\n" + "="*70)
    
    def save_family_state(self):
        """Save family state"""
        state = {
            "timestamp": datetime.now().isoformat(),
            "members": self.members,
            "memory": self.family_memory
        }
        
        with open(self.family_log, 'w') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    
    def start_family(self):
        """Start the entire family system"""
        print("\n" + "="*70)
        print("👨‍👩‍👧‍👦 STARTING AI FAMILY SYSTEM")
        print("   ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ")
        print("="*70)
        
        self.running = True
        
        # Start each family member with error handling
        try:
            self.start_auto_healer()
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Auto-healer start error: {e}")
        
        try:
            self.start_learning_brain()
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Learning brain start error: {e}")
        
        try:
            self.start_video_maker()
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Video maker start error: {e}")
        
        try:
            self.start_monitor()
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Monitor start error: {e}")
        
        try:
            self.start_teacher()
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Teacher start error: {e}")
        
        print("\n✅ All family members started!")
        
        # Run family meetings periodically
        try:
            while self.running:
                time.sleep(600)  # Every 10 minutes
                self.family_meeting()
                self.save_family_state()
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Stopping family system...")
            self.running = False
            time.sleep(3)
            print("✅ Family system stopped")


def main():
    """Main entry point"""
    family = AIFamilySystem()
    family.start_family()


if __name__ == "__main__":
    main()
