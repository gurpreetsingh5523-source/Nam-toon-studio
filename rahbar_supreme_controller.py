#!/usr/bin/env python3
"""
👑 RAHBAR AI SUPREME CONTROLLER
ਰਾਹਬਰ AI ਸੁਪਰੀਮ - ਸਭ ਕੁੱਝ ਆਪਣੇ ਆਪ ਕਰੇ

ਇਹ Rahbar AI:
1. ✅ System check ਆਪਣੇ ਆਪ ਕਰੇ
2. 🔍 Problems ਲੱਭੇ (stuck agents, missing files, errors)
3. 🔧 Auto fix ਕਰੇ (ਕੋਡ ਠੀਕ, dependencies install)
4. 🎬 Videos ਬਣਾਏ (commands ਦੇ ਕੇ agents ਨੂੰ)
5. 🎓 Training ਦੇਵੇ (ਦੂਜੇ systems ਨੂੰ ਸਿਖਾਏ)
6. 📊 Reports ਬਣਾਏ (ਕੀ ਕੀਤਾ, ਕਿੰਨੇ videos)

ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ! 🙏
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

WORKSPACE = Path(__file__).parent
sys.path.insert(0, str(WORKSPACE))

class RahbarSupremeController:
    """
    Supreme Rahbar AI that manages everything automatically
    """
    
    def __init__(self):
        self.workspace = WORKSPACE
        self.log_file = self.workspace / "rahbar_supreme_log.json"
        self.command_history = []
        self.problems_found = []
        self.fixes_applied = []
        self.videos_created = []
        self.training_sessions = []
        
        print("👑 Rahbar Supreme Controller initialized")
        print(f"📂 Workspace: {self.workspace}")
    
    def log_action(self, action_type: str, details: Dict[str, Any]):
        """Log every action"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "details": details
        }
        
        # Load existing log
        log_data = {"actions": []}
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
        
        log_data["actions"].append(entry)
        
        # Save updated log
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
    
    def run_command(self, command: str, description: str, timeout: int = 60) -> Dict[str, Any]:
        """Run a command and return result"""
        print(f"\n💻 Running: {description}")
        print(f"   Command: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = result.returncode == 0
            output = result.stdout if success else result.stderr
            
            cmd_result = {
                "command": command,
                "description": description,
                "success": success,
                "return_code": result.returncode,
                "output": output[:500] if output else "",  # Limit output
                "timestamp": datetime.now().isoformat()
            }
            
            self.command_history.append(cmd_result)
            self.log_action("command_executed", cmd_result)
            
            if success:
                print(f"   ✅ Success!")
            else:
                print(f"   ❌ Failed (code {result.returncode})")
            
            return cmd_result
            
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Timeout after {timeout}s")
            return {
                "command": command,
                "description": description,
                "success": False,
                "error": "timeout",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return {
                "command": command,
                "description": description,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def check_system_health(self) -> Dict[str, Any]:
        """Check entire system health"""
        print("\n" + "="*70)
        print("🏥 SYSTEM HEALTH CHECK")
        print("="*70)
        
        health = {
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # 1. Check Python version
        result = self.run_command("python3 --version", "Python version check", timeout=5)
        health["checks"]["python"] = result["success"]
        
        # 2. Check critical files
        critical_files = [
            "simple_working_agent.py",
            "realistic_movie_maker.py",
            "ai_family_system.py",
            "rahbar_auto_healer.py",
            "rahbar_auto_learner.py"
        ]
        
        missing_files = []
        for file in critical_files:
            if not (self.workspace / file).exists():
                missing_files.append(file)
        
        health["checks"]["critical_files"] = len(missing_files) == 0
        health["missing_files"] = missing_files
        
        if missing_files:
            print(f"   ⚠️ Missing files: {missing_files}")
            self.problems_found.append({
                "type": "missing_files",
                "files": missing_files,
                "severity": "HIGH"
            })
        
        # 3. Check for stuck processes
        result = self.run_command(
            "ps aux | grep -E 'python.*agent' | grep -v grep",
            "Check for running agents",
            timeout=5
        )
        
        if result["success"] and result["output"]:
            # Check if any are stuck (TN state)
            if " TN " in result["output"] or " T " in result["output"]:
                print(f"   ⚠️ Found stuck processes!")
                self.problems_found.append({
                    "type": "stuck_processes",
                    "severity": "MEDIUM"
                })
                health["checks"]["no_stuck_processes"] = False
            else:
                health["checks"]["no_stuck_processes"] = True
        else:
            health["checks"]["no_stuck_processes"] = True
        
        # 4. Check disk space
        result = self.run_command("df -h . | tail -1", "Disk space check", timeout=5)
        if result["success"]:
            # Parse disk usage
            parts = result["output"].split()
            if len(parts) >= 5:
                usage_percent = parts[4].replace('%', '')
                try:
                    if int(usage_percent) > 90:
                        print(f"   ⚠️ Disk almost full: {usage_percent}%")
                        self.problems_found.append({
                            "type": "disk_full",
                            "usage": usage_percent,
                            "severity": "HIGH"
                        })
                        health["checks"]["disk_space"] = False
                    else:
                        health["checks"]["disk_space"] = True
                except:
                    health["checks"]["disk_space"] = True
        
        # 5. Check recent video creation
        result = self.run_command(
            'find . -name "training_*.mp4" -mmin -60 -type f | wc -l',
            "Check recent videos",
            timeout=10
        )
        
        if result["success"]:
            recent_count = int(result["output"].strip()) if result["output"].strip().isdigit() else 0
            health["checks"]["videos_created_recently"] = recent_count > 0
            health["recent_videos_count"] = recent_count
            
            if recent_count == 0:
                print(f"   ⚠️ No videos created in last hour")
                self.problems_found.append({
                    "type": "no_recent_videos",
                    "severity": "MEDIUM"
                })
        
        # Overall health
        all_checks = list(health["checks"].values())
        health["overall_healthy"] = all(all_checks) if all_checks else False
        health["problems_count"] = len(self.problems_found)
        
        print(f"\n📊 Health Status: {'✅ HEALTHY' if health['overall_healthy'] else '⚠️ ISSUES FOUND'}")
        print(f"   Problems detected: {len(self.problems_found)}")
        
        self.log_action("health_check", health)
        return health
    
    def auto_fix_problems(self):
        """Auto fix detected problems"""
        if not self.problems_found:
            print("\n✅ No problems to fix!")
            return
        
        print("\n" + "="*70)
        print("🔧 AUTO-FIXING PROBLEMS")
        print("="*70)
        
        for problem in self.problems_found:
            print(f"\n🔍 Problem: {problem['type']} (Severity: {problem['severity']})")
            
            if problem['type'] == 'stuck_processes':
                # Kill stuck processes
                result = self.run_command(
                    "pkill -f 'python.*agent' || true",
                    "Kill stuck processes"
                )
                if result["success"]:
                    print("   ✅ Stuck processes killed")
                    self.fixes_applied.append({
                        "problem": problem['type'],
                        "fix": "killed_stuck_processes",
                        "success": True
                    })
            
            elif problem['type'] == 'no_recent_videos':
                # Create test video
                print("   🎬 Creating test video to verify system...")
                result = self.run_command(
                    "python3 simple_working_agent.py --videos 1 --delay 1",
                    "Test video creation",
                    timeout=120
                )
                if result["success"]:
                    print("   ✅ Test video created successfully")
                    self.fixes_applied.append({
                        "problem": problem['type'],
                        "fix": "created_test_video",
                        "success": True
                    })
                else:
                    print("   ❌ Test video creation failed")
                    self.fixes_applied.append({
                        "problem": problem['type'],
                        "fix": "created_test_video",
                        "success": False
                    })
            
            elif problem['type'] == 'disk_full':
                # Cleanup old videos
                print("   🧹 Cleaning up old training videos...")
                result = self.run_command(
                    'find . -name "training_*.mp4" -mtime +1 -type f -delete',
                    "Delete videos older than 1 day"
                )
                if result["success"]:
                    print("   ✅ Old videos cleaned up")
                    self.fixes_applied.append({
                        "problem": problem['type'],
                        "fix": "cleanup_old_videos",
                        "success": True
                    })
        
        print(f"\n✅ Applied {len(self.fixes_applied)} fixes")
        self.log_action("fixes_applied", {"fixes": self.fixes_applied})
    
    def create_videos_batch(self, count: int = 5, delay: int = 10):
        """Create a batch of videos"""
        print("\n" + "="*70)
        print(f"🎬 CREATING {count} VIDEOS")
        print("="*70)
        
        result = self.run_command(
            f"python3 simple_working_agent.py --videos {count} --delay {delay}",
            f"Create {count} training videos",
            timeout=count * 60  # 1 minute per video
        )
        
        if result["success"]:
            # Count created videos
            count_result = self.run_command(
                'find . -name "training_*.mp4" -mmin -10 -type f | wc -l',
                "Count newly created videos",
                timeout=10
            )
            
            if count_result["success"]:
                created = int(count_result["output"].strip()) if count_result["output"].strip().isdigit() else 0
                print(f"\n✅ Created {created} videos")
                
                self.videos_created.append({
                    "timestamp": datetime.now().isoformat(),
                    "count": created,
                    "requested": count
                })
                
                self.log_action("videos_created", {
                    "count": created,
                    "requested": count
                })
        else:
            print(f"\n❌ Video creation failed")
    
    def train_other_systems(self):
        """Train other systems with lessons learned"""
        print("\n" + "="*70)
        print("🎓 TRAINING OTHER SYSTEMS")
        print("="*70)
        
        # Create training report
        training_data = {
            "timestamp": datetime.now().isoformat(),
            "lessons": [],
            "commands_learned": [],
            "best_practices": []
        }
        
        # Lesson 1: System health checks
        training_data["lessons"].append({
            "topic": "System Health Monitoring",
            "importance": "CRITICAL",
            "what_learned": "Always check: Python version, critical files, stuck processes, disk space, recent output",
            "code_pattern": "ps aux | grep -E 'python.*agent' | grep -v grep"
        })
        
        # Lesson 2: Auto fixing
        training_data["lessons"].append({
            "topic": "Automatic Problem Resolution",
            "importance": "HIGH",
            "what_learned": "Kill stuck processes, create test outputs, cleanup old data",
            "code_pattern": "pkill -f 'pattern' || true"
        })
        
        # Lesson 3: Video creation
        training_data["lessons"].append({
            "topic": "Reliable Video Creation",
            "importance": "HIGH",
            "what_learned": "Use simple_working_agent.py with .mp4 extension, check output with find",
            "code_pattern": "python3 simple_working_agent.py --videos N --delay D"
        })
        
        # Best commands learned
        training_data["commands_learned"] = [
            cmd for cmd in self.command_history if cmd.get("success", False)
        ]
        
        # Best practices
        training_data["best_practices"] = [
            "Always check file existence before running",
            "Use timeouts for subprocess calls",
            "Log every action with timestamps",
            "Clean up old data automatically",
            "Test fixes immediately after applying",
            "Use || true to prevent command failures from stopping execution"
        ]
        
        # Save training data
        training_file = self.workspace / "rahbar_training_data.json"
        with open(training_file, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Training data saved: {training_file}")
        print(f"   Lessons: {len(training_data['lessons'])}")
        print(f"   Commands learned: {len(training_data['commands_learned'])}")
        print(f"   Best practices: {len(training_data['best_practices'])}")
        
        self.training_sessions.append(training_data)
        self.log_action("training_completed", {
            "lessons_count": len(training_data['lessons']),
            "commands_count": len(training_data['commands_learned'])
        })
    
    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "="*70)
        print("📊 RAHBAR SUPREME CONTROLLER REPORT")
        print("="*70)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "commands_executed": len(self.command_history),
                "problems_found": len(self.problems_found),
                "fixes_applied": len(self.fixes_applied),
                "videos_created": sum(v.get("count", 0) for v in self.videos_created),
                "training_sessions": len(self.training_sessions)
            },
            "details": {
                "command_history": self.command_history[-10:],  # Last 10 commands
                "problems_found": self.problems_found,
                "fixes_applied": self.fixes_applied,
                "videos_created": self.videos_created,
                "training_sessions": self.training_sessions
            }
        }
        
        print(f"\n📈 Summary:")
        print(f"   Commands executed: {report['summary']['commands_executed']}")
        print(f"   Problems found: {report['summary']['problems_found']}")
        print(f"   Fixes applied: {report['summary']['fixes_applied']}")
        print(f"   Videos created: {report['summary']['videos_created']}")
        print(f"   Training sessions: {report['summary']['training_sessions']}")
        
        # Save report
        report_file = self.workspace / f"rahbar_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Report saved: {report_file}")
        return report
    
    def run_full_cycle(self):
        """Run complete autonomous cycle"""
        print("\n" + "="*70)
        print("👑 RAHBAR SUPREME CONTROLLER - FULL AUTONOMOUS CYCLE")
        print("   ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ")
        print("="*70)
        
        # Step 1: Check system health
        health = self.check_system_health()
        
        # Step 2: Auto-fix problems
        if self.problems_found:
            self.auto_fix_problems()
            
            # Re-check health after fixes
            time.sleep(3)
            self.problems_found = []  # Clear old problems
            health = self.check_system_health()
        
        # Step 3: Create videos if system healthy
        if health.get("overall_healthy", False):
            self.create_videos_batch(count=5, delay=10)
        else:
            print("\n⚠️ System not fully healthy, skipping video creation")
        
        # Step 4: Train other systems
        self.train_other_systems()
        
        # Step 5: Generate report
        report = self.generate_report()
        
        print("\n" + "="*70)
        print("✅ FULL CYCLE COMPLETE!")
        print("="*70)
        
        return report


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("👑 RAHBAR AI SUPREME CONTROLLER")
    print("   Complete Autonomous System Management")
    print("   ਰਾਹਬਰ AI ਸੁਪਰੀਮ - ਸਭ ਕੁੱਝ ਆਪਣੇ ਆਪ")
    print("="*70)
    
    controller = RahbarSupremeController()
    controller.run_full_cycle()


if __name__ == "__main__":
    main()
