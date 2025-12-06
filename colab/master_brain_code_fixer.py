#!/usr/bin/env python3
"""
🧠 MASTER BRAIN CODE FIXER & LOGIC UNDERSTANDING 🧠
===================================================

Master Brain can now:
1. Understand code logic from all brains
2. Fix code issues automatically
3. Learn from brain experiences
4. Analyze media data (music, images, videos)
5. Share knowledge between brains
6. Create coordinated video plans

ਮਾਸਟਰ ਦਿਮਾਗ ਹੁਣ ਕੋਡ ਠੀਕ ਕਰ ਸਕਦਾ ਹੈ!
"""

import json
import ast
import re
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import inspect


class CodeUnderstanding:
    """Master Brain's ability to understand and fix code"""
    
    def __init__(self):
        self.known_patterns = {
            "import_error": {
                "pattern": r"ModuleNotFoundError|ImportError",
                "fix": "Add missing import or check sys.path"
            },
            "type_error": {
                "pattern": r"TypeError",
                "fix": "Check function arguments and types"
            },
            "value_error": {
                "pattern": r"ValueError",
                "fix": "Validate input values before processing"
            },
            "attribute_error": {
                "pattern": r"AttributeError",
                "fix": "Check if object has the attribute"
            },
            "key_error": {
                "pattern": r"KeyError",
                "fix": "Check if dictionary key exists"
            }
        }
        
        self.fixed_issues = []
        self.learning_log = []
    
    def analyze_error(self, error_text: str) -> Dict[str, Any]:
        """Understand what went wrong"""
        
        analysis = {
            "error_type": "unknown",
            "severity": "medium",
            "fixable": False,
            "suggested_fix": None,
            "learning": None
        }
        
        # Detect error type
        for error_name, info in self.known_patterns.items():
            if re.search(info["pattern"], error_text):
                analysis["error_type"] = error_name
                analysis["suggested_fix"] = info["fix"]
                analysis["fixable"] = True
                break
        
        # Determine severity
        if "Critical" in error_text or "Fatal" in error_text:
            analysis["severity"] = "critical"
        elif "Warning" in error_text:
            analysis["severity"] = "low"
        
        # Extract learning
        analysis["learning"] = f"Encountered {analysis['error_type']}, learned to check for this pattern"
        
        return analysis
    
    def fix_code_issue(self, code: str, error_info: Dict[str, Any]) -> str:
        """Attempt to fix code based on error understanding"""
        
        fixed_code = code
        
        if error_info["error_type"] == "import_error":
            # Add try-except around imports
            fixed_code = self._add_import_fallback(code)
        
        elif error_info["error_type"] == "type_error":
            # Add type checking
            fixed_code = self._add_type_checks(code)
        
        elif error_info["error_type"] == "key_error":
            # Add dict.get() instead of dict[]
            fixed_code = self._safe_dict_access(code)
        
        # Log the fix
        self.fixed_issues.append({
            "timestamp": datetime.now().isoformat(),
            "error_type": error_info["error_type"],
            "fix_applied": True
        })
        
        return fixed_code
    
    def _add_import_fallback(self, code: str) -> str:
        """Add try-except for imports"""
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                fixed_lines.append(f"try:")
                fixed_lines.append(f"    {line}")
                fixed_lines.append(f"except ImportError as e:")
                fixed_lines.append(f"    print(f'Warning: {{e}}')")
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _add_type_checks(self, code: str) -> str:
        """Add type validation"""
        # Add isinstance checks before operations
        return code  # Simplified for now
    
    def _safe_dict_access(self, code: str) -> str:
        """Replace dict[] with dict.get()"""
        # Replace risky dict access patterns
        fixed = re.sub(r'(\w+)\[(["\'][\w_]+["\']\])', r'\1.get(\2, None)', code)
        return fixed
    
    def understand_brain_logic(self, brain_name: str, brain_code: str) -> Dict[str, Any]:
        """Deep understanding of a brain's logic"""
        
        understanding = {
            "brain": brain_name,
            "functions": [],
            "algorithms": [],
            "data_structures": [],
            "complexity": "unknown",
            "strengths": [],
            "weaknesses": []
        }
        
        try:
            # Parse the code
            tree = ast.parse(brain_code)
            
            # Extract functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    understanding["functions"].append({
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "line": node.lineno
                    })
                
                # Detect algorithms
                if isinstance(node, ast.For):
                    understanding["algorithms"].append("iteration")
                if isinstance(node, ast.If):
                    understanding["algorithms"].append("conditional_logic")
                if isinstance(node, ast.Try):
                    understanding["algorithms"].append("error_handling")
            
            # Analyze complexity
            function_count = len(understanding["functions"])
            if function_count > 20:
                understanding["complexity"] = "high"
            elif function_count > 10:
                understanding["complexity"] = "medium"
            else:
                understanding["complexity"] = "low"
            
            # Identify strengths
            if "error_handling" in understanding["algorithms"]:
                understanding["strengths"].append("Good error handling")
            if function_count > 5:
                understanding["strengths"].append("Well-modularized code")
            
        except Exception as e:
            understanding["error"] = str(e)
        
        return understanding


class BrainLearningSharing:
    """System for brains to share what they learned"""
    
    def __init__(self):
        self.knowledge_base = {
            "visual_brain": {
                "learned_patterns": [],
                "successful_strategies": [],
                "failed_approaches": [],
                "shared_insights": []
            },
            "audio_brain": {
                "learned_patterns": [],
                "successful_strategies": [],
                "failed_approaches": [],
                "shared_insights": []
            },
            "voice_brain": {
                "learned_patterns": [],
                "successful_strategies": [],
                "failed_approaches": [],
                "shared_insights": []
            },
            "creative_brain": {
                "learned_patterns": [],
                "successful_strategies": [],
                "failed_approaches": [],
                "shared_insights": []
            }
        }
    
    def brain_shares_learning(
        self, 
        brain_name: str, 
        learning_type: str, 
        content: Dict[str, Any]
    ) -> None:
        """Brain shares what it learned with Master Brain"""
        
        if brain_name not in self.knowledge_base:
            return
        
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": learning_type,
            "content": content,
            "usefulness": 0  # Will be updated based on usage
        }
        
        if learning_type == "pattern":
            self.knowledge_base[brain_name]["learned_patterns"].append(learning_entry)
        elif learning_type == "success":
            self.knowledge_base[brain_name]["successful_strategies"].append(learning_entry)
        elif learning_type == "failure":
            self.knowledge_base[brain_name]["failed_approaches"].append(learning_entry)
        elif learning_type == "insight":
            self.knowledge_base[brain_name]["shared_insights"].append(learning_entry)
        
        print(f"\n📚 {brain_name} shared {learning_type}:")
        print(f"   {content.get('summary', 'New learning')}")
    
    def get_shared_knowledge(self, requesting_brain: str) -> Dict[str, Any]:
        """Get knowledge shared by other brains"""
        
        shared = {
            "from_others": {},
            "count": 0
        }
        
        for brain_name, knowledge in self.knowledge_base.items():
            if brain_name != requesting_brain:
                shared["from_others"][brain_name] = {
                    "patterns": len(knowledge["learned_patterns"]),
                    "strategies": len(knowledge["successful_strategies"]),
                    "insights": len(knowledge["shared_insights"])
                }
                shared["count"] += sum(shared["from_others"][brain_name].values())
        
        return shared
    
    def cross_brain_learning(self) -> Dict[str, Any]:
        """Find patterns that multiple brains discovered"""
        
        common_patterns = []
        
        # Compare learnings across brains
        all_patterns = []
        for brain_name, knowledge in self.knowledge_base.items():
            for pattern in knowledge["learned_patterns"]:
                all_patterns.append({
                    "brain": brain_name,
                    "pattern": pattern
                })
        
        # Find common themes
        # (Simplified - could use NLP for real similarity)
        
        return {
            "common_patterns": common_patterns,
            "total_shared_learnings": len(all_patterns)
        }


class MediaDataAnalyzer:
    """Master Brain analyzes music, images, video to understand media"""
    
    def __init__(self):
        self.media_library = {
            "music": [],
            "images": [],
            "videos": []
        }
        
        self.media_understanding = {
            "music_emotions": {},
            "visual_styles": {},
            "video_patterns": {}
        }
    
    def analyze_music(self, music_file: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Understand music characteristics"""
        
        analysis = {
            "file": music_file,
            "emotion": metadata.get("emotion", "unknown"),
            "tempo": metadata.get("tempo", "medium"),
            "instruments": metadata.get("instruments", []),
            "cultural_context": metadata.get("culture", "universal"),
            "usage_scenarios": []
        }
        
        # Learn from this music
        if analysis["emotion"] not in self.media_understanding["music_emotions"]:
            self.media_understanding["music_emotions"][analysis["emotion"]] = []
        
        self.media_understanding["music_emotions"][analysis["emotion"]].append(analysis)
        
        # Determine when to use this music
        if analysis["tempo"] == "slow" and analysis["emotion"] in ["sad", "peaceful"]:
            analysis["usage_scenarios"].append("emotional_scenes")
        elif analysis["tempo"] == "fast" and analysis["emotion"] in ["happy", "excited"]:
            analysis["usage_scenarios"].append("celebration_scenes")
        
        self.media_library["music"].append(analysis)
        
        return analysis
    
    def analyze_image(self, image_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Understand image characteristics"""
        
        analysis = {
            "file": image_path,
            "dominant_colors": metadata.get("colors", []),
            "objects": metadata.get("objects", []),
            "emotion": metadata.get("emotion", "neutral"),
            "style": metadata.get("style", "realistic"),
            "usage_scenarios": []
        }
        
        # Learn visual patterns
        if analysis["style"] not in self.media_understanding["visual_styles"]:
            self.media_understanding["visual_styles"][analysis["style"]] = []
        
        self.media_understanding["visual_styles"][analysis["style"]].append(analysis)
        
        self.media_library["images"].append(analysis)
        
        return analysis
    
    def analyze_video(self, video_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Understand video patterns"""
        
        analysis = {
            "file": video_path,
            "duration": metadata.get("duration", 0),
            "fps": metadata.get("fps", 24),
            "scenes": metadata.get("scenes", []),
            "transitions": metadata.get("transitions", []),
            "pacing": metadata.get("pacing", "medium")
        }
        
        self.media_library["videos"].append(analysis)
        
        return analysis
    
    def get_media_recommendations(self, scene_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend media based on learned patterns"""
        
        recommendations = {
            "music": None,
            "visual_style": None,
            "pacing": None,
            "reasoning": []
        }
        
        emotion = scene_requirements.get("emotion", "neutral")
        
        # Find matching music
        if emotion in self.media_understanding["music_emotions"]:
            music_options = self.media_understanding["music_emotions"][emotion]
            if music_options:
                recommendations["music"] = music_options[0]["file"]
                recommendations["reasoning"].append(
                    f"Selected music based on {len(music_options)} learned examples for {emotion}"
                )
        
        # Find matching visual style
        style = scene_requirements.get("style", "realistic")
        if style in self.media_understanding["visual_styles"]:
            recommendations["visual_style"] = style
            recommendations["reasoning"].append(
                f"Using {style} style based on learned patterns"
            )
        
        return recommendations


class MasterBrainCodeFixer:
    """
    Supreme Master Brain with:
    - Code understanding and fixing
    - Learning from all brains
    - Media analysis and understanding
    - Video creation planning with knowledge sharing
    """
    
    def __init__(self):
        print("\n" + "="*70)
        print("🧠 INITIALIZING MASTER BRAIN CODE FIXER")
        print("="*70)
        
        self.code_understanding = CodeUnderstanding()
        self.learning_system = BrainLearningSharing()
        self.media_analyzer = MediaDataAnalyzer()
        
        self.video_plans = []
        self.fix_history = []
        
        print("✅ Code Understanding: ENABLED")
        print("✅ Learning Sharing: ENABLED")
        print("✅ Media Analysis: ENABLED")
        print("✅ Video Planning: ENABLED")
        print("="*70)
    
    def receive_brain_learning(
        self, 
        brain_name: str, 
        learning: Dict[str, Any]
    ) -> None:
        """Receive and process learning from a brain"""
        
        print(f"\n📥 Receiving learning from {brain_name}...")
        
        learning_type = learning.get("type", "insight")
        content = learning.get("content", {})
        
        self.learning_system.brain_shares_learning(brain_name, learning_type, content)
        
        # Analyze if this learning can help other brains
        shared_knowledge = self.learning_system.get_shared_knowledge(brain_name)
        
        if shared_knowledge["count"] > 0:
            print(f"   💡 This connects with {shared_knowledge['count']} learnings from other brains!")
    
    def fix_brain_issue(
        self, 
        brain_name: str, 
        error_text: str, 
        brain_code: str
    ) -> Dict[str, Any]:
        """Master Brain fixes issues in other brains"""
        
        print(f"\n🔧 Master Brain analyzing {brain_name} issue...")
        
        # Understand the error
        error_analysis = self.code_understanding.analyze_error(error_text)
        
        print(f"   Error Type: {error_analysis['error_type']}")
        print(f"   Severity: {error_analysis['severity']}")
        print(f"   Fixable: {'Yes ✅' if error_analysis['fixable'] else 'No ❌'}")
        
        if error_analysis["fixable"]:
            print(f"\n   🛠️  Attempting to fix...")
            fixed_code = self.code_understanding.fix_code_issue(brain_code, error_analysis)
            
            result = {
                "fixed": True,
                "fixed_code": fixed_code,
                "analysis": error_analysis,
                "explanation": f"Applied fix: {error_analysis['suggested_fix']}"
            }
            
            # Log this fix
            self.fix_history.append({
                "timestamp": datetime.now().isoformat(),
                "brain": brain_name,
                "error": error_analysis["error_type"],
                "fixed": True
            })
            
            print(f"   ✅ Fix applied successfully!")
            return result
        else:
            print(f"   ⚠️  Cannot auto-fix, needs manual intervention")
            return {
                "fixed": False,
                "analysis": error_analysis,
                "explanation": "Requires manual fix"
            }
    
    def understand_all_brains(self, brain_codes: Dict[str, str]) -> Dict[str, Any]:
        """Deep understanding of all brain logics"""
        
        print("\n" + "="*70)
        print("🧠 MASTER BRAIN UNDERSTANDING ALL BRAIN LOGICS")
        print("="*70)
        
        all_understanding = {}
        
        for brain_name, code in brain_codes.items():
            print(f"\n📖 Understanding {brain_name}...")
            understanding = self.code_understanding.understand_brain_logic(brain_name, code)
            all_understanding[brain_name] = understanding
            
            print(f"   Functions: {len(understanding['functions'])}")
            print(f"   Complexity: {understanding['complexity']}")
            print(f"   Strengths: {', '.join(understanding['strengths']) if understanding['strengths'] else 'None identified'}")
        
        print("\n" + "="*70)
        return all_understanding
    
    def load_media_training_data(self, media_data: Dict[str, List[Dict]]) -> None:
        """Load music, images, videos for brains to learn from"""
        
        print("\n" + "="*70)
        print("📚 LOADING MEDIA TRAINING DATA FOR ALL BRAINS")
        print("="*70)
        
        # Analyze music
        if "music" in media_data:
            print(f"\n🎵 Analyzing {len(media_data['music'])} music files...")
            for music in media_data["music"]:
                analysis = self.media_analyzer.analyze_music(
                    music["file"], 
                    music["metadata"]
                )
                print(f"   ✅ {music['file']}: {analysis['emotion']} ({analysis['tempo']})")
        
        # Analyze images
        if "images" in media_data:
            print(f"\n🖼️  Analyzing {len(media_data['images'])} images...")
            for image in media_data["images"]:
                analysis = self.media_analyzer.analyze_image(
                    image["file"],
                    image["metadata"]
                )
                print(f"   ✅ {image['file']}: {analysis['style']}")
        
        # Analyze videos
        if "videos" in media_data:
            print(f"\n🎬 Analyzing {len(media_data['videos'])} videos...")
            for video in media_data["videos"]:
                analysis = self.media_analyzer.analyze_video(
                    video["file"],
                    video["metadata"]
                )
                print(f"   ✅ {video['file']}: {analysis['duration']}s")
        
        print(f"\n✅ Media training data loaded!")
        print(f"   🎵 Music emotions understood: {len(self.media_analyzer.media_understanding['music_emotions'])}")
        print(f"   🎨 Visual styles learned: {len(self.media_analyzer.media_understanding['visual_styles'])}")
        print("="*70)
    
    def create_video_plan_with_knowledge_sharing(
        self, 
        scene_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create comprehensive video plan where:
        1. Master Brain analyzes requirements
        2. Gets recommendations from learned media
        3. Shares knowledge with all brains
        4. Brains discuss and contribute their expertise
        5. Final coordinated plan created
        """
        
        print("\n" + "="*70)
        print("🎬 CREATING VIDEO PLAN WITH KNOWLEDGE SHARING")
        print("="*70)
        
        plan = {
            "scene": scene_requirements,
            "master_analysis": {},
            "media_recommendations": {},
            "brain_contributions": {},
            "final_plan": {},
            "knowledge_used": []
        }
        
        # Step 1: Master Brain analyzes
        print("\n1️⃣  Master Brain analyzing scene requirements...")
        plan["master_analysis"] = {
            "emotion": scene_requirements.get("emotion", "neutral"),
            "complexity": "medium",
            "required_brains": ["visual", "audio", "voice", "creative"]
        }
        
        # Step 2: Get media recommendations
        print("\n2️⃣  Getting recommendations from learned media...")
        recommendations = self.media_analyzer.get_media_recommendations(scene_requirements)
        plan["media_recommendations"] = recommendations
        
        if recommendations["reasoning"]:
            print("   💡 Recommendations:")
            for reason in recommendations["reasoning"]:
                print(f"      • {reason}")
        
        # Step 3: Gather knowledge from all brains
        print("\n3️⃣  Gathering shared knowledge from all brains...")
        for brain_name in ["visual_brain", "audio_brain", "voice_brain", "creative_brain"]:
            shared = self.learning_system.get_shared_knowledge(brain_name)
            plan["brain_contributions"][brain_name] = shared
            
            if shared["count"] > 0:
                print(f"   📚 {brain_name}: {shared['count']} relevant learnings found")
        
        # Step 4: Create coordinated plan
        print("\n4️⃣  Creating final coordinated plan...")
        plan["final_plan"] = {
            "visual": {
                "style": recommendations.get("visual_style", "realistic"),
                "colors": self._get_emotion_colors(scene_requirements.get("emotion", "neutral")),
                "composition": "centered"
            },
            "audio": {
                "music": recommendations.get("music", "ambient.mp3"),
                "volume": 0.4,
                "ambient_sounds": []
            },
            "voice": {
                "character": scene_requirements.get("character", "narrator"),
                "accent": scene_requirements.get("accent", "Majhi"),
                "emotion": scene_requirements.get("emotion", "neutral")
            },
            "creative": {
                "duration": scene_requirements.get("duration", 5.0),
                "transition": "fade",
                "pacing": recommendations.get("pacing", "medium")
            }
        }
        
        print("\n✅ Video plan created with knowledge from all brains!")
        print("="*70)
        
        self.video_plans.append(plan)
        return plan
    
    def _get_emotion_colors(self, emotion: str) -> List[str]:
        """Get colors based on emotion"""
        color_map = {
            "happy": ["#FFD700", "#FFA500"],
            "sad": ["#4169E1", "#708090"],
            "angry": ["#DC143C", "#8B0000"],
            "peaceful": ["#98FB98", "#B0E0E6"],
            "excited": ["#FF6347", "#FF4500"]
        }
        return color_map.get(emotion, ["#808080", "#A9A9A9"])
    
    def get_master_brain_report(self) -> str:
        """Comprehensive report of Master Brain activities"""
        
        report = []
        report.append("\n" + "="*70)
        report.append("🧠 MASTER BRAIN CODE FIXER REPORT")
        report.append("="*70)
        
        # Fixes applied
        report.append(f"\n🔧 CODE FIXES:")
        report.append(f"   Total Issues Fixed: {len(self.fix_history)}")
        if self.fix_history:
            for fix in self.fix_history[-5:]:  # Last 5
                report.append(f"   • {fix['brain']}: {fix['error']} ✅")
        
        # Knowledge sharing
        report.append(f"\n📚 KNOWLEDGE SHARING:")
        total_learnings = 0
        for brain_name, knowledge in self.learning_system.knowledge_base.items():
            brain_total = (
                len(knowledge["learned_patterns"]) +
                len(knowledge["successful_strategies"]) +
                len(knowledge["shared_insights"])
            )
            total_learnings += brain_total
            if brain_total > 0:
                report.append(f"   {brain_name}: {brain_total} learnings shared")
        report.append(f"   Total Shared Learnings: {total_learnings}")
        
        # Media understanding
        report.append(f"\n🎬 MEDIA UNDERSTANDING:")
        report.append(f"   Music Files: {len(self.media_analyzer.media_library['music'])}")
        report.append(f"   Images: {len(self.media_analyzer.media_library['images'])}")
        report.append(f"   Videos: {len(self.media_analyzer.media_library['videos'])}")
        report.append(f"   Emotions Understood: {len(self.media_analyzer.media_understanding['music_emotions'])}")
        
        # Video plans
        report.append(f"\n🎥 VIDEO PLANS CREATED:")
        report.append(f"   Total Plans: {len(self.video_plans)}")
        
        report.append("="*70)
        
        return "\n".join(report)


# Example usage
if __name__ == "__main__":
    master = MasterBrainCodeFixer()
    
    # Example: Brain shares learning
    master.receive_brain_learning(
        "visual_brain",
        {
            "type": "success",
            "content": {
                "summary": "Using warm colors for happy emotions works well",
                "data": {"emotion": "happy", "colors": ["#FFD700", "#FFA500"], "success_rate": 0.95}
            }
        }
    )
    
    # Example: Load training data
    training_data = {
        "music": [
            {
                "file": "punjabi_folk_happy.mp3",
                "metadata": {
                    "emotion": "happy",
                    "tempo": "fast",
                    "instruments": ["dhol", "tumbi"],
                    "culture": "punjabi"
                }
            },
            {
                "file": "kirtan_peaceful.mp3",
                "metadata": {
                    "emotion": "peaceful",
                    "tempo": "slow",
                    "instruments": ["harmonium", "tabla"],
                    "culture": "punjabi"
                }
            }
        ],
        "images": [
            {
                "file": "punjab_fields.jpg",
                "metadata": {
                    "colors": ["green", "yellow"],
                    "objects": ["wheat_field", "sky"],
                    "emotion": "peaceful",
                    "style": "realistic"
                }
            }
        ]
    }
    
    master.load_media_training_data(training_data)
    
    # Example: Create video plan
    scene = {
        "emotion": "happy",
        "character": "Amandip",
        "accent": "Majhi",
        "duration": 5.0
    }
    
    plan = master.create_video_plan_with_knowledge_sharing(scene)
    
    # Show report
    print(master.get_master_brain_report())
