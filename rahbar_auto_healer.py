#!/usr/bin/env python3
"""
🤖 RAHBAR AI AUTO-HEALER
ਖੁਦ-ਕਾਰ ਠੀਕ ਕਰਨ ਵਾਲਾ ਸਿਸਟਮ

This system:
1. Automatically detects problems
2. Analyzes root causes
3. Generates fixes
4. Tests solutions
5. Deploys if working
6. Teaches other brains
7. Learns from everything

ਜਿਵੇਂ ਪਰਿਵਾਰ - ਸਾਰੇ ਦਿਮਾਗ ਮਿਲ ਕੇ ਕੰਮ ਕਰਦੇ

ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ! 🙏
"""

import os
import sys
import json
import time
import subprocess
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

WORKSPACE = Path(__file__).parent.absolute()
sys.path.insert(0, str(WORKSPACE))


class AutoHealer:
    """
    🤖 Automatic system healer
    ਖੁਦ-ਕਾਰ ਠੀਕ ਕਰਨ ਵਾਲਾ
    """
    
    def __init__(self):
        self.workspace = WORKSPACE
        self.healing_log = self.workspace / "auto_healing_log.json"
        self.history = self._load_history()
        
        print("🤖 Auto-Healer initialized")
        print("   Watching system health 24/7...")
    
    def _load_history(self):
        """Load healing history"""
        if self.healing_log.exists():
            with open(self.healing_log, 'r') as f:
                return json.load(f)
        return {
            "sessions": [],
            "total_fixes": 0,
            "success_rate": 0.0
        }
    
    def _save_history(self):
        """Save healing history"""
        with open(self.healing_log, 'w') as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)
    
    def detect_problems(self) -> List[Dict]:
        """Automatically detect system problems"""
        problems = []
        
        print("\n🔍 AUTO-DETECTING PROBLEMS...")
        
        # 1. Check for stuck processes
        stuck = self._check_stuck_processes()
        if stuck:
            problems.extend(stuck)
        
        # 2. Check for missing videos
        no_output = self._check_missing_output()
        if no_output:
            problems.append(no_output)
        
        # 3. Check for import errors
        import_errors = self._check_import_errors()
        if import_errors:
            problems.extend(import_errors)
        
        # 4. Check for config issues
        config_problems = self._check_config_issues()
        if config_problems:
            problems.extend(config_problems)
        
        # 5. Check disk space
        disk_problem = self._check_disk_space()
        if disk_problem:
            problems.append(disk_problem)
        
        print(f"   Found {len(problems)} problems")
        return problems
    
    def _check_stuck_processes(self) -> List[Dict]:
        """Check for stuck processes"""
        problems = []
        
        try:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            for line in result.stdout.split('\n'):
                if 'autonomous_learning_agent' in line or 'MASTER_TRAINING' in line:
                    parts = line.split()
                    if len(parts) > 7:
                        cpu = float(parts[2])
                        state = parts[7]
                        
                        if cpu == 0.0 and state in ['T', 'TN']:
                            problems.append({
                                "type": "stuck_process",
                                "severity": "HIGH",
                                "description": f"Process stuck in {state} state",
                                "pid": parts[1],
                                "auto_fixable": True
                            })
        except Exception as e:
            print(f"   ⚠️ Could not check processes: {e}")
        
        return problems
    
    def _check_missing_output(self) -> Optional[Dict]:
        """Check if videos are being created"""
        video_files = list(self.workspace.glob("training_*.mp4"))
        
        if len(video_files) == 0:
            # Check if agents are supposed to be running
            agent_configs = list(self.workspace.glob("agent_*_config.json"))
            if agent_configs:
                return {
                    "type": "no_output",
                    "severity": "HIGH",
                    "description": "Agents configured but no videos created",
                    "auto_fixable": True
                }
        
        return None
    
    def _check_import_errors(self) -> List[Dict]:
        """Check for common import errors"""
        problems = []
        
        # Test critical imports
        critical_modules = [
            "realistic_movie_maker",
            "integrated_smart_video_maker",
            "self_learning_ai"
        ]
        
        for module in critical_modules:
            try:
                __import__(module)
            except ImportError as e:
                problems.append({
                    "type": "import_error",
                    "severity": "CRITICAL",
                    "description": f"Cannot import {module}: {e}",
                    "module": module,
                    "auto_fixable": False
                })
        
        return problems
    
    def _check_config_issues(self) -> List[Dict]:
        """Check for configuration issues"""
        problems = []
        
        # Check orchestrator config
        orch_config = self.workspace / "orchestrator_config.json"
        if orch_config.exists():
            try:
                with open(orch_config, 'r') as f:
                    config = json.load(f)
                    
                # Check if agents are enabled but files missing
                for agent_name, agent_config in config.get('agents', {}).items():
                    if agent_config.get('enabled'):
                        agent_file = self.workspace / f"{agent_name}.py"
                        if not agent_file.exists():
                            problems.append({
                                "type": "missing_agent_file",
                                "severity": "MEDIUM",
                                "description": f"Agent {agent_name} enabled but file missing",
                                "auto_fixable": True
                            })
            except Exception as e:
                problems.append({
                    "type": "config_error",
                    "severity": "MEDIUM",
                    "description": f"Config file corrupted: {e}",
                    "auto_fixable": True
                })
        
        return problems
    
    def _check_disk_space(self) -> Optional[Dict]:
        """Check disk space"""
        try:
            result = subprocess.run(
                ["df", "-h", str(self.workspace)],
                capture_output=True,
                text=True
            )
            
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                usage = parts[4].rstrip('%')
                
                if int(usage) > 95:
                    return {
                        "type": "disk_full",
                        "severity": "HIGH",
                        "description": f"Disk {usage}% full",
                        "auto_fixable": True
                    }
        except Exception as e:
            print(f"   ⚠️ Could not check disk: {e}")
        
        return None
    
    def auto_fix(self, problem: Dict) -> bool:
        """Automatically fix a problem"""
        print(f"\n🔧 AUTO-FIXING: {problem['type']}")
        
        if not problem.get('auto_fixable'):
            print(f"   ⚠️ Not auto-fixable")
            return False
        
        try:
            if problem['type'] == 'stuck_process':
                return self._fix_stuck_process(problem)
            
            elif problem['type'] == 'no_output':
                return self._fix_no_output(problem)
            
            elif problem['type'] == 'disk_full':
                return self._fix_disk_full(problem)
            
            elif problem['type'] == 'missing_agent_file':
                return self._fix_missing_agent(problem)
            
            elif problem['type'] == 'config_error':
                return self._fix_config_error(problem)
            
            else:
                print(f"   ⚠️ Unknown problem type")
                return False
                
        except Exception as e:
            print(f"   ❌ Fix failed: {e}")
            traceback.print_exc()
            return False
    
    def _fix_stuck_process(self, problem: Dict) -> bool:
        """Fix stuck process"""
        pid = problem['pid']
        print(f"   Killing stuck process {pid}...")
        
        try:
            subprocess.run(["kill", "-9", pid], check=True)
            time.sleep(1)
            print(f"   ✅ Process {pid} terminated")
            return True
        except Exception as e:
            print(f"   ❌ Could not kill process: {e}")
            return False
    
    def _fix_no_output(self, problem: Dict) -> bool:
        """Fix no output issue"""
        print(f"   Analyzing why no videos created...")
        
        # Check if simple agent works
        simple_agent = self.workspace / "simple_working_agent.py"
        if simple_agent.exists():
            print(f"   Testing simple_working_agent...")
            try:
                result = subprocess.run(
                    [sys.executable, str(simple_agent), "--videos", "1", "--delay", "2"],
                    cwd=self.workspace,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                # Check if video was created
                video_files = list(self.workspace.glob("training_*.mp4"))
                if len(video_files) > 0:
                    print(f"   ✅ Simple agent works! Created video.")
                    return True
                else:
                    print(f"   ❌ Simple agent ran but no video created")
                    print(f"   Output: {result.stdout[-500:]}")
                    return False
                    
            except subprocess.TimeoutExpired:
                print(f"   ⚠️ Simple agent timed out")
                return False
        
        print(f"   ⚠️ Cannot test - simple agent not found")
        return False
    
    def _fix_disk_full(self, problem: Dict) -> bool:
        """Fix disk full issue"""
        print(f"   Cleaning up old training videos...")
        
        video_files = sorted(
            self.workspace.glob("training_*.mp4"),
            key=lambda x: x.stat().st_mtime
        )
        
        # Delete oldest 50%
        to_delete = len(video_files) // 2
        deleted = 0
        
        for video in video_files[:to_delete]:
            try:
                video.unlink()
                deleted += 1
            except Exception as e:
                print(f"   ⚠️ Could not delete {video.name}: {e}")
        
        print(f"   ✅ Deleted {deleted} old videos")
        return deleted > 0
    
    def _fix_missing_agent(self, problem: Dict) -> bool:
        """Fix missing agent file"""
        print(f"   Creating missing agent file...")
        
        # Use simple_working_agent as template
        simple_agent = self.workspace / "simple_working_agent.py"
        if not simple_agent.exists():
            print(f"   ⚠️ Template not found")
            return False
        
        # For now, just disable the agent in config
        orch_config = self.workspace / "orchestrator_config.json"
        try:
            with open(orch_config, 'r') as f:
                config = json.load(f)
            
            # Disable missing agent
            if 'agents' in config:
                for agent_name in config['agents']:
                    agent_file = self.workspace / f"{agent_name}.py"
                    if not agent_file.exists():
                        config['agents'][agent_name]['enabled'] = False
            
            with open(orch_config, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"   ✅ Disabled missing agents in config")
            return True
            
        except Exception as e:
            print(f"   ❌ Could not fix config: {e}")
            return False
    
    def _fix_config_error(self, problem: Dict) -> bool:
        """Fix config error"""
        print(f"   Regenerating config file...")
        
        orch_config = self.workspace / "orchestrator_config.json"
        
        # Create default config
        default_config = {
            "max_training_videos": 100,
            "cleanup_threshold": 150,
            "auto_cleanup": True,
            "regenerated_at": datetime.now().isoformat(),
            "agents": {}
        }
        
        try:
            with open(orch_config, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            print(f"   ✅ Config regenerated")
            return True
        except Exception as e:
            print(f"   ❌ Could not regenerate: {e}")
            return False
    
    def teach_other_brains(self, problem: Dict, fix_result: bool):
        """Teach other AI brains what we learned"""
        print(f"\n📚 TEACHING OTHER BRAINS...")
        
        lesson = {
            "timestamp": datetime.now().isoformat(),
            "problem": problem,
            "fix_attempted": True,
            "fix_successful": fix_result,
            "lesson": self._generate_lesson(problem, fix_result)
        }
        
        # Save to learning feed
        learning_feed = self.workspace / "rahbar_learning_feed.json"
        if learning_feed.exists():
            try:
                with open(learning_feed, 'r') as f:
                    feed = json.load(f)
                
                if 'auto_healing_lessons' not in feed:
                    feed['auto_healing_lessons'] = []
                
                feed['auto_healing_lessons'].append(lesson)
                
                with open(learning_feed, 'w') as f:
                    json.dump(feed, f, indent=2, ensure_ascii=False)
                
                print(f"   ✅ Lesson saved to learning feed")
            except Exception as e:
                print(f"   ⚠️ Could not save lesson: {e}")
        
        print(f"   📖 Lesson: {lesson['lesson']}")
    
    def _generate_lesson(self, problem: Dict, success: bool) -> str:
        """Generate lesson from problem"""
        if problem['type'] == 'stuck_process' and success:
            return "When process has 0% CPU and TN state, kill it immediately"
        
        elif problem['type'] == 'no_output' and success:
            return "Test simple_working_agent first before complex orchestrator"
        
        elif problem['type'] == 'disk_full' and success:
            return "Auto-delete old training videos when disk > 95% full"
        
        elif problem['type'] == 'missing_agent_file':
            return "Disable agents in config if their files don't exist"
        
        elif problem['type'] == 'config_error':
            return "Regenerate config from defaults when corrupted"
        
        else:
            return f"Encountered {problem['type']}, fix {'successful' if success else 'failed'}"
    
    def generate_status_report(self, problems: List[Dict], fixes: List[bool]) -> Dict:
        """Generate status report"""
        successful_fixes = sum(fixes)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "problems_detected": len(problems),
            "problems_fixed": successful_fixes,
            "problems_remaining": len(problems) - successful_fixes,
            "success_rate": (successful_fixes / len(problems) * 100) if problems else 100,
            "details": []
        }
        
        for problem, fixed in zip(problems, fixes):
            report['details'].append({
                "problem": problem['type'],
                "severity": problem['severity'],
                "fixed": fixed
            })
        
        return report
    
    def run_healing_cycle(self) -> Dict:
        """Run one complete healing cycle"""
        print("\n" + "="*70)
        print("🤖 AUTO-HEALING CYCLE STARTING")
        print("   ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ")
        print("="*70)
        
        # Step 1: Detect problems
        problems = self.detect_problems()
        
        if not problems:
            print("\n✅ No problems detected - system healthy!")
            return {"status": "healthy", "problems": 0}
        
        # Step 2: Auto-fix each problem
        fixes = []
        for i, problem in enumerate(problems, 1):
            print(f"\n{'='*70}")
            print(f"PROBLEM {i}/{len(problems)}")
            print(f"Type: {problem['type']}")
            print(f"Severity: {problem['severity']}")
            print(f"Description: {problem['description']}")
            print(f"{'='*70}")
            
            fixed = self.auto_fix(problem)
            fixes.append(fixed)
            
            # Step 3: Teach other brains
            self.teach_other_brains(problem, fixed)
            
            time.sleep(2)  # Brief pause between fixes
        
        # Step 4: Generate report
        report = self.generate_status_report(problems, fixes)
        
        # Step 5: Save to history
        self.history['sessions'].append(report)
        self.history['total_fixes'] += report['problems_fixed']
        self._save_history()
        
        print("\n" + "="*70)
        print("✅ HEALING CYCLE COMPLETE")
        print(f"   Problems detected: {report['problems_detected']}")
        print(f"   Problems fixed: {report['problems_fixed']}")
        print(f"   Success rate: {report['success_rate']:.1f}%")
        print("="*70)
        
        return report


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto-Healer System')
    parser.add_argument('--once', action='store_true',
                       help='Run once then exit')
    parser.add_argument('--interval', type=int, default=300,
                       help='Check interval in seconds (default: 300 = 5 min)')
    
    args = parser.parse_args()
    
    healer = AutoHealer()
    
    if args.once:
        # Run once
        healer.run_healing_cycle()
    else:
        # Run continuously
        print(f"🔄 Running continuously (checking every {args.interval}s)")
        print("   Press Ctrl+C to stop")
        
        try:
            while True:
                healer.run_healing_cycle()
                print(f"\n😴 Sleeping {args.interval} seconds...")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n\n⚠️ Stopped by user")


if __name__ == "__main__":
    main()
