#!/usr/bin/env python3
"""
🧠 RAHBAR AI AUTO-LEARNER & FIXER
ਰਾਹਬਰ AI ਜੋ ਸਿੱਖ ਕੇ ਆਪ ਠੀਕ ਕਰੇ

This makes Rahbar AI:
1. Read learning feed
2. Understand problems
3. Generate fixes
4. Apply fixes
5. Test solutions
"""

import json
import sys
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(__file__).parent
sys.path.insert(0, str(WORKSPACE))

from RAHBAR_AI_DEVELOPER import RahbarAIDeveloper, CodeGenerator

class RahbarAutoLearner:
    """Rahbar AI that learns and fixes automatically"""
    
    def __init__(self):
        self.workspace = WORKSPACE
        self.learning_feed = self._load_learning_feed()
        self.rahbar = RahbarAIDeveloper(self.workspace)
        self.intelligence_plan = self._load_intelligence_plan()
        print("🧠 Rahbar Auto-Learner initialized")
    
    def _load_learning_feed(self):
        """Load learning data"""
        feed_file = self.workspace / "rahbar_learning_feed.json"
        if not feed_file.exists():
            print("❌ Learning feed not found!")
            return None
        
        with open(feed_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📚 Loaded {len(data['lessons_learned'])} lessons")
        return data

    def _load_intelligence_plan(self):
        """Load Rahbar intelligence plan if available."""
        plan_path = self.workspace / "rahbar_intelligence_plan.json"
        if not plan_path.exists():
            return None
        try:
            with open(plan_path, 'r', encoding='utf-8') as handle:
                plan = json.load(handle)
            print("🧠 Intelligence plan detected for auto tasks")
            return plan
        except Exception as exc:
            print(f"⚠️ Could not load intelligence plan: {exc}")
            return None

    def apply_intelligence_plan(self):
        """Transform intelligence plan into actionable auto tasks."""
        if not self.intelligence_plan:
            print("⚠️ No intelligence plan found to apply")
            return None
        tasks = []
        for tool in self.intelligence_plan.get('recommended_tools', []):
            tasks.append({
                "type": "tool",
                "name": tool.get('name'),
                "suggested_file": tool.get('suggested_file'),
                "priority": tool.get('priority'),
                "description": tool.get('description'),
                "description_pa": tool.get('description_pa')
            })
        for upgrade in self.intelligence_plan.get('automation_upgrades', []):
            tasks.append({
                "type": "automation",
                "name": upgrade.get('name'),
                "priority": upgrade.get('priority'),
                "description": upgrade.get('description'),
                "description_pa": upgrade.get('description_pa')
            })
        for objective in self.intelligence_plan.get('learning_objectives', []):
            tasks.append({
                "type": "learning",
                "name": objective.get('title'),
                "priority": "HIGH",
                "description": objective.get('objective'),
                "description_pa": objective.get('objective_pa')
            })
        output_path = self.workspace / "rahbar_auto_tasks.json"
        payload = {
            "generated_at": datetime.now().isoformat(),
            "tasks": tasks
        }
        with open(output_path, 'w', encoding='utf-8') as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
        print(f"🧾 Intelligence tasks saved: {output_path}")
        return payload
    
    def study_lessons(self):
        """Study all lessons learned"""
        print("\n" + "="*70)
        print("📖 RAHBAR AI STUDYING LESSONS...")
        print("="*70)
        
        for lesson in self.learning_feed['lessons_learned']:
            print(f"\n📌 Lesson {lesson['lesson_id']}: {lesson['title']}")
            print(f"   Problem: {lesson['problem']}")
            print(f"   Importance: {lesson['importance']}")
            key_learning = lesson.get('lesson') or lesson.get('lesson_summary', 'N/A')
            print(f"   Key Learning: {key_learning}")
        
        print(f"\n✅ Studied {len(self.learning_feed['lessons_learned'])} lessons")
    
    def analyze_priorities(self):
        """Analyze what needs to be fixed first"""
        print("\n" + "="*70)
        print("🎯 ANALYZING PRIORITIES...")
        print("="*70)
        
        improvements = self.learning_feed['future_improvements']
        
        # Sort by priority
        priority_order = {'CRITICAL': 1, 'URGENT': 2, 'HIGH': 3, 'MEDIUM': 4, 'LOW': 5}
        sorted_tasks = sorted(improvements, 
                            key=lambda x: priority_order.get(x['priority'], 10))
        
        print("\n📋 Priority Order:")
        for i, task in enumerate(sorted_tasks, 1):
            print(f"\n{i}. [{task['priority']}] {task['task']}")
            print(f"   Complexity: {task['complexity']}")
            print(f"   Time: {task['estimated_time']}")
            print(f"   Approach: {task['approach']}")
        
        return sorted_tasks
    
    def generate_fix_for_agent_config(self):
        """Generate fix for autonomous_learning_agent.py config loading"""
        print("\n" + "="*70)
        print("🔧 GENERATING FIX: Agent Config Loading")
        print("="*70)
        
        # Get the lesson
        lesson = [l for l in self.learning_feed['lessons_learned'] 
                 if l['lesson_id'] == 1][0]
        
        print(f"\n📝 Problem: {lesson['problem']}")
        print(f"🎯 Solution: {lesson['solution']}")
        
        fix_code = '''
# FIX TO ADD IN autonomous_learning_agent.py main() function:

# After args = parser.parse_args()
# After agent = AutonomousLearningAgent()

# Add this block:
if args.config:
    import json
    from pathlib import Path
    try:
        config_path = Path(args.config)
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                custom_config = json.load(f)
                
            # Load custom patterns if provided
            if 'patterns' in custom_config:
                print(f"✅ Loading {len(custom_config['patterns'])} custom patterns from config")
                agent.training_scenarios = custom_config['patterns']
                
            # Load other config options
            if 'max_videos' in custom_config:
                # Use config max_videos if not overridden by CLI
                if not hasattr(args, 'max_videos') or args.max_videos == 20:
                    args.max_videos = custom_config['max_videos']
                    
            print(f"✅ Config loaded from {args.config}")
        else:
            print(f"⚠️ Config file not found: {args.config}")
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        import traceback
        traceback.print_exc()
'''
        
        print("\n💾 Fix Code Generated:")
        print(fix_code)
        
        # Save fix
        fix_file = self.workspace / "FIX_agent_config_loading.txt"
        with open(fix_file, 'w') as f:
            f.write(fix_code)
        
        print(f"\n✅ Fix saved to: {fix_file}")
        return fix_code
    
    def create_simple_working_agent(self):
        """Create a simple agent that actually works"""
        print("\n" + "="*70)
        print("🔧 CREATING SIMPLE WORKING AGENT")
        print("="*70)
        
        lesson = [l for l in self.learning_feed['lessons_learned'] 
                 if l['lesson_id'] == 4][0]
        
        print(f"📖 Following lesson: {lesson['title']}")
        print(f"🎯 Approach: {lesson['lesson']}")
        
        # Check if simple_working_agent.py already exists
        agent_file = self.workspace / "simple_working_agent.py"
        if agent_file.exists():
            print(f"✅ Simple working agent already exists: {agent_file}")
            print(f"   Size: {agent_file.stat().st_size} bytes")
            return True
        else:
            print(f"⚠️ Simple working agent not found")
            print(f"   Expected at: {agent_file}")
            return False
    
    def test_simple_agent(self):
        """Test if simple agent can create videos"""
        print("\n" + "="*70)
        print("🧪 TESTING SIMPLE AGENT")
        print("="*70)
        
        agent_file = self.workspace / "simple_working_agent.py"
        if not agent_file.exists():
            print("❌ Simple agent not found, cannot test")
            return False
        
        print("📝 Test Plan:")
        print("   1. Import simple_working_agent")
        print("   2. Create agent instance")
        print("   3. Create 1 test video")
        print("   4. Verify video exists")
        
        try:
            print("\n🔍 Importing agent...")
            from simple_working_agent import SimpleWorkingAgent
            
            print("✅ Import successful")
            print("\n🔧 Creating agent instance...")
            agent = SimpleWorkingAgent()
            
            print("✅ Agent created")
            print(f"   Scenarios available: {len(agent.scenarios)}")
            
            print("\n🎬 Creating test video...")
            success = agent.create_one_video(0)
            
            if success:
                print("✅ TEST PASSED: Video created successfully!")
                return True
            else:
                print("❌ TEST FAILED: Video creation failed")
                return False
                
        except Exception as e:
            print(f"❌ TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_action_plan(self):
        """Generate complete action plan"""
        print("\n" + "="*70)
        print("📋 RAHBAR AI ACTION PLAN")
        print("="*70)
        
        plan = {
            "generated_at": datetime.now().isoformat(),
            "generated_by": "Rahbar AI Auto-Learner",
            "based_on": "Learning feed from debugging session",
            
            "immediate_actions": [
                {
                    "action": "Test simple_working_agent.py",
                    "reason": "Verify we have a working baseline",
                    "command": "python3 simple_working_agent.py --videos 2 --delay 2",
                    "expected": "2 videos created successfully",
                    "priority": "CRITICAL"
                },
                {
                    "action": "Fix autonomous_learning_agent.py config loading",
                    "reason": "Original agent can't load custom patterns",
                    "file": "autonomous_learning_agent.py",
                    "changes": "Add config loading block in main()",
                    "priority": "URGENT"
                },
                {
                    "action": "Add process health monitoring",
                    "reason": "Detect stuck agents early",
                    "file": "MASTER_TRAINING_ORCHESTRATOR.py",
                    "changes": "Check CPU% and process state",
                    "priority": "HIGH"
                }
            ],
            
            "testing_strategy": [
                "1. Test simple agent with 1 video",
                "2. If works, test with 5 videos",
                "3. Fix any issues found",
                "4. Only then deploy orchestrator",
                "5. Start with 1 agent, not 4",
                "6. Scale up gradually"
            ],
            
            "success_criteria": [
                "✅ Simple agent creates videos reliably",
                "✅ Config loading works",
                "✅ Process monitoring active",
                "✅ No stuck processes",
                "✅ Videos actually created",
                "✅ Diverse patterns used"
            ]
        }
        
        # Save plan
        plan_file = self.workspace / "rahbar_action_plan.json"
        with open(plan_file, 'w') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Action plan saved: {plan_file}")
        
        print("\n📋 IMMEDIATE ACTIONS:")
        for i, action in enumerate(plan['immediate_actions'], 1):
            print(f"\n{i}. [{action['priority']}] {action['action']}")
            print(f"   Reason: {action['reason']}")
            if 'command' in action:
                print(f"   Command: {action['command']}")
        
        return plan
    
    def run_full_learning_cycle(self):
        """Run complete learning and fixing cycle"""
        print("\n" + "="*70)
        print("🚀 RAHBAR AI FULL LEARNING CYCLE STARTING")
        print("   ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ")
        print("="*70)
        
        # Step 1: Study lessons
        self.study_lessons()
        
        # Step 2: Analyze priorities
        tasks = self.analyze_priorities()
        
        # Step 3: Generate fixes
        self.generate_fix_for_agent_config()
        
        # Step 4: Check simple agent
        simple_agent_exists = self.create_simple_working_agent()
        
        # Step 5: Test if possible
        if simple_agent_exists:
            test_result = self.test_simple_agent()
        
        # Step 6: Generate action plan
        plan = self.generate_action_plan()
        auto_tasks = self.apply_intelligence_plan()
        
        print("\n" + "="*70)
        print("✅ RAHBAR AI LEARNING CYCLE COMPLETE")
        print("="*70)
        print("\n📚 Summary:")
        print(f"   Lessons studied: {len(self.learning_feed['lessons_learned'])}")
        print(f"   Fixes generated: 1 (agent config)")
        print(f"   Action items: {len(plan['immediate_actions'])}")
        print(f"   Simple agent: {'✅ Ready' if simple_agent_exists else '⚠️ Not found'}")
        if auto_tasks:
            print(f"   Intelligence tasks: {len(auto_tasks['tasks'])}")
        
        print("\n🎯 NEXT STEPS FOR HUMAN:")
        print("   1. Review: rahbar_action_plan.json")
        print("   2. Apply fix: FIX_agent_config_loading.txt")
        print("   3. Test: python3 simple_working_agent.py --videos 2")
        print("   4. Deploy: Only after testing works!")
        
        return {
            "lessons_studied": len(self.learning_feed['lessons_learned']),
            "fixes_generated": 1,
            "plan_created": True,
            "simple_agent_ready": simple_agent_exists
        }


def main():
    """Main entry point"""
    learner = RahbarAutoLearner()
    result = learner.run_full_learning_cycle()
    
    print("\n✅ Rahbar AI learning complete!")
    print(f"   Results: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    main()
