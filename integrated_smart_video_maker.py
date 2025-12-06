#!/usr/bin/env python3
"""
🧠🎬 INTEGRATED SMART VIDEO MAKER
Combines: Video Maker + Self-Learning AI + Brain Chain
ਵੀਡੀਓ ਮੇਕਰ + ਸਿੱਖਣ ਵਾਲਾ AI = ਸਮਾਰਟ ਸਿਸਟਮ
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add workspace to path
WORKSPACE = Path(__file__).parent.absolute()
sys.path.insert(0, str(WORKSPACE))

# Import existing systems
from realistic_movie_maker import RealisticMovieMaker
from self_learning_ai import SelfLearningBrain
from realistic_renderer import RealisticRenderer

try:
    from amrit_perception_brain import AmritPerceptionBrain
    PERCEPTION_AVAILABLE = True
    PERCEPTION_IMPORT_ERROR = None
except Exception as e:  # pragma: no cover - optional dependency
    PERCEPTION_AVAILABLE = False
    PERCEPTION_IMPORT_ERROR = str(e)

try:
    from amrit_brain_chain import AmritBrainChain
    BRAIN_CHAIN_AVAILABLE = True
except:
    BRAIN_CHAIN_AVAILABLE = False
    print("⚠️ Brain chain not available (optional)")


class IntegratedSmartVideoMaker:
    """
    Smart video maker that learns and improves
    ਸਮਾਰਟ ਵੀਡੀਓ ਬਣਾਉਣ ਵਾਲਾ ਜੋ ਸਿੱਖਦਾ ਹੈ
    """
    
    def __init__(self, workspace=None):
        """Initialize integrated system"""
        self.workspace = Path(workspace or WORKSPACE)
        
        # Core systems
        print("🔧 Initializing systems...")
        self.video_maker = RealisticMovieMaker()
        self.ai_brain = SelfLearningBrain(self.workspace)

        self.perception_brain = None
        if PERCEPTION_AVAILABLE:
            try:
                self.perception_brain = AmritPerceptionBrain(workspace=self.workspace)
                print("✅ Perception brain connected")
            except Exception as e:
                self.perception_brain = None
                print(f"⚠️ Perception brain not initialized: {e}")
        elif PERCEPTION_IMPORT_ERROR:
            print(f"⚠️ Perception brain unavailable: {PERCEPTION_IMPORT_ERROR}")
        
        # Optional: Brain chain for intelligent responses
        if BRAIN_CHAIN_AVAILABLE:
            try:
                self.brain_chain = AmritBrainChain(str(self.workspace))
                print("✅ Brain chain connected")
            except Exception as e:
                self.brain_chain = None
                print(f"⚠️ Brain chain not initialized: {e}")
        else:
            self.brain_chain = None
        
        print("✅ Integrated Smart Video Maker ready!")
        self._show_ai_stats()
    
    def _show_ai_stats(self):
        """Show AI learning statistics"""
        stats = self.ai_brain.get_statistics()
        print("\n📊 AI LEARNING STATUS:")
        print(f"   Videos created: {stats['total_videos']}")
        print(f"   Success rate: {stats['success_rate']:.1f}%")
        print(f"   Patterns learned: {stats['patterns_learned']}")
        print(f"   Pending improvements: {stats['pending_improvements']}")
        
        # Show recommendations if available
        recommendations = self.ai_brain.get_recommendations()
        if recommendations:
            print(f"\n💡 AI RECOMMENDATIONS ({len(recommendations)}):")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"   {i}. {rec['suggestion']} (confidence: {rec['confidence']}%)")
    
    def create_video(self, text, output_path="smart_video.mp4", 
                    add_voice=True, add_music=True, ask_feedback=True,
                    run_perception=True, perception_options=None):
        """
        Create video with AI learning
        
        Args:
            text: Story text
            output_path: Output video path
            add_voice: Add Punjabi voice narration
            add_music: Add background music
            ask_feedback: Ask for user feedback after creation
            run_perception: Run perception analysis on finished video
            perception_options: Optional tuning dict for perception brain
        """
        print("\n" + "="*70)
        print("🧠🎬 SMART VIDEO CREATION STARTED")
        print("="*70)
        
        video_id = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        perception_options = perception_options or {}
        perception_report = None
        
        # Check AI recommendations before starting
        recommendations = self.ai_brain.get_recommendations()
        if recommendations:
            print("\n💡 AI SUGGESTIONS:")
            for rec in recommendations[:2]:
                print(f"   • {rec['suggestion']}")
        
        # Create video using existing maker
        try:
            print("\n🎬 Creating video...")
            result = self.video_maker.create_movie(
                text=text,
                output_path=output_path,
                add_voice=add_voice,
                add_music=add_music
            )

            planner_summary = getattr(self.video_maker, "last_scene_plan", None)
            if planner_summary and planner_summary.get("scenes"):
                print("\n🧭 Planner summary:")
                max_preview = 3
                for scene in planner_summary["scenes"][:max_preview]:
                    title = scene.get("title") or f"Scene {scene.get('scene_id')}"
                    location_tag = (scene.get("location") or {}).get("tag") or "unknown"
                    mood_tag = (scene.get("mood") or {}).get("tag") or "unspecified"
                    print(f"   • {title} → location: {location_tag}, mood: {mood_tag}")
                extra = len(planner_summary["scenes"]) - max_preview
                if extra > 0:
                    print(f"   • ...and {extra} more scene(s)")
            
            # Record success
            self.ai_brain.record_video_creation(
                success=True,
                details={
                    "video_id": video_id,
                    "style": "realistic",
                    "voice": add_voice,
                    "music": add_music,
                    "timestamp": datetime.now().isoformat()
                }
            )

            if run_perception:
                if self.perception_brain:
                    print("\n🔍 Running perception analysis on the finished video...")
                    try:
                        perception_report = self.perception_brain.analyze_video(
                            output_path,
                            frame_stride=perception_options.get("frame_stride", 10),
                            max_frames=perception_options.get("max_frames", 200),
                            audio_window=perception_options.get("audio_window", 1.0),
                            audio_sample_rate=perception_options.get("audio_sample_rate"),
                            save_report=perception_options.get("save_report", True),
                        )
                        if perception_report:
                            self.ai_brain.record_perception_report(
                                video_id=video_id,
                                report_path=perception_report.get("report_path"),
                                vision_summary=perception_report.get("vision"),
                                audio_summary=perception_report.get("audio"),
                            )
                    except Exception as e:
                        print(f"⚠️ Perception analysis failed: {e}")
                else:
                    print("⚠️ Perception brain unavailable, skipping analysis.")
            
            print(f"\n✅ Video created successfully: {output_path}")
            if perception_report and perception_report.get("report_path"):
                print(f"🧠 Perception report: {perception_report['report_path']}")
            
            # Ask for feedback to help AI learn
            if ask_feedback:
                self._collect_feedback(video_id)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Video creation failed: {e}")
            
            # Record failure
            self.ai_brain.record_video_creation(
                success=False,
                details={
                    "video_id": video_id,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            return False
    
    def _collect_feedback(self, video_id):
        """Collect user feedback for AI learning"""
        print("\n" + "="*70)
        print("📝 FEEDBACK TIME - Help AI Learn!")
        print("="*70)
        print("\nVideo dekhi? Kiven lagi? (Video watched? How was it?)")
        print("\nPress Enter to skip feedback, or provide your thoughts:")
        print("Example: 'Video thik hai, par character hor realistic chahide'")
        
        try:
            feedback_text = input("\n➤ Your feedback (Punjabi/English): ").strip()
            
            if not feedback_text:
                print("⏭️  Feedback skipped")
                return
            
            # Ask for rating
            print("\nRating deo (Give rating): 1-5")
            print("1 = Very bad, 2 = Bad, 3 = OK, 4 = Good, 5 = Excellent")
            
            try:
                rating = int(input("➤ Rating (1-5): ").strip())
                rating = max(1, min(5, rating))  # Clamp to 1-5
            except:
                rating = 3  # Default to OK
            
            # Quick analysis
            good_things = []
            needs_improvement = []
            
            feedback_lower = feedback_text.lower()
            
            # Positive signals
            if any(word in feedback_lower for word in ['good', 'changa', 'wadia', 'nice', 'excellent', 'perfect']):
                good_things.append("Overall positive feedback")
            
            if any(word in feedback_lower for word in ['voice', 'awaaz', 'sound']):
                if any(word in feedback_lower for word in ['good', 'changa', 'wadia']):
                    good_things.append("Voice quality appreciated")
                else:
                    needs_improvement.append("Voice needs improvement")
            
            # Negative signals
            if any(word in feedback_lower for word in ['cartoon', 'fake', 'unrealistic']):
                needs_improvement.append("Too cartoonish, need more realism")
            
            if any(word in feedback_lower for word in ['slow', 'lag', 'speed']):
                needs_improvement.append("Performance/speed issues")
            
            if any(word in feedback_lower for word in ['realistic', 'real', 'asli']):
                needs_improvement.append("Need more realistic rendering")
            
            # Record feedback
            self.ai_brain.record_user_feedback(
                video_id=video_id,
                feedback_text=feedback_text,
                satisfaction_score=rating,
                what_was_good=good_things if good_things else ["User provided feedback"],
                what_needs_improvement=needs_improvement if needs_improvement else ["General improvements needed"]
            )
            
            print("\n✅ Thank you! AI is learning from your feedback.")
            print("🧠 AI will use this to improve future videos!")
            
        except KeyboardInterrupt:
            print("\n⏭️  Feedback cancelled")
        except Exception as e:
            print(f"\n⚠️ Could not record feedback: {e}")
    
    def ask_brain_chain(self, question):
        """Ask the brain chain a question (if available)"""
        if not self.brain_chain:
            return "❌ Brain chain not available"
        
        try:
            response = self.brain_chain.process_input(question)
            return response
        except Exception as e:
            return f"❌ Brain chain error: {e}"
    
    def show_learning_progress(self):
        """Show detailed learning progress"""
        print("\n" + "="*70)
        print("🧠 AI LEARNING PROGRESS REPORT")
        print("="*70)
        
        stats = self.ai_brain.get_statistics()
        
        print(f"\n📊 STATISTICS:")
        print(f"   Total videos: {stats['total_videos']}")
        print(f"   Success rate: {stats['success_rate']:.1f}%")
        print(f"   Average satisfaction: {stats['average_satisfaction']:.1f}/5")
        print(f"   Patterns learned: {stats['patterns_learned']}")
        
        # Show learned patterns
        if self.ai_brain.memory["learned_patterns"]:
            print(f"\n🔍 LEARNED PATTERNS:")
            for pattern_name, pattern_data in list(self.ai_brain.memory["learned_patterns"].items())[:5]:
                count = pattern_data.get("count", 1)
                print(f"   • {pattern_name}: {count}x times")
        
        # Show pending improvements
        improvements = self.ai_brain.get_pending_improvements()
        if improvements:
            print(f"\n🔧 PENDING IMPROVEMENTS ({len(improvements)}):")
            for i, imp in enumerate(improvements[:3], 1):
                print(f"   {i}. {imp['suggested_solution']}")
                print(f"      Priority: {imp['priority']}/10")
        
        # Show recommendations
        recommendations = self.ai_brain.get_recommendations()
        if recommendations:
            print(f"\n💡 AI RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"   {i}. {rec['suggestion']}")
                print(f"      Confidence: {rec['confidence']}%")
        
        print("\n" + "="*70)
    
    def interactive_mode(self):
        """Interactive mode for testing"""
        print("\n" + "="*70)
        print("🎮 INTERACTIVE MODE")
        print("="*70)
        print("\nCommands:")
        print("  1. create - Create a video")
        print("  2. stats - Show learning progress")
        print("  3. ask - Ask brain chain a question")
        print("  4. quit - Exit")
        
        while True:
            try:
                cmd = input("\n➤ Command: ").strip().lower()
                
                if cmd in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                elif cmd in ['create', '1']:
                    text = input("➤ Story text (Punjabi/English): ").strip()
                    if text:
                        self.create_video(text, output_path="interactive_video.mp4")
                    else:
                        print("❌ Text required")
                
                elif cmd in ['stats', '2']:
                    self.show_learning_progress()
                
                elif cmd in ['ask', '3']:
                    question = input("➤ Your question: ").strip()
                    if question:
                        response = self.ask_brain_chain(question)
                        print(f"\n🧠 Brain Chain: {response}")
                    else:
                        print("❌ Question required")
                
                else:
                    print(f"❌ Unknown command: {cmd}")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Main function with demo"""
    print("\n" + "="*70)
    print("🧠🎬 INTEGRATED SMART VIDEO MAKER")
    print("   Video Maker + AI Learning + Brain Chain")
    print("="*70)
    
    # Initialize
    maker = IntegratedSmartVideoMaker()
    
    # Check command line args
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == '--interactive':
            maker.interactive_mode()
            return
        elif sys.argv[1] == '--stats':
            maker.show_learning_progress()
            return
    
    # Demo video
    print("\n📝 Creating demo video...")
    demo_text = """
    [SCENE 1: Village]
    ਇੱਕ ਵਾਰ ਦੀ ਗੱਲ ਹੈ, ਪਿੰਡ ਵਿੱਚ ਇੱਕ ਨੌਜਵਾਨ ਰਹਿੰਦਾ ਸੀ।
    Once upon a time, there was a young man in the village.
    
    [SCENE 2: Walking]
    ਉਹ ਹਰ ਰੋਜ਼ ਸਵੇਰੇ ਟਹਿਲਣ ਜਾਂਦਾ ਸੀ।
    He used to go for a walk every morning.
    """
    
    success = maker.create_video(
        text=demo_text,
        output_path="smart_demo_video.mp4",
        add_voice=True,
        add_music=True,
        ask_feedback=True
    )
    
    if success:
        print("\n✅ Demo complete!")
        print("\n💡 TIP: Run with --interactive for interactive mode")
        print("💡 TIP: Run with --stats to see learning progress")


if __name__ == '__main__':
    main()
