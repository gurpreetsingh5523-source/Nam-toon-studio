#!/usr/bin/env python3
"""
📚 LEARNING FEED FOR RAHBAR AI
ਰਾਹਬਰ AI ਨੂੰ ਸਿੱਖਣ ਲਈ ਡਾਟਾ

This file teaches Rahbar AI what we learned from debugging:
ਇਹ ਫਾਈਲ Rahbar AI ਨੂੰ ਸਿਖਾਉਂਦੀ ਹੈ ਕਿ ਅਸੀਂ debugging ਤੋਂ ਕੀ ਸਿੱਖਿਆ
"""

import json
from pathlib import Path
from datetime import datetime

LEARNING_DATA = {
    "timestamp": datetime.now().isoformat(),
    "teacher": "Human Developer",
    "student": "Rahbar AI Developer",
    
    "lessons_learned": [
        {
            "lesson_id": 1,
            "title": "Agent Configuration Loading Issue",
            "problem": "Agents were stuck in TN (stopped) state, no videos created",
            "root_cause": "autonomous_learning_agent.py didn't properly load custom config files",
            "symptoms": [
                "Processes running but CPU 0.0%",
                "Status: TN (stopped/waiting)",
                "No videos created",
                "Config files created but not loaded"
            ],
            "solution": "Need to add config loading logic in autonomous_learning_agent.py main() function",
            "code_pattern": """
# BEFORE (broken):
def main():
    agent = AutonomousLearningAgent()
    # Config never loaded!

# AFTER (working):
def main():
    args = parser.parse_args()
    agent = AutonomousLearningAgent()
    
    # Load custom config if provided
    if args.config:
        import json
        with open(args.config, 'r') as f:
            custom_config = json.load(f)
            if 'patterns' in custom_config:
                agent.training_scenarios = custom_config['patterns']
""",
            "importance": "CRITICAL",
            "lesson": "Always verify config loading works BEFORE spawning multiple processes"
        },
        
        {
            "lesson_id": 2,
            "title": "Testing Before Deployment",
            "problem": "Launched 4 agents without testing if one works",
            "root_cause": "Assumed code would work without validation",
            "solution": "Always test with 1 agent first, then scale up",
            "code_pattern": """
# WRONG: Launch all at once
for agent in all_agents:
    start_agent(agent)  # If broken, all fail!

# RIGHT: Test first
test_agent = agents[0]
if test_agent_works():
    for agent in all_agents:
        start_agent(agent)
else:
    fix_issues_first()
""",
            "importance": "HIGH",
            "lesson": "Test small, then scale. Don't assume."
        },
        
        {
            "lesson_id": 3,
            "title": "Process State Monitoring",
            "problem": "Processes showed 'TN' state but we didn't catch it early",
            "root_cause": "No proactive monitoring of process health",
            "solution": "Add process state checking in orchestrator",
            "code_pattern": """
def monitor_agent_health(process):
    # Check CPU usage
    if process.cpu_percent() == 0.0:
        log.warning(f"Agent {process.pid} has 0% CPU - may be stuck!")
    
    # Check state (T = stopped, S = sleeping, R = running)
    state = get_process_state(process.pid)
    if state in ['T', 'TN']:
        log.error(f"Agent {process.pid} is in stopped state!")
        restart_agent(process)
""",
            "importance": "HIGH",
            "lesson": "Monitor process health actively, not just assume it's working"
        },
        
        {
            "lesson_id": 4,
            "title": "Simplicity Over Complexity",
            "problem": "Complex orchestrator with 4 agents, configs, patterns - too many moving parts",
            "root_cause": "Tried to do everything at once",
            "solution": "Create simple_working_agent.py - minimal, works reliably",
            "code_pattern": """
# COMPLEX (breaks easily):
- Master orchestrator
- 4 different agents
- Config files for each
- Pattern library loading
- Custom scenario injection
= Too many failure points!

# SIMPLE (reliable):
class SimpleAgent:
    def __init__(self):
        self.maker = RealisticMovieMaker()
        self.scenarios = [5 hardcoded scenarios]
    
    def create_one_video(self):
        scenario = random.choice(self.scenarios)
        self.maker.create_movie(scenario['story'], name)
        
= Works every time!
""",
            "importance": "CRITICAL",
            "lesson": "Start simple. Add complexity only when simple version works perfectly."
        },
        
        {
            "lesson_id": 5,
            "title": "Method Name Mismatch",
            "problem": "autonomous_learning_agent calls video_maker.create_video() but integrated_smart_video_maker doesn't have that method",
            "root_cause": "Assumed method names without checking API",
            "symptoms": [
                "AttributeError: 'IntegratedSmartVideoMaker' object has no attribute 'create_video'",
                "Agent crashes silently",
                "No error shown to user"
            ],
            "solution": "Check actual API of classes before calling",
            "code_pattern": """
# WRONG (assumed):
video_maker.create_video(text=story)

# RIGHT (actual API):
# Check realistic_movie_maker.py:
def create_movie(self, story_text, output_name):
    # This is the real method!

# So use:
video_maker.create_movie(story, video_name)
""",
            "importance": "HIGH",
            "lesson": "Never assume method names. Always check the actual class definition."
        },
        
        {
            "lesson_id": 6,
            "title": "Data Flow Understanding",
            "problem": "User wants existing data (brain files, gurbani) used in training",
            "solution": "Pattern library builder that loads from existing files",
            "implementation": """
def _build_pattern_library(self):
    patterns = {}
    
    # 1. Load brain files
    brain_files = list(self.workspace.glob('brain_*.txt'))
    for brain_file in brain_files:
        content = brain_file.read_text(encoding='utf-8')[:1000]
        patterns['category'].append({
            'source': brain_file.name,
            'content': content,
            'type': 'text'
        })
    
    # 2. Load gurbani JSON
    gurbani_json = self.workspace / 'gurbani_knowledge.json'
    if gurbani_json.exists():
        data = json.load(gurbani_json.open())
        patterns['gurbani'].extend(data)
    
    return patterns
""",
            "importance": "MEDIUM",
            "lesson": "User's existing data is valuable - make sure to USE it, not ignore it"
        },
        
        {
            "lesson_id": 7,
            "title": "Auto-Cleanup Logic",
            "problem": "Training videos accumulate, user wants automatic deletion",
            "solution": "Implement smart cleanup with thresholds",
            "code_pattern": """
def cleanup_old_videos(self):
    video_files = list(workspace.glob('training_video*.mp4'))
    video_count = len(video_files)
    
    if video_count > self.cleanup_threshold:
        # Sort by modification time (oldest first)
        video_files.sort(key=lambda x: x.stat().st_mtime)
        
        # Keep newest N videos
        to_delete = video_count - self.max_training_videos
        
        for video_file in video_files[:to_delete]:
            video_file.unlink()  # Delete
            
        log.info(f'Deleted {to_delete} old videos')
""",
            "importance": "MEDIUM",
            "lesson": "Automate maintenance tasks. Don't let system fill up."
        },
        
        {
            "lesson_id": 8,
            "title": "User Feedback Integration",
            "problem": "User said 'eh kamm ni kar ria' - agents not working",
            "user_observation": "Checked and saw 0.0% CPU, TN state, no videos",
            "correct_response": [
                "Stop all stuck processes immediately",
                "Diagnose why they're stuck",
                "Create simpler working version",
                "Test before redeploying"
            ],
            "importance": "CRITICAL",
            "lesson": "When user says 'not working', believe them! Check immediately, don't assume."
        }
    ],
    
    "patterns_to_remember": {
        "process_debugging": {
            "check_cpu": "ps aux | grep <process> shows CPU usage",
            "check_state": "Status column shows T/S/R (stopped/sleeping/running)",
            "check_output": "tail -f logfile to see what process is doing",
            "check_errors": "Look for exceptions in logs"
        },
        
        "testing_workflow": {
            "step1": "Write minimal test case",
            "step2": "Run test case manually",
            "step3": "Verify it works",
            "step4": "Only then automate",
            "step5": "Scale up gradually"
        },
        
        "code_architecture": {
            "simple_first": "Build simplest version that works",
            "add_features": "Add one feature at a time",
            "test_each": "Test after each addition",
            "dont_assume": "Verify every assumption"
        }
    },
    
    "future_improvements": [
        {
            "id": 1,
            "task": "Fix autonomous_learning_agent.py config loading",
            "priority": "URGENT",
            "complexity": "LOW",
            "estimated_time": "30 minutes",
            "approach": "Add config file loading logic in main() function"
        },
        {
            "id": 2,
            "task": "Add process health monitoring to orchestrator",
            "priority": "HIGH",
            "complexity": "MEDIUM",
            "estimated_time": "1 hour",
            "approach": "Check CPU%, state, and restart if stuck"
        },
        {
            "id": 3,
            "task": "Create working agent that actually produces videos",
            "priority": "URGENT",
            "complexity": "LOW",
            "estimated_time": "30 minutes",
            "approach": "Use simple_working_agent.py as template"
        },
        {
            "id": 4,
            "task": "Test video creation end-to-end before automation",
            "priority": "CRITICAL",
            "complexity": "LOW",
            "estimated_time": "15 minutes",
            "approach": "Run python3 simple_working_agent.py --videos 2"
        }
    ],
    
    "code_templates": {
        "simple_agent_pattern": """
class SimpleAgent:
    def __init__(self):
        self.maker = RealisticMovieMaker()
        self.scenarios = [list of scenarios]
    
    def create_one(self, index):
        scenario = self.scenarios[index]
        return self.maker.create_movie(scenario['story'], name)
    
    def run_batch(self, count):
        for i in range(count):
            self.create_one(i)
""",
        
        "process_health_check": """
def is_process_healthy(pid):
    try:
        proc = psutil.Process(pid)
        cpu = proc.cpu_percent(interval=1.0)
        status = proc.status()
        
        if cpu == 0.0 and status in ['stopped', 'zombie']:
            return False
        return True
    except:
        return False
""",
        
        "config_loader": """
def load_agent_config(config_file):
    if not config_file or not Path(config_file).exists():
        return None
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    return config
"""
    },
    
    "rahbar_ai_tasks": [
        "Read this learning data",
        "Understand what went wrong",
        "Generate fixed version of autonomous_learning_agent.py",
        "Create process monitoring system",
        "Build simple working agent",
        "Test everything before deployment",
        "Report back with results"
    ]
}


def save_learning_data():
    """Save learning data to file for Rahbar AI"""
    workspace = Path(__file__).parent
    output_file = workspace / "rahbar_learning_feed.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(LEARNING_DATA, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Learning data saved: {output_file}")
    print(f"📚 Total lessons: {len(LEARNING_DATA['lessons_learned'])}")
    print(f"🎯 Future improvements: {len(LEARNING_DATA['future_improvements'])}")
    print(f"\n👨‍💻 Rahbar AI can now read and learn from this!")
    
    return output_file


if __name__ == "__main__":
    save_learning_data()
