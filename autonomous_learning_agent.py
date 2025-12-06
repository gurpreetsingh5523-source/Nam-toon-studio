#!/usr/bin/env python3
"""
🤖 AUTONOMOUS LEARNING AGENT
24x7 Video Creation + Learning + Self-Improvement
ਆਟੋਮੈਟਿਕ ਸਿੱਖਣ ਵਾਲਾ ਏਜੰਟ
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime
import random

# Add workspace to path
WORKSPACE = Path(__file__).parent.absolute()
sys.path.insert(0, str(WORKSPACE))

from integrated_smart_video_maker import IntegratedSmartVideoMaker


class AutonomousLearningAgent:
    """
    Agent that continuously creates videos and learns
    ਏਜੰਟ ਜੋ ਵੀਡੀਓ ਬਣਾਉਂਦਾ ਰਹਿੰਦਾ ਹੈ ਤੇ ਸਿੱਖਦਾ ਰਹਿੰਦਾ ਹੈ
    """
    
    def __init__(self, workspace=None):
        """Initialize agent"""
        self.workspace = Path(workspace or WORKSPACE)
        self.video_maker = IntegratedSmartVideoMaker(self.workspace)
        self.training_log = self.workspace / "agent_training_log.json"
        self.training_data = self._load_training_log()
        
        # Training scenarios
        self.training_scenarios = [
            {
                "id": "punjabi_village",
                "text": "[SCENE 1: Village]\nਇੱਕ ਪਿੰਡ ਵਿੱਚ ਇੱਕ ਬੁੱਢਾ ਕਿਸਾਨ ਰਹਿੰਦਾ ਸੀ।\nThere was an old farmer in the village.",
                "expected_quality": ["realistic", "punjabi_culture"]
            },
            {
                "id": "morning_walk",
                "text": "[SCENE 1: Walking]\nਸਵੇਰੇ ਦੀ ਸੈਰ ਬਹੁਤ ਸਿਹਤਮੰਦ ਹੈ।\nMorning walk is very healthy.",
                "expected_quality": ["smooth_animation", "natural_movement"]
            },
            {
                "id": "guru_teaching",
                "text": "[SCENE 1: Teaching]\nਗੁਰੂ ਜੀ ਨੇ ਕਿਹਾ, ਸਿਖੋ ਤੇ ਸਿਖਾਓ।\nGuru ji said, learn and teach.",
                "expected_quality": ["spiritual", "wisdom"]
            },
            {
                "id": "family_gathering",
                "text": "[SCENE 1: Home]\nਪਰਿਵਾਰ ਇਕੱਠਾ ਹੋਇਆ, ਖੁਸ਼ੀਆਂ ਹੀ ਖੁਸ਼ੀਆਂ।\nFamily gathered, happiness everywhere.",
                "expected_quality": ["warmth", "togetherness"]
            },
            {
                "id": "tech_learning",
                "text": "[SCENE 1: Computer]\nਕੰਪਿਊਟਰ ਸਿੱਖਣਾ ਅੱਜ ਕੱਲ੍ਹ ਬਹੁਤ ਜ਼ਰੂਰੀ ਹੈ।\nLearning computer is very important nowadays.",
                "expected_quality": ["modern", "educational"]
            }
        ]
        
        print("✅ Autonomous Learning Agent initialized")
    
    def _load_training_log(self):
        """Load training log"""
        if self.training_log.exists():
            with open(self.training_log, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "sessions": [],
            "total_videos": 0,
            "total_training_time": 0,
            "best_video": None,
            "worst_video": None
        }
    
    def _save_training_log(self):
        """Save training log"""
        with open(self.training_log, 'w', encoding='utf-8') as f:
            json.dump(self.training_data, f, indent=2, ensure_ascii=False)
    
    def run_training_session(self, num_videos=5, delay_seconds=2):
        """
        Run training session - create multiple videos and learn
        
        Args:
            num_videos: Number of videos to create
            delay_seconds: Delay between videos
        """
        print("\n" + "="*70)
        print(f"🤖 AUTONOMOUS TRAINING SESSION STARTED")
        print(f"   Creating {num_videos} videos for learning")
        print("="*70)
        
        session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        session_start = time.time()
        
        session_data = {
            "session_id": session_id,
            "start_time": datetime.now().isoformat(),
            "videos_created": 0,
            "successful": 0,
            "failed": 0,
            "scenarios_used": []
        }
        
        for i in range(num_videos):
            print(f"\n{'='*70}")
            print(f"🎬 VIDEO {i+1}/{num_videos}")
            print(f"{'='*70}")
            
            # Select random scenario
            scenario = random.choice(self.training_scenarios)
            print(f"📝 Scenario: {scenario['id']}")
            
            output_path = self.workspace / f"training_video_{session_id}_{i+1}.mp4"
            
            try:
                # Create video
                success = self.video_maker.create_video(
                    text=scenario['text'],
                    output_path=str(output_path),
                    add_voice=True,
                    add_music=True,
                    ask_feedback=False  # Auto mode, no manual feedback
                )
                
                if success:
                    session_data['successful'] += 1
                    session_data['videos_created'] += 1
                    
                    # Auto-generate feedback for learning
                    self._auto_feedback(scenario['id'], i+1)
                    
                    print(f"✅ Video {i+1} completed")
                else:
                    session_data['failed'] += 1
                    print(f"❌ Video {i+1} failed")
                
                session_data['scenarios_used'].append(scenario['id'])
                
            except Exception as e:
                print(f"❌ Error creating video {i+1}: {e}")
                session_data['failed'] += 1
            
            # Delay before next video
            if i < num_videos - 1:
                print(f"\n⏳ Waiting {delay_seconds} seconds before next video...")
                time.sleep(delay_seconds)
        
        # Session complete
        session_end = time.time()
        session_duration = session_end - session_start
        
        session_data['end_time'] = datetime.now().isoformat()
        session_data['duration_seconds'] = session_duration
        
        # Save session data
        self.training_data['sessions'].append(session_data)
        self.training_data['total_videos'] += session_data['videos_created']
        self.training_data['total_training_time'] += session_duration
        self._save_training_log()
        
        # Show results
        print("\n" + "="*70)
        print("📊 TRAINING SESSION COMPLETE")
        print("="*70)
        print(f"✅ Videos created: {session_data['videos_created']}")
        print(f"✅ Successful: {session_data['successful']}")
        print(f"❌ Failed: {session_data['failed']}")
        print(f"⏱️  Duration: {session_duration:.1f} seconds")
        print(f"📈 Success rate: {(session_data['successful']/num_videos*100):.1f}%")
        
        # Show AI learning progress
        print("\n🧠 AI LEARNING AFTER THIS SESSION:")
        self.video_maker.show_learning_progress()
    
    def _auto_feedback(self, scenario_id, video_num):
        """Generate automatic feedback for learning"""
        # Simulate realistic feedback patterns
        feedback_patterns = {
            "punjabi_village": {
                "good": ["Village scene looks good", "Cultural elements present"],
                "improve": ["Need more realistic textures", "Characters could be more detailed"],
                "score": random.randint(3, 4)
            },
            "morning_walk": {
                "good": ["Animation is smooth", "Movement looks natural"],
                "improve": ["Background could be more detailed", "Lighting needs improvement"],
                "score": random.randint(3, 5)
            },
            "guru_teaching": {
                "good": ["Spiritual atmosphere captured", "Respectful representation"],
                "improve": ["Facial expressions need work", "More realistic guru appearance"],
                "score": random.randint(3, 4)
            },
            "family_gathering": {
                "good": ["Warm feeling conveyed", "Multiple characters visible"],
                "improve": ["Character interactions could be better", "More realistic faces"],
                "score": random.randint(3, 4)
            },
            "tech_learning": {
                "good": ["Modern elements visible", "Educational context clear"],
                "improve": ["Computer details need improvement", "More realistic rendering"],
                "score": random.randint(3, 4)
            }
        }
        
        pattern = feedback_patterns.get(scenario_id, {
            "good": ["Video created"],
            "improve": ["General improvements needed"],
            "score": 3
        })
        
        # Record feedback
        video_id = f"auto_{scenario_id}_{video_num}"
        self.video_maker.ai_brain.record_user_feedback(
            video_id=video_id,
            feedback_text=f"Auto-generated feedback for {scenario_id}",
            satisfaction_score=pattern['score'],
            what_was_good=pattern['good'],
            what_needs_improvement=pattern['improve']
        )
        
        print(f"🤖 Auto-feedback recorded: {pattern['score']}/5")
    
    def continuous_learning_mode(self, max_iterations=None):
        """
        Continuous learning - keeps creating and learning
        
        Args:
            max_iterations: Max iterations (None = infinite)
        """
        print("\n" + "="*70)
        print("🔄 CONTINUOUS LEARNING MODE ACTIVATED")
        print("   Press Ctrl+C to stop")
        print("="*70)
        
        iteration = 0
        
        try:
            while max_iterations is None or iteration < max_iterations:
                iteration += 1
                print(f"\n🔄 Iteration {iteration}")
                
                # Run training session
                self.run_training_session(num_videos=2, delay_seconds=3)
                
                # Show progress
                print(f"\n📈 Total videos created so far: {self.training_data['total_videos']}")
                
                # Wait before next iteration
                wait_time = 10
                print(f"\n⏳ Next iteration in {wait_time} seconds...")
                time.sleep(wait_time)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Continuous learning stopped by user")
            print(f"📊 Total iterations completed: {iteration}")
    
    def analyze_learning_progress(self):
        """Analyze learning progress over time"""
        print("\n" + "="*70)
        print("📊 LEARNING PROGRESS ANALYSIS")
        print("="*70)
        
        if not self.training_data['sessions']:
            print("❌ No training sessions found")
            return
        
        total_sessions = len(self.training_data['sessions'])
        total_videos = self.training_data['total_videos']
        total_time = self.training_data['total_training_time']
        
        print(f"\n📈 OVERALL STATISTICS:")
        print(f"   Training sessions: {total_sessions}")
        print(f"   Total videos: {total_videos}")
        print(f"   Total training time: {total_time/60:.1f} minutes")
        print(f"   Avg videos per session: {total_videos/total_sessions:.1f}")
        
        # Calculate success rate trend
        if total_sessions >= 2:
            first_session = self.training_data['sessions'][0]
            last_session = self.training_data['sessions'][-1]
            
            first_success_rate = (first_session['successful'] / 
                                 (first_session['successful'] + first_session['failed']) * 100)
            last_success_rate = (last_session['successful'] / 
                                (last_session['successful'] + last_session['failed']) * 100)
            
            improvement = last_success_rate - first_success_rate
            
            print(f"\n📈 IMPROVEMENT TREND:")
            print(f"   First session success: {first_success_rate:.1f}%")
            print(f"   Last session success: {last_success_rate:.1f}%")
            print(f"   Improvement: {improvement:+.1f}%")
        
        # Show AI brain stats
        print("\n🧠 AI BRAIN STATISTICS:")
        self.video_maker.show_learning_progress()


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Autonomous Learning Agent')
    parser.add_argument('--mode', choices=['session', 'continuous', 'analyze', 'limited'], 
                       default='session', help='Operation mode')
    parser.add_argument('--videos', type=int, default=3, 
                       help='Number of videos per session')
    parser.add_argument('--iterations', type=int, default=None, 
                       help='Max iterations for continuous mode')
    parser.add_argument('--max-videos', type=int, default=20,
                       help='Max videos to create in limited mode')
    parser.add_argument('--config', type=str, default=None,
                       help='Config file with custom patterns')
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = AutonomousLearningAgent()
    
    # Load custom config if provided
    if args.config:
        import json
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                custom_config = json.load(f)
                if 'patterns' in custom_config:
                    agent.training_scenarios = custom_config['patterns']
                    print(f"✅ Loaded {len(agent.training_scenarios)} custom patterns")
        except Exception as e:
            print(f"⚠️ Could not load config: {e}")
    
    if args.mode == 'session':
        # Single training session
        agent.run_training_session(num_videos=args.videos)
    
    elif args.mode == 'continuous':
        # Continuous learning
        agent.continuous_learning_mode(max_iterations=args.iterations)
    
    elif args.mode == 'limited':
        # Limited mode - create specific number of videos then stop
        print(f"🎯 Limited mode: Creating {args.max_videos} videos")
        for i in range(args.max_videos):
            agent.run_training_session(num_videos=1)
            if (i + 1) % 5 == 0:
                print(f"✅ Progress: {i + 1}/{args.max_videos} videos")
        print(f"✅ Limited mode complete: {args.max_videos} videos created")
    
    elif args.mode == 'analyze':
        # Analyze progress
        agent.analyze_learning_progress()


if __name__ == '__main__':
    main()
