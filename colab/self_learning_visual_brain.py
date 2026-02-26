"""
🧠 SELF-LEARNING VISUAL AI BRAIN
=================================

Advanced AI system that learns and improves over time:

1. COLOR INTELLIGENCE
   - Learns color psychology (emotions → colors)
   - Analyzes successful color combinations
   - Adapts based on scene mood and cultural context

2. BEHAVIOR UNDERSTANDING
   - Recognizes character actions from text
   - Learns body language patterns
   - Predicts appropriate gestures and poses

3. EMOTION DETECTION
   - Analyzes dialogue for emotional content
   - Maps emotions to visual expressions
   - Learns subtle emotional transitions

4. CONTINUOUS LEARNING
   - Tracks what works well (user feedback)
   - Learns from mistakes (error correction)
   - Improves over time (experience database)

5. CULTURAL AWARENESS
   - Learns Sikh/Punjabi cultural elements
   - Understands traditional clothing, colors
   - Respects religious and cultural symbolism

Author: Amrit Core Team
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import re

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    import numpy as np
except ImportError:
    os.system("pip install Pillow numpy")
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    import numpy as np


class ColorIntelligence:
    """
    Learns and understands color psychology and combinations.
    """
    
    def __init__(self, brain_dir: str = "brain_memory"):
        self.brain_dir = Path(brain_dir)
        self.brain_dir.mkdir(exist_ok=True)
        
        # Initialize color knowledge base
        self.emotion_colors = {
            "happy": {
                "primary": ["#FFD700", "#FFA500", "#FFFF00"],  # Gold, Orange, Yellow
                "secondary": ["#FF69B4", "#FFB6C1", "#FFC0CB"],  # Pink tones
                "meaning": "Joy, celebration, warmth",
                "success_rate": 0.0,
                "usage_count": 0
            },
            "sad": {
                "primary": ["#4169E1", "#1E90FF", "#87CEEB"],  # Blue tones
                "secondary": ["#708090", "#778899", "#B0C4DE"],  # Gray-blue
                "meaning": "Sorrow, melancholy, tears",
                "success_rate": 0.0,
                "usage_count": 0
            },
            "angry": {
                "primary": ["#DC143C", "#FF0000", "#8B0000"],  # Red tones
                "secondary": ["#FF4500", "#FF6347", "#CD5C5C"],  # Orange-red
                "meaning": "Rage, intensity, heat",
                "success_rate": 0.0,
                "usage_count": 0
            },
            "peaceful": {
                "primary": ["#90EE90", "#98FB98", "#00FA9A"],  # Green tones
                "secondary": ["#87CEEB", "#ADD8E6", "#B0E0E6"],  # Light blue
                "meaning": "Calm, nature, serenity",
                "success_rate": 0.0,
                "usage_count": 0
            },
            "romantic": {
                "primary": ["#FF1493", "#FF69B4", "#FFC0CB"],  # Pink/Rose
                "secondary": ["#DDA0DD", "#EE82EE", "#DA70D6"],  # Purple tones
                "meaning": "Love, # TODO: Implement functionion, tenderness",
                "success_rate": 0.0,
                "usage_count": 0
            },
            "fearful": {
                "primary": ["#2F4F4F", "#696969", "#000000"],  # Dark tones
                "secondary": ["#483D8B", "#6A5ACD", "#8B008B"],  # Dark purple
                "meaning": "Darkness, uncertainty, danger",
                "success_rate": 0.0,
                "usage_count": 0
            },
            "celebratory": {
                "primary": ["#FF8C00", "#FFA500", "#FFD700"],  # Orange/Gold
                "secondary": ["#FF6347", "#FF4500", "#DC143C"],  # Red-orange
                "meaning": "Sikh celebrations, festivals (Vaisakhi colors)",
                "success_rate": 0.0,
                "usage_count": 0
            },
            "spiritual": {
                "primary": ["#FF8C00", "#0000FF", "#FFFFFF"],  # Sikh flag colors
                "secondary": ["#FFD700", "#FFA500", "#F0E68C"],  # Gold (sacred)
                "meaning": "Religious, divine, purity",
                "success_rate": 0.0,
                "usage_count": 0
            }
        }
        
        # Cultural color meanings (Punjabi/Sikh context)
        self.cultural_colors = {
            "saffron_orange": {
                "hex": "#FF8C00",
                "meaning": "Courage, sacrifice (Sikh tradition)",
                "contexts": ["prayer", "celebration", "bravery"]
            },
            "blue": {
                "hex": "#0000FF",
                "meaning": "Warrior spirit, strength (Khalsa)",
                "contexts": ["courage", "protection", "honor"]
            },
            "white": {
                "hex": "#FFFFFF",
                "meaning": "Purity, peace, truth",
                "contexts": ["elderly", "spiritual", "mourning"]
            },
            "red": {
                "hex": "#FF0000",
                "meaning": "Marriage, celebration, energy",
                "contexts": ["wedding", "festival", "joy"]
            },
            "green": {
                "hex": "#228B22",
                "meaning": "Agriculture, prosperity, life",
                "contexts": ["farming", "fields", "growth"]
            },
            "pink": {
                "hex": "#FF69B4",
                "meaning": "Femininity, youth, love",
                "contexts": ["young_women", "romance", "softness"]
            }
        }
        
        self.load_learning_data()
    
    def load_learning_data(self):
        """Load previously learned color patterns."""
        memory_file = self.brain_dir / "color_intelligence.json"
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                # Merge with defaults
                for emotion, data in saved_data.get("emotion_colors", {}).items():
                    if emotion in self.emotion_colors:
                        self.emotion_colors[emotion].update(data)
            print("✅ Loaded color intelligence memory")
    
    def save_learning_data(self):
        """Save learned color patterns."""
        memory_file = self.brain_dir / "color_intelligence.json"
        data = {
            "emotion_colors": self.emotion_colors,
            "cultural_colors": self.cultural_colors,
            "last_updated": datetime.now().isoformat()
        }
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_colors_for_emotion(
        self,
        emotion: str,
        cultural_context: Optional[str] = None
    ) -> Dict[str, List[str]]:
        """
        Get appropriate colors based on emotion and cultural context.
        Learns which combinations work best over time.
        """
        emotion_clean = emotion.lower().strip()
        
        # Get base colors
        color_scheme = self.emotion_colors.get(
            emotion_clean,
            self.emotion_colors["peaceful"]  # Default fallback
        )
        
        # Apply cultural context
        if cultural_context:
            if "prayer" in cultural_context.lower() or "spiritual" in cultural_context.lower():
                # Use spiritual colors
                color_scheme = self.emotion_colors["spiritual"]
            elif "wedding" in cultural_context.lower() or "celebration" in cultural_context.lower():
                color_scheme = self.emotion_colors["celebratory"]
        
        # Track usage
        color_scheme["usage_count"] += 1
        self.save_learning_data()
        
        return {
            "primary": color_scheme["primary"],
            "secondary": color_scheme["secondary"],
            "meaning": color_scheme["meaning"]
        }
    
    def learn_from_feedback(self, emotion: str, success: bool):
        """
        Learn from user feedback or results.
        Updates success rates for color choices.
        """
        emotion_clean = emotion.lower().strip()
        if emotion_clean in self.emotion_colors:
            scheme = self.emotion_colors[emotion_clean]
            current_rate = scheme["success_rate"]
            count = scheme["usage_count"]
            
            # Update success rate using moving average
            if count > 0:
                new_rate = (current_rate * (count - 1) + (1.0 if success else 0.0)) / count
                scheme["success_rate"] = new_rate
            
            self.save_learning_data()
            print(f"🧠 Learned: {emotion} colors → success rate: {scheme['success_rate']:.2%}")
    
    def analyze_color_harmony(self, color1: str, color2: str) -> float:
        """
        Analyze if two colors work well together.
        Returns harmony score (0.0 to 1.0).
        """
        # Convert hex to RGB
        rgb1 = tuple(int(color1.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        rgb2 = tuple(int(color2.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        # Calculate color distance
        distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))
        
        # Normalize (max distance is ~441 for RGB)
        normalized = distance / 441.0
        
        # Good harmony is neither too similar nor too different
        # Ideal range: 0.3 to 0.7
        if 0.3 <= normalized <= 0.7:
            harmony = 1.0 - abs(normalized - 0.5) * 2
        else:
            harmony = 0.5
        
        return harmony


class BehaviorUnderstanding:
    """
    Understands character behaviors and actions from text.
    """
    
    def __init__(self, brain_dir: str = "brain_memory"):
        self.brain_dir = Path(brain_dir)
        self.brain_dir.mkdir(exist_ok=True)
        
        # Behavior patterns (Punjabi + English)
        self.behavior_patterns = {
            "walking": {
                "keywords": ["ਚੱਲ", "ਗਿਆ", "ਆਇਆ", "walk", "went", "came", "going"],
                "animation": "walking_forward",
                "intensity": "medium",
                "confidence": 0.0,
                "examples": []
            },
            "running": {
                "keywords": ["ਭੱਜ", "ਦੌੜ", "run", "rush", "hurry"],
                "animation": "running_fast",
                "intensity": "high",
                "confidence": 0.0,
                "examples": []
            },
            "crying": {
                "keywords": ["ਰੋ", "ਅੱਥਰੂ", "cry", "tears", "weep", "sob"],
                "animation": "crying_gesture",
                "intensity": "high",
                "confidence": 0.0,
                "examples": []
            },
            "laughing": {
                "keywords": ["ਹੱਸ", "laugh", "smile", "grin", "chuckle"],
                "animation": "laughing_happy",
                "intensity": "medium",
                "confidence": 0.0,
                "examples": []
            },
            "praying": {
                "keywords": ["ਪ੍ਰਾਰਥਨਾ", "ਅਰਦਾਸ", "pray", "prayer", "worship", "ਅਰਦਾਸ"],
                "animation": "prayer_hands",
                "intensity": "calm",
                "confidence": 0.0,
                "examples": []
            },
            "farming": {
                "keywords": ["ਖੇਤ", "ਫਸਲ", "farm", "field", "harvest", "plow"],
                "animation": "working_field",
                "intensity": "medium",
                "confidence": 0.0,
                "examples": []
            },
            "gesturing": {
                "keywords": ["ਇਸ਼ਾਰਾ", "gesture", "point", "wave", "signal"],
                "animation": "hand_gesture",
                "intensity": "low",
                "confidence": 0.0,
                "examples": []
            },
            "sitting": {
                "keywords": ["ਬੈਠ", "sit", "sat", "seated"],
                "animation": "sitting_still",
                "intensity": "low",
                "confidence": 0.0,
                "examples": []
            },
            "embracing": {
                "keywords": ["ਗਲੇ", "embrace", "hug", "hold"],
                "animation": "hugging",
                "intensity": "medium",
                "confidence": 0.0,
                "examples": []
            },
            "fighting": {
                "keywords": ["ਲੜ", "fight", "struggle", "battle"],
                "animation": "aggressive_stance",
                "intensity": "high",
                "confidence": 0.0,
                "examples": []
            }
        }
        
        self.load_learning_data()
    
    def load_learning_data(self):
        """Load learned behavior patterns."""
        memory_file = self.brain_dir / "behavior_understanding.json"
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                for behavior, data in saved_data.get("patterns", {}).items():
                    if behavior in self.behavior_patterns:
                        self.behavior_patterns[behavior].update(data)
            print("✅ Loaded behavior understanding memory")
    
    def save_learning_data(self):
        """Save learned patterns."""
        memory_file = self.brain_dir / "behavior_understanding.json"
        data = {
            "patterns": self.behavior_patterns,
            "last_updated": datetime.now().isoformat()
        }
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def detect_behavior(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect behaviors from dialogue text.
        Returns list of detected behaviors with confidence scores.
        """
        text_lower = text.lower()
        detected = []
        
        for behavior, pattern in self.behavior_patterns.items():
            # Check if any keyword matches
            matches = [kw for kw in pattern["keywords"] if kw.lower() in text_lower]
            
            if matches:
                confidence = min(len(matches) * 0.3 + pattern["confidence"], 1.0)
                
                detected.append({
                    "behavior": behavior,
                    "animation": pattern["animation"],
                    "intensity": pattern["intensity"],
                    "confidence": confidence,
                    "matched_keywords": matches
                })
                
                # Learn from detection
                pattern["confidence"] = min(pattern["confidence"] + 0.01, 1.0)
                if text not in pattern["examples"]:
                    pattern["examples"].append(text[:100])  # Store snippet
        
        # Sort by confidence
        detected.sort(key=lambda x: x["confidence"], reverse=True)
        
        if detected:
            self.save_learning_data()
        
        return detected
    
    def learn_new_behavior(
        self,
        behavior_name: str,
        keywords: List[str],
        animation_type: str,
        intensity: str = "medium"
    ):
        """
        Learn a new behavior pattern.
        """
        self.behavior_patterns[behavior_name] = {
            "keywords": keywords,
            "animation": animation_type,
            "intensity": intensity,
            "confidence": 0.5,  # Start with medium confidence
            "examples": []
        }
        self.save_learning_data()
        print(f"🧠 Learned new behavior: {behavior_name}")


class EmotionDetection:
    """
    Detects and understands emotions from dialogue.
    """
    
    def __init__(self, brain_dir: str = "brain_memory"):
        self.brain_dir = Path(brain_dir)
        self.brain_dir.mkdir(exist_ok=True)
        
        # Emotion indicators (Punjabi + English)
        self.emotion_indicators = {
            "happy": {
                "keywords": ["ਖੁਸ਼", "ਖੁਸ਼ੀ", "happy", "joy", "glad", "delighted", "pleased"],
                "intensity_modifiers": ["very", "so", "extremely", "ਬਹੁਤ"],
                "accuracy": 0.0,
                "detection_count": 0
            },
            "sad": {
                "keywords": ["ਦੁਖੀ", "ਉਦਾਸ", "sad", "sorrow", "grief", "unhappy"],
                "intensity_modifiers": ["very", "deeply", "extremely", "ਬਹੁਤ"],
                "accuracy": 0.0,
                "detection_count": 0
            },
            "angry": {
                "keywords": ["ਗੁੱਸਾ", "ਕ੍ਰੋਧ", "angry", "rage", "furious", "mad"],
                "intensity_modifiers": ["very", "extremely", "ਬਹੁਤ"],
                "accuracy": 0.0,
                "detection_count": 0
            },
            "fearful": {
                "keywords": ["ਡਰ", "ਭਿਆ", "fear", "scared", "afraid", "terrified"],
                "intensity_modifiers": ["very", "so", "ਬਹੁਤ"],
                "accuracy": 0.0,
                "detection_count": 0
            },
            "surprised": {
                "keywords": ["ਹੈਰਾਨ", "surprise", "shocked", "amazed", "astonished"],
                "intensity_modifiers": ["very", "so", "ਬਹੁਤ"],
                "accuracy": 0.0,
                "detection_count": 0
            },
            "loving": {
                "keywords": ["ਪਿਆਰ", "ਪ੍ਰੇਮ", "love", "affection", "care", "dear"],
                "intensity_modifiers": ["deep", "true", "ਗਹਿਰਾ"],
                "accuracy": 0.0,
                "detection_count": 0
            },
            "peaceful": {
                "keywords": ["ਸ਼ਾਂਤ", "ਸੁਖ", "peace", "calm", "serene", "tranquil"],
                "intensity_modifiers": ["very", "completely", "ਬਹੁਤ"],
                "accuracy": 0.0,
                "detection_count": 0
            }
        }
        
        self.load_learning_data()
    
    def load_learning_data(self):
        """Load learned emotion patterns."""
        memory_file = self.brain_dir / "emotion_detection.json"
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                for emotion, data in saved_data.get("indicators", {}).items():
                    if emotion in self.emotion_indicators:
                        self.emotion_indicators[emotion].update(data)
            print("✅ Loaded emotion detection memory")
    
    def save_learning_data(self):
        """Save learned patterns."""
        memory_file = self.brain_dir / "emotion_detection.json"
        data = {
            "indicators": self.emotion_indicators,
            "last_updated": datetime.now().isoformat()
        }
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def detect_emotion(
        self,
        text: str,
        context_emotion: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Detect emotion from text with confidence score.
        """
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, indicators in self.emotion_indicators.items():
            score = 0.0
            matched_keywords = []
            
            # Check keywords
            for keyword in indicators["keywords"]:
                if keyword.lower() in text_lower:
                    score += 1.0
                    matched_keywords.append(keyword)
            
            # Check intensity modifiers
            for modifier in indicators["intensity_modifiers"]:
                if modifier.lower() in text_lower:
                    score += 0.3
            
            # Apply learned accuracy
            score *= (1.0 + indicators["accuracy"])
            
            if score > 0:
                emotion_scores[emotion] = {
                    "score": score,
                    "matched_keywords": matched_keywords
                }
        
        # Use context emotion if no clear detection
        if not emotion_scores and context_emotion:
            return {
                "emotion": context_emotion,
                "confidence": 0.3,
                "source": "context",
                "matched_keywords": []
            }
        
        # Get highest scoring emotion
        if emotion_scores:
            best_emotion = max(emotion_scores.items(), key=lambda x: x[1]["score"])
            emotion_name = best_emotion[0]
            data = best_emotion[1]
            
            # Update detection count
            self.emotion_indicators[emotion_name]["detection_count"] += 1
            self.save_learning_data()
            
            return {
                "emotion": emotion_name,
                "confidence": min(data["score"] / 2.0, 1.0),
                "source": "text",
                "matched_keywords": data["matched_keywords"]
            }
        
        # Default neutral
        return {
            "emotion": "neutral",
            "confidence": 0.5,
            "source": "default",
            "matched_keywords": []
        }
    
    def learn_from_correction(
        self,
        text: str,
        detected_emotion: str,
        correct_emotion: str
    ):
        """
        Learn from mistakes - update when detection was wrong.
        """
        if detected_emotion == correct_emotion:
            # Increase accuracy for correct detection
            self.emotion_indicators[detected_emotion]["accuracy"] += 0.05
        else:
            # Decrease accuracy for wrong detection
            if detected_emotion in self.emotion_indicators:
                self.emotion_indicators[detected_emotion]["accuracy"] -= 0.02
            
            # Increase accuracy for correct emotion
            if correct_emotion in self.emotion_indicators:
                self.emotion_indicators[correct_emotion]["accuracy"] += 0.05
        
        self.save_learning_data()
        print(f"🧠 Learned from correction: {detected_emotion} → {correct_emotion}")


class MistakeLearningSystem:
    """
    Tracks mistakes and learns from them to improve over time.
    """
    
    def __init__(self, brain_dir: str = "brain_memory"):
        self.brain_dir = Path(brain_dir)
        self.brain_dir.mkdir(exist_ok=True)
        
        self.mistake_log = []
        self.corrections = {}
        self.improvement_metrics = {
            "total_mistakes": 0,
            "corrected": 0,
            "improvement_rate": 0.0
        }
        
        self.load_learning_data()
    
    def load_learning_data(self):
        """Load mistake history."""
        memory_file = self.brain_dir / "mistake_learning.json"
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.mistake_log = data.get("mistakes", [])
                self.corrections = data.get("corrections", {})
                self.improvement_metrics = data.get("metrics", self.improvement_metrics)
            print(f"✅ Loaded mistake learning memory ({self.improvement_metrics['total_mistakes']} mistakes tracked)")
    
    def save_learning_data(self):
        """Save mistake history."""
        memory_file = self.brain_dir / "mistake_learning.json"
        data = {
            "mistakes": self.mistake_log[-100:],  # Keep last 100
            "corrections": self.corrections,
            "metrics": self.improvement_metrics,
            "last_updated": datetime.now().isoformat()
        }
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def log_mistake(
        self,
        category: str,
        description: str,
        context: Dict[str, Any]
    ):
        """Log a mistake for learning."""
        mistake = {
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "description": description,
            "context": context,
            "corrected": False
        }
        
        self.mistake_log.append(mistake)
        self.improvement_metrics["total_mistakes"] += 1
        self.save_learning_data()
        
        print(f"⚠️  Logged mistake: {category} - {description}")
    
    def apply_correction(
        self,
        mistake_category: str,
        correction_rule: str
    ):
        """Apply a correction rule for a category of mistakes."""
        if mistake_category not in self.corrections:
            self.corrections[mistake_category] = []
        
        self.corrections[mistake_category].append({
            "rule": correction_rule,
            "applied_at": datetime.now().isoformat()
        })
        
        self.improvement_metrics["corrected"] += 1
        self.improvement_metrics["improvement_rate"] = (
            self.improvement_metrics["corrected"] / 
            max(self.improvement_metrics["total_mistakes"], 1)
        )
        
        self.save_learning_data()
        print(f"✅ Applied correction: {correction_rule}")
    
    def get_improvement_report(self) -> str:
        """Generate improvement report."""
        report = f"""
🧠 LEARNING PROGRESS REPORT
===========================
Total Mistakes Tracked: {self.improvement_metrics['total_mistakes']}
Corrections Applied: {self.improvement_metrics['corrected']}
Improvement Rate: {self.improvement_metrics['improvement_rate']:.1%}

Recent Corrections:
"""
        for category, corrections in self.corrections.items():
            report += f"\n{category}:\n"
            for corr in corrections[-3:]:  # Last 3
                report += f"  - {corr['rule']}\n"
        
        return report


class SelfLearningVisualBrain:
    """
    Master brain that coordinates all learning systems.
    """
    
    def __init__(self, brain_dir: str = "brain_memory"):
        self.brain_dir = Path(brain_dir)
        self.brain_dir.mkdir(exist_ok=True)
        
        print("🧠 Initializing Self-Learning Visual Brain...")
        
        # Initialize subsystems
        self.color_intelligence = ColorIntelligence(brain_dir)
        self.behavior_understanding = BehaviorUnderstanding(brain_dir)
        self.emotion_detection = EmotionDetection(brain_dir)
        self.mistake_learning = MistakeLearningSystem(brain_dir)
        
        print("✅ Self-Learning Visual Brain ready!")
        print(f"📊 Brain memory location: {self.brain_dir}")
    
    def analyze_scene_comprehensively(
        self,
        scene_data: Dict
    ) -> Dict[str, Any]:
        """
        Comprehensive scene analysis using all learning systems.
        """
        print(f"\n🧠 Analyzing scene {scene_data.get('scene_id', 0)} with AI brain...")
        
        analysis = {
            "scene_id": scene_data.get("scene_id", 0),
            "colors": {},
            "behaviors": [],
            "emotions": [],
            "recommendations": []
        }
        
        # Analyze emotions from scene
        scene_emotion = scene_data.get("emotion", "neutral")
        
        # Get intelligent color scheme
        colors = self.color_intelligence.get_colors_for_emotion(
            scene_emotion,
            cultural_context=scene_data.get("context", "")
        )
        analysis["colors"] = colors
        
        # Analyze each dialogue
        for dialogue in scene_data.get("dialogues", []):
            text = dialogue.get("text", "")
            character = dialogue.get("character", "")
            
            # Detect emotion in dialogue
            emotion_result = self.emotion_detection.detect_emotion(text, scene_emotion)
            analysis["emotions"].append({
                "character": character,
                "detected_emotion": emotion_result["emotion"],
                "confidence": emotion_result["confidence"],
                "keywords": emotion_result["matched_keywords"]
            })
            
            # Detect behaviors
            behaviors = self.behavior_understanding.detect_behavior(text)
            if behaviors:
                analysis["behaviors"].extend([
                    {"character": character, **b} for b in behaviors
                ])
        
        # Generate recommendations
        if analysis["behaviors"]:
            analysis["recommendations"].append(
                f"Animate {len(analysis['behaviors'])} detected behaviors"
            )
        
        if any(e["confidence"] > 0.7 for e in analysis["emotions"]):
            analysis["recommendations"].append(
                "Strong emotions detected - emphasize visual expression"
            )
        
        return analysis
    
    def learn_from_feedback(
        self,
        scene_id: int,
        feedback_type: str,
        feedback_data: Dict
    ):
        """
        Learn from user feedback or automated metrics.
        """
        if feedback_type == "color_success":
            emotion = feedback_data.get("emotion")
            success = feedback_data.get("success", True)
            self.color_intelligence.learn_from_feedback(emotion, success)
        
        elif feedback_type == "emotion_correction":
            text = feedback_data.get("text")
            detected = feedback_data.get("detected_emotion")
            correct = feedback_data.get("correct_emotion")
            self.emotion_detection.learn_from_correction(text, detected, correct)
        
        elif feedback_type == "mistake":
            self.mistake_learning.log_mistake(
                category=feedback_data.get("category", "general"),
                description=feedback_data.get("description", ""),
                context=feedback_data
            )
    
    def get_learning_report(self) -> str:
        """Get comprehensive learning report."""
        report = "="*70 + "\n"
        report += "🧠 SELF-LEARNING VISUAL BRAIN - STATUS REPORT\n"
        report += "="*70 + "\n\n"
        
        report += "COLOR INTELLIGENCE:\n"
        for emotion, data in self.color_intelligence.emotion_colors.items():
            if data["usage_count"] > 0:
                report += f"  {emotion}: {data['usage_count']} uses, "
                report += f"{data['success_rate']:.1%} success\n"
        
        report += "\nBEHAVIOR UNDERSTANDING:\n"
        for behavior, data in self.behavior_understanding.behavior_patterns.items():
            if len(data["examples"]) > 0:
                report += f"  {behavior}: {len(data['examples'])} examples, "
                report += f"{data['confidence']:.1%} confidence\n"
        
        report += "\nEMOTION DETECTION:\n"
        for emotion, data in self.emotion_detection.emotion_indicators.items():
            if data["detection_count"] > 0:
                report += f"  {emotion}: {data['detection_count']} detections, "
                report += f"{data['accuracy']:.2f} accuracy\n"
        
        report += "\n" + self.mistake_learning.get_improvement_report()
        
        return report


def main():
    """Test self-learning visual brain."""
    print("="*70)
    print("🧠 SELF-LEARNING VISUAL AI BRAIN - Test Mode")
    print("="*70)
    
    # Initialize brain
    brain = SelfLearningVisualBrain()
    
    # Test scene
    test_scene = {
        "scene_id": 0,
        "emotion": "happy",
        "context": "celebration",
        "dialogues": [
            {
                "character": "ਕੁਲਵੰਤ",
                "text": "ਪਿੰਡ ਵਿੱਚ ਬਹੁਤ ਖੁਸ਼ੀ ਹੈ, ਸਾਰੇ ਨੱਚ ਰਹੇ ਹਨ।"
            },
            {
                "character": "ਅਮਨਦੀਪ",
                "text": "ਹਾਂ ਪਿਤਾ ਜੀ, ਮੈਂ ਬਹੁਤ ਖੁਸ਼ ਹਾਂ!"
            }
        ]
    }
    
    # Analyze
    analysis = brain.analyze_scene_comprehensively(test_scene)
    
    print("\n📊 SCENE ANALYSIS:")
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
    
    # Simulate learning from feedback
    print("\n🎓 LEARNING FROM FEEDBACK...")
    brain.learn_from_feedback(0, "color_success", {
        "emotion": "happy",
        "success": True
    })
    
    # Get report
    print("\n" + brain.get_learning_report())
    
    print("\n✅ Self-learning brain test complete!")
    print(f"💾 Memory saved in: {brain.brain_dir}")


if __name__ == "__main__":
    main()
