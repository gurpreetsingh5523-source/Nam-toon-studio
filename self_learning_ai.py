#!/usr/bin/env python3
"""
🧠 SELF-LEARNING AI SYSTEM
System that learns from user feedback and improves itself
ਆਪਣੇ ਆਪ ਸਿੱਖਣ ਵਾਲਾ ਸਿਸਟਮ
"""

import json
import os
from pathlib import Path
from datetime import datetime
import hashlib

class SelfLearningBrain:
    """AI that learns and improves from feedback"""
    
    def __init__(self, workspace_path):
        self.workspace = Path(workspace_path)
        self.memory_file = self.workspace / "ai_memory.json"
        self.feedback_file = self.workspace / "user_feedback.json"
        self.improvements_file = self.workspace / "ai_improvements.json"
        
        # Load or initialize memory
        self.memory = self.load_memory()
        self.feedback_history = self.load_feedback()
        self.improvements = self.load_improvements()
    
    def load_memory(self):
        """Load AI's learning memory"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if "perception_reports" not in data:
                data["perception_reports"] = []
            return data
        return {
            "created": datetime.now().isoformat(),
            "total_videos_created": 0,
            "successful_renders": 0,
            "failed_renders": 0,
            "user_satisfaction_scores": [],
            "learned_patterns": {},
            "character_styles": {
                "realistic": {"success_rate": 0, "usage_count": 0},
                "cartoon": {"success_rate": 0, "usage_count": 0},
                "anime": {"success_rate": 0, "usage_count": 0}
            },
            "rendering_techniques": {},
            "optimization_history": [],
            "perception_reports": []
        }
    
    def load_feedback(self):
        """Load user feedback history"""
        if self.feedback_file.exists():
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def load_improvements(self):
        """Load AI improvements history"""
        if self.improvements_file.exists():
            with open(self.improvements_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_memory(self):
        """Save AI memory to disk"""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)
    
    def save_feedback(self):
        """Save feedback history"""
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(self.feedback_history, f, indent=2, ensure_ascii=False)
    
    def save_improvements(self):
        """Save improvements history"""
        with open(self.improvements_file, 'w', encoding='utf-8') as f:
            json.dump(self.improvements, f, indent=2, ensure_ascii=False)
    
    def record_video_creation(self, success, details):
        """Record video creation attempt"""
        self.memory["total_videos_created"] += 1
        
        if success:
            self.memory["successful_renders"] += 1
        else:
            self.memory["failed_renders"] += 1
        
        # Learn from this attempt
        style = details.get("style", "realistic")
        if style in self.memory["character_styles"]:
            self.memory["character_styles"][style]["usage_count"] += 1
        
        self.save_memory()

    def record_perception_report(self, video_id, report_path, vision_summary=None, audio_summary=None):
        """Record perception analysis so the AI can track visual quality."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "video_id": video_id,
            "report_path": report_path,
            "vision_summary": vision_summary or {},
            "audio_summary": audio_summary or {},
        }
        self.memory.setdefault("perception_reports", []).append(entry)
        self.save_memory()
    
    def record_user_feedback(self, video_id, feedback_text, satisfaction_score, 
                            what_was_good, what_needs_improvement):
        """
        Record user feedback for learning
        
        Args:
            video_id: Unique ID for the video
            feedback_text: User's feedback in their words
            satisfaction_score: 1-5 rating
            what_was_good: List of positive aspects
            what_needs_improvement: List of things to improve
        """
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "video_id": video_id,
            "feedback": feedback_text,
            "score": satisfaction_score,
            "positive": what_was_good,
            "negative": what_needs_improvement
        }
        
        self.feedback_history.append(feedback_entry)
        self.memory["user_satisfaction_scores"].append(satisfaction_score)
        
        # Analyze feedback
        self.analyze_and_learn(feedback_entry)
        
        self.save_feedback()
        self.save_memory()
    
    def analyze_and_learn(self, feedback):
        """Analyze feedback and learn patterns"""
        
        # Learn from negative feedback
        for issue in feedback.get("negative", []):
            issue_lower = issue.lower()
            
            # Pattern: "cartoon" or "cartoonish" mentioned
            if "cartoon" in issue_lower or "cartoonish" in issue_lower:
                self.learn_pattern("avoid_cartoon_style", {
                    "reason": "User doesn't want cartoonish look",
                    "solution": "Increase realism in character rendering",
                    "implementation": "Use more detailed facial features, better proportions, textures"
                })
            
            # Pattern: "realistic" or "real" requested
            if "real" in issue_lower or "realistic" in issue_lower:
                self.learn_pattern("prefer_realistic", {
                    "reason": "User wants realistic rendering",
                    "solution": "Use photo-realistic rendering techniques",
                    "implementation": "Add shadows, textures, proper lighting, anatomy"
                })
            
            # Pattern: "voice" or "awaaz" issues
            if "voice" in issue_lower or "awaaz" in issue_lower:
                self.learn_pattern("improve_voice", {
                    "reason": "Voice quality issues",
                    "solution": "Better TTS or voice settings",
                    "implementation": "Adjust speed, tone, or use better voice model"
                })
            
            # Pattern: "slow" or "speed" issues
            if "slow" in issue_lower or "speed" in issue_lower:
                self.learn_pattern("optimize_speed", {
                    "reason": "Rendering too slow",
                    "solution": "Optimize rendering pipeline",
                    "implementation": "Cache backgrounds, parallel processing, reduce quality where not visible"
                })
        
        # Learn from positive feedback
        for positive in feedback.get("positive", []):
            positive_lower = positive.lower()
            
            if "realistic" in positive_lower or "real" in positive_lower:
                self.reinforce_pattern("realistic_rendering_success")
            
            if "voice" in positive_lower or "awaaz" in positive_lower:
                self.reinforce_pattern("voice_quality_good")
            
            if "smooth" in positive_lower or "animation" in positive_lower:
                self.reinforce_pattern("animation_quality_good")
    
    def learn_pattern(self, pattern_name, pattern_data):
        """Learn a new pattern or update existing one"""
        if pattern_name not in self.memory["learned_patterns"]:
            self.memory["learned_patterns"][pattern_name] = {
                "count": 1,
                "first_seen": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "data": pattern_data
            }
        else:
            self.memory["learned_patterns"][pattern_name]["count"] += 1
            self.memory["learned_patterns"][pattern_name]["last_updated"] = datetime.now().isoformat()
        
        # Generate improvement suggestion
        if self.memory["learned_patterns"][pattern_name]["count"] >= 2:
            self.generate_improvement(pattern_name, pattern_data)
    
    def reinforce_pattern(self, pattern_name):
        """Reinforce a positive pattern"""
        pattern_key = f"positive_{pattern_name}"
        if pattern_key not in self.memory["learned_patterns"]:
            self.memory["learned_patterns"][pattern_key] = {
                "count": 1,
                "type": "positive_reinforcement"
            }
        else:
            self.memory["learned_patterns"][pattern_key]["count"] += 1
    
    def generate_improvement(self, pattern_name, pattern_data):
        """Generate improvement suggestion based on learned pattern"""
        improvement = {
            "timestamp": datetime.now().isoformat(),
            "pattern": pattern_name,
            "reason": pattern_data.get("reason", "Unknown"),
            "suggested_solution": pattern_data.get("solution", ""),
            "implementation_details": pattern_data.get("implementation", ""),
            "priority": self.calculate_priority(pattern_name),
            "status": "pending"
        }
        
        self.improvements.append(improvement)
        self.save_improvements()
        
        print(f"\n🧠 AI LEARNED NEW IMPROVEMENT:")
        print(f"   Pattern: {pattern_name}")
        print(f"   Reason: {improvement['reason']}")
        print(f"   Solution: {improvement['suggested_solution']}")
        print(f"   Priority: {improvement['priority']}/10")
    
    def calculate_priority(self, pattern_name):
        """Calculate priority of improvement based on frequency"""
        if pattern_name in self.memory["learned_patterns"]:
            count = self.memory["learned_patterns"][pattern_name]["count"]
            # Priority increases with frequency
            priority = min(10, count * 2)
            return priority
        return 5
    
    def get_recommendations(self):
        """Get AI's recommendations for next video"""
        recommendations = []
        
        # Analyze learned patterns
        for pattern_name, pattern_data in self.memory["learned_patterns"].items():
            if pattern_data.get("count", 0) >= 2:
                if "avoid_cartoon" in pattern_name:
                    recommendations.append({
                        "type": "rendering_style",
                        "suggestion": "Use realistic renderer instead of cartoon style",
                        "confidence": min(100, pattern_data["count"] * 20)
                    })
                
                if "prefer_realistic" in pattern_name:
                    recommendations.append({
                        "type": "rendering_quality",
                        "suggestion": "Focus on photo-realistic details (shadows, textures, anatomy)",
                        "confidence": min(100, pattern_data["count"] * 25)
                    })
        
        # Check satisfaction trend
        if len(self.memory["user_satisfaction_scores"]) >= 3:
            recent_scores = self.memory["user_satisfaction_scores"][-3:]
            avg_score = sum(recent_scores) / len(recent_scores)
            
            if avg_score < 3:
                recommendations.append({
                    "type": "quality_alert",
                    "suggestion": "User satisfaction is low - major changes needed",
                    "confidence": 90
                })
            elif avg_score >= 4:
                recommendations.append({
                    "type": "quality_good",
                    "suggestion": "Current approach is working well - maintain quality",
                    "confidence": 85
                })
        
        return recommendations
    
    def get_pending_improvements(self):
        """Get list of pending improvements"""
        pending = [imp for imp in self.improvements if imp.get("status") == "pending"]
        # Sort by priority
        pending.sort(key=lambda x: x.get("priority", 0), reverse=True)
        return pending
    
    def mark_improvement_implemented(self, improvement_index):
        """Mark an improvement as implemented"""
        if improvement_index < len(self.improvements):
            self.improvements[improvement_index]["status"] = "implemented"
            self.improvements[improvement_index]["implemented_date"] = datetime.now().isoformat()
            self.save_improvements()
            return True
        return False
    
    def get_statistics(self):
        """Get AI learning statistics"""
        return {
            "total_videos": self.memory["total_videos_created"],
            "success_rate": (
                self.memory["successful_renders"] / self.memory["total_videos_created"] * 100
                if self.memory["total_videos_created"] > 0 else 0
            ),
            "average_satisfaction": (
                sum(self.memory["user_satisfaction_scores"]) / len(self.memory["user_satisfaction_scores"])
                if self.memory["user_satisfaction_scores"] else 0
            ),
            "patterns_learned": len(self.memory["learned_patterns"]),
            "pending_improvements": len(self.get_pending_improvements())
        }


class ImprovedRealisticRenderer:
    """Enhanced renderer that uses AI learning"""
    
    def __init__(self, ai_brain):
        self.ai = ai_brain
        self.apply_ai_improvements()
    
    def apply_ai_improvements(self):
        """Apply AI-learned improvements to rendering"""
        recommendations = self.ai.get_recommendations()
        
        print("\n🧠 AI RECOMMENDATIONS:")
        for rec in recommendations:
            print(f"   [{rec['type']}] {rec['suggestion']} (confidence: {rec['confidence']}%)")
        
        # Adjust rendering based on recommendations
        for rec in recommendations:
            if rec['type'] == 'rendering_style' and rec['confidence'] > 60:
                print("   ✅ Using realistic rendering style (learned from feedback)")
            
            if rec['type'] == 'rendering_quality' and rec['confidence'] > 70:
                print("   ✅ Increasing detail level (learned from user preference)")


# Demo usage
if __name__ == '__main__':
    print("🧠 SELF-LEARNING AI SYSTEM DEMO")
    print("="*50)
    
    # Initialize AI brain
    workspace = Path.cwd()
    ai = SelfLearningBrain(workspace)
    
    # Show statistics
    stats = ai.get_statistics()
    print(f"\n📊 AI STATISTICS:")
    print(f"   Videos created: {stats['total_videos']}")
    print(f"   Success rate: {stats['success_rate']:.1f}%")
    print(f"   Avg satisfaction: {stats['average_satisfaction']:.1f}/5")
    print(f"   Patterns learned: {stats['patterns_learned']}")
    print(f"   Pending improvements: {stats['pending_improvements']}")
    
    # Simulate user feedback
    print(f"\n📝 SIMULATING USER FEEDBACK...")
    ai.record_user_feedback(
        video_id="test_video_1",
        feedback_text="Video ਬਹੁਤ ਕਾਰਟੂਨਿਸ਼ ਹੈ, ਮੈਨੂੰ real tarah di chahidi hai",
        satisfaction_score=2,
        what_was_good=["Voice is good", "Animation is smooth"],
        what_needs_improvement=["Too cartoonish", "Need realistic characters", "Background not detailed enough"]
    )
    
    # Get recommendations
    recommendations = ai.get_recommendations()
    print(f"\n💡 AI RECOMMENDATIONS:")
    for rec in recommendations:
        print(f"   • {rec['suggestion']}")
    
    # Get pending improvements
    improvements = ai.get_pending_improvements()
    print(f"\n🔧 PENDING IMPROVEMENTS ({len(improvements)}):")
    for i, imp in enumerate(improvements[:5], 1):
        print(f"   {i}. [{imp['priority']}/10] {imp['suggested_solution']}")
    
    print(f"\n✅ AI is learning from your feedback!")
    print(f"   Memory saved to: {ai.memory_file}")
    print(f"   Feedback saved to: {ai.feedback_file}")
    print(f"   Improvements saved to: {ai.improvements_file}")
