#!/usr/bin/env python3
"""
🎯 MASTER TRAINING ORCHESTRATOR
ਸਾਰੇ Agents ਨੂੰ ਕੰਟਰੋਲ ਕਰਨ ਵਾਲਾ ਮਾਸਟਰ ਸਿਸਟਮ

Features:
- Auto-assigns different patterns to agents
- Uses existing data for training
- Auto-deletes old training videos after limit
- Runs Rahbar AI for guidance
- Orchestrates all agents automatically

ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ! 🙏
"""

import os
import sys
import json
import time
import signal
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='🎯 [MASTER] %(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('master_orchestrator.log'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

WORKSPACE = Path(__file__).parent.absolute()
sys.path.insert(0, str(WORKSPACE))


class MasterTrainingOrchestrator:
    """
    ਮਾਸਟਰ ਸਿਸਟਮ - ਸਾਰੇ agents ਨੂੰ ਮੈਨੇਜ ਕਰੇ
    """
    
    def __init__(self):
        self.workspace = WORKSPACE
        self.config_file = self.workspace / "orchestrator_config.json"
        self.config = self._load_config()
        
        # Agent processes
        self.running_agents = {}
        
        # Training limits
        self.max_training_videos = self.config.get('max_training_videos', 100)
        self.cleanup_threshold = self.config.get('cleanup_threshold', 150)
        
        # Pattern library from existing data
        self.pattern_library = self._build_pattern_library()
        
        log.info("✅ Master Training Orchestrator initialized")
        log.info(f"📊 Pattern library: {len(self.pattern_library)} patterns loaded")
    
    def _load_config(self):
        """Load orchestrator configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Default config
        default_config = {
            "max_training_videos": 100,
            "cleanup_threshold": 150,
            "auto_cleanup": True,
            "video_retention_days": 7,
            "agents": {
                "autonomous_learning_agent": {
                    "enabled": True,
                    "patterns": ["punjabi_culture", "gurbani", "family"],
                    "max_videos_per_session": 20
                },
                "data_collection_agent": {
                    "enabled": True,
                    "patterns": ["user_stories", "feedback"],
                    "max_videos_per_session": 10
                }
            },
            "rahbar_ai": {
                "enabled": True,
                "check_interval_hours": 6
            },
            "data_sources": {
                "brain_files": True,
                "gurbani_data": True,
                "photos_library": True,
                "audio_library": True
            }
        }
        
        # Save default config
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        return default_config
    
    def _build_pattern_library(self):
        """Build pattern library from existing data"""
        log.info("🔍 Building pattern library from existing data...")
        
        patterns = {
            "gurbani": [],
            "punjabi_culture": [],
            "family_stories": [],
            "tech_learning": [],
            "historical": [],
            "daily_life": [],
            "spiritual": []
        }
        
        # 1. Load from brain files
        brain_files = list(self.workspace.glob("brain_*.txt"))
        log.info(f"📚 Found {len(brain_files)} brain files")
        
        for brain_file in brain_files[:10]:  # Load first 10
            try:
                with open(brain_file, 'r', encoding='utf-8') as f:
                    content = f.read()[:1000]  # First 1000 chars
                    
                if 'sggs' in brain_file.name or 'gurbani' in brain_file.name:
                    patterns['gurbani'].append({
                        "source": brain_file.name,
                        "content": content,
                        "type": "text"
                    })
                elif 'punjab' in brain_file.name or 'itihaas' in brain_file.name:
                    patterns['historical'].append({
                        "source": brain_file.name,
                        "content": content,
                        "type": "text"
                    })
                elif 'parivar' in brain_file.name or 'family' in brain_file.name:
                    patterns['family_stories'].append({
                        "source": brain_file.name,
                        "content": content,
                        "type": "text"
                    })
                elif 'jeevan' in brain_file.name or 'daily' in brain_file.name:
                    patterns['daily_life'].append({
                        "source": brain_file.name,
                        "content": content,
                        "type": "text"
                    })
            except Exception as e:
                log.warning(f"⚠️ Could not load {brain_file.name}: {e}")
        
        # 2. Load from gurbani JSON
        gurbani_json = self.workspace / "gurbani_knowledge.json"
        if gurbani_json.exists():
            try:
                with open(gurbani_json, 'r', encoding='utf-8') as f:
                    gurbani_data = json.load(f)
                    if isinstance(gurbani_data, list):
                        patterns['gurbani'].extend([
                            {"source": "gurbani_knowledge.json", "content": item, "type": "json"}
                            for item in gurbani_data[:20]
                        ])
                    log.info(f"📿 Loaded Gurbani knowledge")
            except Exception as e:
                log.warning(f"⚠️ Could not load gurbani: {e}")
        
        # 3. Generate diverse scenarios
        patterns['punjabi_culture'] = [
            {
                "id": "village_morning",
                "text": "[SCENE 1: Village]\nਪਿੰਡ ਵਿੱਚ ਸਵੇਰ ਹੋਈ, ਕਿਸਾਨ ਖੇਤਾਂ ਵੱਲ ਜਾ ਰਹੇ।\nMorning in village, farmers going to fields.",
                "type": "scenario"
            },
            {
                "id": "gurdwara_seva",
                "text": "[SCENE 1: Gurdwara]\nਗੁਰਦੁਆਰੇ ਵਿੱਚ ਸੇਵਾ ਕਰਦੇ ਲੋਕ, ਲੰਗਰ ਛਕਾ ਰਹੇ।\nPeople doing seva in Gurdwara, serving langar.",
                "type": "scenario"
            },
            {
                "id": "wedding_celebration",
                "text": "[SCENE 1: Wedding]\nਵਿਆਹ ਦੀ ਰੌਣਕ, ਖੁਸ਼ੀਆਂ ਹੀ ਖੁਸ਼ੀਆਂ।\nWedding celebration, joy everywhere.",
                "type": "scenario"
            },
            {
                "id": "harvest_festival",
                "text": "[SCENE 1: Fields]\nਵਿਸਾਖੀ ਦਾ ਤਿਉਹਾਰ, ਫਸਲ ਕੱਟਣ ਦੀ ਖੁਸ਼ੀ।\nVaisakhi festival, joy of harvest.",
                "type": "scenario"
            },
            {
                "id": "grandma_stories",
                "text": "[SCENE 1: Home]\nਦਾਦੀ ਕਹਾਣੀਆਂ ਸੁਣਾ ਰਹੀ, ਬੱਚੇ ਸੁਣ ਰਹੇ।\nGrandmother telling stories, children listening.",
                "type": "scenario"
            }
        ]
        
        patterns['spiritual'] = [
            {
                "id": "morning_prayer",
                "text": "[SCENE 1: Morning]\nਜਪੁਜੀ ਸਾਹਿਬ ਦਾ ਪਾਠ, ਸਵੇਰੇ ਦਾ ਸਮਾਂ।\nJapji Sahib path, morning time.",
                "type": "scenario"
            },
            {
                "id": "evening_rehraas",
                "text": "[SCENE 1: Evening]\nਰਹਿਰਾਸ ਸਾਹਿਬ ਪੜ੍ਹਦੇ, ਦੀਵੇ ਬਲਦੇ।\nReading Rehraas Sahib, lamps glowing.",
                "type": "scenario"
            }
        ]
        
        total_patterns = sum(len(v) for v in patterns.values())
        log.info(f"✅ Pattern library built: {total_patterns} total patterns")
        
        return patterns
    
    def assign_patterns_to_agents(self):
        """Assign different patterns to different agents"""
        log.info("🎯 Assigning patterns to agents...")
        
        agent_assignments = {}
        
        # Agent 1: Gurbani + Spiritual
        agent_assignments['agent_1_spiritual'] = {
            "patterns": self.pattern_library['gurbani'][:10] + self.pattern_library['spiritual'],
            "focus": "Spiritual and Gurbani content",
            "max_videos": 30
        }
        
        # Agent 2: Culture + Family
        agent_assignments['agent_2_culture'] = {
            "patterns": self.pattern_library['punjabi_culture'] + self.pattern_library['family_stories'][:5],
            "focus": "Punjabi culture and family stories",
            "max_videos": 30
        }
        
        # Agent 3: History + Daily Life
        agent_assignments['agent_3_life'] = {
            "patterns": self.pattern_library['historical'][:5] + self.pattern_library['daily_life'][:5],
            "focus": "Historical and daily life scenarios",
            "max_videos": 20
        }
        
        # Agent 4: Tech Learning
        agent_assignments['agent_4_tech'] = {
            "patterns": [
                {
                    "id": "computer_learning",
                    "text": "[SCENE 1: Computer]\nਕੰਪਿਊਟਰ ਸਿੱਖਣਾ ਬਹੁਤ ਜ਼ਰੂਰੀ ਹੈ।\nLearning computer is important.",
                    "type": "scenario"
                }
            ],
            "focus": "Technology and learning",
            "max_videos": 20
        }
        
        log.info(f"✅ Assigned patterns to {len(agent_assignments)} agents")
        return agent_assignments
    
    def cleanup_old_videos(self):
        """Auto-delete old training videos when limit reached"""
        video_files = list(self.workspace.glob("training_video*.mp4"))
        video_count = len(video_files)
        
        log.info(f"📊 Current training videos: {video_count}")
        
        if video_count > self.cleanup_threshold:
            log.warning(f"⚠️ Cleanup threshold reached: {video_count} > {self.cleanup_threshold}")
            
            # Sort by modification time (oldest first)
            video_files.sort(key=lambda x: x.stat().st_mtime)
            
            # Calculate how many to delete
            to_delete = video_count - self.max_training_videos
            
            if to_delete > 0:
                log.info(f"🗑️ Deleting {to_delete} oldest videos...")
                
                deleted = 0
                for video_file in video_files[:to_delete]:
                    try:
                        video_file.unlink()
                        deleted += 1
                    except Exception as e:
                        log.error(f"❌ Could not delete {video_file.name}: {e}")
                
                log.info(f"✅ Deleted {deleted} videos. Remaining: {video_count - deleted}")
                return deleted
        
        return 0
    
    def run_rahbar_ai_guidance(self):
        """Run Rahbar AI for system guidance"""
        log.info("🧠 Consulting Rahbar AI for guidance...")
        
        try:
            rahbar_file = self.workspace / "RAHBAR_AI_DEVELOPER.py"
            if rahbar_file.exists():
                result = subprocess.run(
                    [sys.executable, str(rahbar_file), "--scan"],
                    cwd=self.workspace,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    log.info("✅ Rahbar AI guidance received")
                    return True
                else:
                    log.warning(f"⚠️ Rahbar AI returned code {result.returncode}")
            else:
                log.warning("⚠️ Rahbar AI not found")
        except Exception as e:
            log.error(f"❌ Rahbar AI error: {e}")
        
        return False
    
    def start_training_agent(self, agent_name: str, patterns: List[Dict], max_videos: int = 20):
        """Start a training agent with specific patterns"""
        log.info(f"🚀 Starting agent: {agent_name}")
        log.info(f"   Patterns: {len(patterns)}")
        log.info(f"   Max videos: {max_videos}")
        
        # Create agent config
        agent_config = {
            "agent_name": agent_name,
            "patterns": patterns,
            "max_videos": max_videos,
            "started_at": datetime.now().isoformat()
        }
        
        config_file = self.workspace / f"{agent_name}_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(agent_config, f, indent=2, ensure_ascii=False)
        
        try:
            # Start autonomous learning agent with this config
            process = subprocess.Popen(
                [
                    sys.executable,
                    str(self.workspace / "autonomous_learning_agent.py"),
                    "--mode", "limited",
                    "--max-videos", str(max_videos),
                    "--config", str(config_file)
                ],
                cwd=self.workspace,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.running_agents[agent_name] = {
                "process": process,
                "config": agent_config,
                "started_at": datetime.now()
            }
            
            log.info(f"✅ Agent {agent_name} started (PID: {process.pid})")
            return True
            
        except Exception as e:
            log.error(f"❌ Failed to start agent {agent_name}: {e}")
            return False
    
    def monitor_agents(self):
        """Monitor running agents"""
        log.info("👁️ Monitoring agents...")
        
        for agent_name, agent_info in list(self.running_agents.items()):
            process = agent_info['process']
            
            # Check if process is still running
            if process.poll() is not None:
                log.info(f"✅ Agent {agent_name} completed")
                del self.running_agents[agent_name]
            else:
                runtime = (datetime.now() - agent_info['started_at']).seconds / 60
                log.info(f"   {agent_name}: Running for {runtime:.1f} minutes")
    
    def orchestrate(self, duration_hours: int = 24):
        """Main orchestration loop"""
        log.info("=" * 80)
        log.info("🎯 MASTER TRAINING ORCHESTRATOR STARTING")
        log.info("=" * 80)
        log.info(f"⏰ Duration: {duration_hours} hours")
        log.info(f"🎬 Max training videos: {self.max_training_videos}")
        log.info(f"🗑️ Cleanup threshold: {self.cleanup_threshold}")
        log.info("")
        
        start_time = datetime.now()
        end_time = start_time.timestamp() + (duration_hours * 3600)
        
        cycle = 0
        
        try:
            while datetime.now().timestamp() < end_time:
                cycle += 1
                log.info("")
                log.info(f"🔄 CYCLE {cycle} - {datetime.now().strftime('%H:%M:%S')}")
                log.info("-" * 60)
                
                # 1. Check and cleanup old videos
                deleted = self.cleanup_old_videos()
                
                # 2. Consult Rahbar AI every 6 hours
                if cycle % 12 == 1:  # Every 12 cycles (assuming 30 min per cycle)
                    self.run_rahbar_ai_guidance()
                
                # 3. Assign patterns to agents
                agent_assignments = self.assign_patterns_to_agents()
                
                # 4. Start agents if not running
                for agent_name, assignment in agent_assignments.items():
                    if agent_name not in self.running_agents:
                        self.start_training_agent(
                            agent_name,
                            assignment['patterns'],
                            assignment['max_videos']
                        )
                
                # 5. Monitor running agents
                self.monitor_agents()
                
                # 6. Wait before next cycle
                log.info(f"😴 Sleeping 30 minutes until next cycle...")
                time.sleep(1800)  # 30 minutes
                
        except KeyboardInterrupt:
            log.info("\n⚠️ Keyboard interrupt received")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Graceful shutdown"""
        log.info("")
        log.info("🛑 SHUTTING DOWN ORCHESTRATOR")
        log.info("-" * 60)
        
        # Stop all running agents
        for agent_name, agent_info in self.running_agents.items():
            process = agent_info['process']
            log.info(f"   Stopping {agent_name} (PID: {process.pid})...")
            try:
                process.terminate()
                process.wait(timeout=10)
                log.info(f"   ✅ {agent_name} stopped")
            except Exception as e:
                log.error(f"   ❌ Error stopping {agent_name}: {e}")
                process.kill()
        
        log.info("")
        log.info("✅ Orchestrator shutdown complete")
        log.info("ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ! 🙏")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Master Training Orchestrator')
    parser.add_argument('--hours', type=int, default=24,
                       help='Duration to run (hours)')
    parser.add_argument('--max-videos', type=int, default=100,
                       help='Max training videos to keep')
    parser.add_argument('--cleanup-threshold', type=int, default=150,
                       help='Cleanup when this many videos reached')
    
    args = parser.parse_args()
    
    orchestrator = MasterTrainingOrchestrator()
    orchestrator.max_training_videos = args.max_videos
    orchestrator.cleanup_threshold = args.cleanup_threshold
    
    orchestrator.orchestrate(duration_hours=args.hours)


if __name__ == "__main__":
    main()
