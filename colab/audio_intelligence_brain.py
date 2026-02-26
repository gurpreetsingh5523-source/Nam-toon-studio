"""
🎵 AUDIO INTELLIGENCE BRAIN - Sound Design & Music AI
=====================================================

This brain understands and creates:
1. Background Music - Emotion-based music selection
2. Sound Effects (SFX) - Action-synchronized sounds
3. Natural Sounds - Wind, birds, water, village ambience
4. Musical Instruments - Tabla, dhol, tumbi, sarangi, harmonium
5. Cultural Audio - Sikh kirtan, punjabi folk music
6. Dynamic Mixing - Adjusts levels based on scene intensity

Learns from:
- Which sounds work well together
- Optimal volume levels
- Cultural appropriateness
- Emotional impact

Author: Amrit Core Team
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import random
import math

try:
    import numpy as np
except ImportError:
    os.system("pip install numpy")
    import numpy as np


class AudioIntelligence:
    """
    Intelligent audio selection and mixing based on scene context.
    """
    
    def __init__(self, brain_dir: str = "brain_memory"):
        self.brain_dir = Path(brain_dir)
        self.brain_dir.mkdir(exist_ok=True)
        
        # Music library (emotion-based)
        self.music_library = {
            "happy": {
                "tracks": ["punjabi_folk_happy.mp3", "dhol_celebration.mp3", "tumbi_joyful.mp3"],
                "instruments": ["dhol", "tumbi", "chimta", "algoza"],
                "tempo": "fast",
                "volume_base": 0.6,
                "success_rate": 0.0,
                "usage_count": 0
            },
            "sad": {
                "tracks": ["sarangi_melancholy.mp3", "flute_sorrow.mp3", "harmonium_sad.mp3"],
                "instruments": ["sarangi", "flute", "harmonium", "ektar"],
                "tempo": "slow",
                "volume_base": 0.4,
                "success_rate": 0.0,
                "usage_count": 0
            },
            "angry": {
                "tracks": ["dhol_intense.mp3", "tabla_aggressive.mp3", "drums_war.mp3"],
                "instruments": ["dhol", "nagara", "dhad", "tabla"],
                "tempo": "very_fast",
                "volume_base": 0.7,
                "success_rate": 0.0,
                "usage_count": 0
            },
            "peaceful": {
                "tracks": ["harmonium_calm.mp3", "nature_peaceful.mp3", "kirtan_soft.mp3"],
                "instruments": ["harmonium", "tanpura", "dilruba"],
                "tempo": "slow",
                "volume_base": 0.3,
                "success_rate": 0.0,
                "usage_count": 0
            },
            "romantic": {
                "tracks": ["flute_love.mp3", "sarangi_romantic.mp3", "sitar_gentle.mp3"],
                "instruments": ["flute", "sarangi", "sitar", "tanpura"],
                "tempo": "medium",
                "volume_base": 0.4,
                "success_rate": 0.0,
                "usage_count": 0
            },
            "spiritual": {
                "tracks": ["kirtan_divine.mp3", "harmonium_prayer.mp3", "tabla_kirtan.mp3"],
                "instruments": ["harmonium", "tabla", "tanpura", "manjira"],
                "tempo": "medium",
                "volume_base": 0.5,
                "success_rate": 0.0,
                "usage_count": 0
            },
            "tense": {
                "tracks": ["suspense_low.mp3", "tabla_tension.mp3", "drone_ominous.mp3"],
                "instruments": ["tabla", "tanpura_low", "dhad"],
                "tempo": "varied",
                "volume_base": 0.5,
                "success_rate": 0.0,
                "usage_count": 0
            }
        }
        
        # Sound effects library (action-based)
        self.sfx_library = {
            "walking": {
                "sounds": ["footsteps_dirt.wav", "walking_grass.wav"],
                "volume": 0.3,
                "cultural_context": "village_paths",
                "success_rate": 0.0
            },
            "running": {
                "sounds": ["running_fast.wav", "footsteps_running.wav"],
                "volume": 0.4,
                "cultural_context": "urgency",
                "success_rate": 0.0
            },
            "crying": {
                "sounds": ["sobbing.wav", "tears.wav", "sniffling.wav"],
                "volume": 0.5,
                "cultural_context": "emotional",
                "success_rate": 0.0
            },
            "laughing": {
                "sounds": ["laughter.wav", "chuckle.wav", "giggle.wav"],
                "volume": 0.4,
                "cultural_context": "joyful",
                "success_rate": 0.0
            },
            "door": {
                "sounds": ["door_open.wav", "door_close.wav", "door_creak.wav"],
                "volume": 0.4,
                "cultural_context": "home",
                "success_rate": 0.0
            },
            "farming": {
                "sounds": ["plow_field.wav", "harvesting.wav", "wheat_rustle.wav"],
                "volume": 0.3,
                "cultural_context": "agriculture",
                "success_rate": 0.0
            },
            "prayer": {
                "sounds": ["bell_temple.wav", "prayer_beads.wav", "incense.wav"],
                "volume": 0.3,
                "cultural_context": "spiritual",
                "success_rate": 0.0
            },
            "celebration": {
                "sounds": ["dhol_beat.wav", "clapping.wav", "cheering.wav"],
                "volume": 0.6,
                "cultural_context": "festival",
                "success_rate": 0.0
            }
        }
        
        # Natural ambient sounds
        self.ambient_sounds = {
            "village_day": {
                "sounds": ["birds_chirping.wav", "village_ambience.wav", "distant_voices.wav"],
                "volume": 0.2,
                "time": "day",
                "weather": "clear",
                "success_rate": 0.0
            },
            "village_night": {
                "sounds": ["crickets.wav", "night_ambience.wav", "owl.wav"],
                "volume": 0.15,
                "time": "night",
                "weather": "clear",
                "success_rate": 0.0
            },
            "wind_gentle": {
                "sounds": ["wind_soft.wav", "leaves_rustle.wav"],
                "volume": 0.2,
                "time": "any",
                "weather": "breezy",
                "success_rate": 0.0
            },
            "wind_strong": {
                "sounds": ["wind_strong.wav", "storm_approaching.wav"],
                "volume": 0.4,
                "time": "any",
                "weather": "stormy",
                "success_rate": 0.0
            },
            "rain": {
                "sounds": ["rain_light.wav", "rain_heavy.wav", "thunder.wav"],
                "volume": 0.3,
                "time": "any",
                "weather": "rainy",
                "success_rate": 0.0
            },
            "farm_field": {
                "sounds": ["wheat_field.wav", "tractor.wav", "birds_field.wav"],
                "volume": 0.25,
                "time": "day",
                "weather": "clear",
                "success_rate": 0.0
            },
            "river": {
                "sounds": ["river_flowing.wav", "water_stream.wav"],
                "volume": 0.3,
                "time": "any",
                "weather": "clear",
                "success_rate": 0.0
            },
            "home_interior": {
                "sounds": ["home_ambience.wav", "clock_ticking.wav", "fire_crackling.wav"],
                "volume": 0.15,
                "time": "any",
                "weather": "any",
                "success_rate": 0.0
            }
        }
        
        # Musical instruments database (Punjabi/Indian)
        self.instruments = {
            "dhol": {
                "type": "percussion",
                "emotion": ["happy", "celebratory", "energetic"],
                "cultural": "punjabi_traditional",
                "volume": 0.6
            },
            "tumbi": {
                "type": "string",
                "emotion": ["happy", "folk", "rural"],
                "cultural": "punjabi_folk",
                "volume": 0.5
            },
            "sarangi": {
                "type": "string",
                "emotion": ["sad", "romantic", "deep"],
                "cultural": "classical_indian",
                "volume": 0.4
            },
            "flute": {
                "type": "wind",
                "emotion": ["peaceful", "romantic", "spiritual"],
                "cultural": "universal",
                "volume": 0.4
            },
            "tabla": {
                "type": "percussion",
                "emotion": ["spiritual", "rhythmic", "cultural"],
                "cultural": "indian_classical",
                "volume": 0.5
            },
            "harmonium": {
                "type": "keyboard",
                "emotion": ["spiritual", "devotional", "peaceful"],
                "cultural": "sikh_kirtan",
                "volume": 0.5
            },
            "algoza": {
                "type": "wind",
                "emotion": ["folk", "pastoral", "happy"],
                "cultural": "punjabi_folk",
                "volume": 0.4
            },
            "chimta": {
                "type": "percussion",
                "emotion": ["celebratory", "rhythmic"],
                "cultural": "punjabi_bhangra",
                "volume": 0.3
            }
        }
        
        self.load_learning_data()
    
    def load_learning_data(self):
        """Load learned audio patterns."""
        memory_file = self.brain_dir / "audio_intelligence.json"
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                # Merge learned data
                for category in ['music_library', 'sfx_library', 'ambient_sounds']:
                    if category in saved_data:
                        for key, data in saved_data[category].items():
                            if key in getattr(self, category):
                                getattr(self, category)[key].update(data)
            print("✅ Loaded audio intelligence memory")
    
    def save_learning_data(self):
        """Save learned patterns."""
        memory_file = self.brain_dir / "audio_intelligence.json"
        data = {
            "music_library": self.music_library,
            "sfx_library": self.sfx_library,
            "ambient_sounds": self.ambient_sounds,
            "instruments": self.instruments,
            "last_updated": datetime.now().isoformat()
        }
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def select_background_music(
        self,
        emotion: str,
        intensity: float = 0.5,
        cultural_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Select appropriate background music based on emotion and context.
        """
        emotion_clean = emotion.lower().strip()
        
        # Get music data
        music_data = self.music_library.get(emotion_clean, self.music_library["peaceful"])
        
        # Adjust for cultural context
        if cultural_context:
            if "prayer" in cultural_context.lower() or "spiritual" in cultural_context.lower():
                music_data = self.music_library["spiritual"]
            elif "celebration" in cultural_context.lower():
                music_data = self.music_library["happy"]
        
        # Select track
        track = random.choice(music_data["tracks"])
        
        # Calculate volume based on intensity
        base_volume = music_data["volume_base"]
        adjusted_volume = base_volume * (0.5 + intensity * 0.5)
        
        # Track usage
        music_data["usage_count"] += 1
        self.save_learning_data()
        
        return {
            "track": track,
            "volume": adjusted_volume,
            "tempo": music_data["tempo"],
            "instruments": music_data["instruments"],
            "emotion": emotion_clean
        }
    
    def select_sound_effects(
        self,
        behaviors: List[str],
        scene_context: str = "village"
    ) -> List[Dict[str, Any]]:
        """
        Select appropriate SFX based on detected behaviors.
        """
        selected_sfx = []
        
        for behavior in behaviors:
            behavior_clean = behavior.lower().strip()
            
            if behavior_clean in self.sfx_library:
                sfx_data = self.sfx_library[behavior_clean]
                
                # Select sound file
                sound = random.choice(sfx_data["sounds"])
                
                selected_sfx.append({
                    "behavior": behavior_clean,
                    "sound": sound,
                    "volume": sfx_data["volume"],
                    "context": sfx_data["cultural_context"]
                })
        
        return selected_sfx
    
    def select_ambient_sound(
        self,
        location: str = "village",
        time_of_day: str = "day",
        weather: str = "clear",
        emotion: str = "neutral"
    ) -> Dict[str, Any]:
        """
        Select appropriate ambient/natural sounds.
        """
        # Match ambient sound to context
        ambient_key = f"{location}_{time_of_day}"
        
        # Try specific location+time
        if ambient_key in self.ambient_sounds:
            ambient_data = self.ambient_sounds[ambient_key]
        # Try just location
        elif location in self.ambient_sounds:
            ambient_data = self.ambient_sounds[location]
        else:
            ambient_data = self.ambient_sounds["village_day"]
        
        # Override for weather
        if weather == "rainy":
            ambient_data = self.ambient_sounds["rain"]
        elif weather == "stormy":
            ambient_data = self.ambient_sounds["wind_strong"]
        elif weather == "breezy":
            ambient_data = self.ambient_sounds["wind_gentle"]
        
        # Select sound
        sound = random.choice(ambient_data["sounds"])
        
        # Adjust volume for emotion
        volume = ambient_data["volume"]
        if emotion in ["tense", "fearful"]:
            volume *= 0.7  # Reduce ambient for tense scenes
        
        return {
            "sound": sound,
            "volume": volume,
            "time": time_of_day,
            "weather": weather,
            "location": location
        }
    
    def create_audio_mix(
        self,
        scene_data: Dict,
        analysis: Dict
    ) -> Dict[str, Any]:
        """
        Create complete audio mix for a scene.
        Combines music, SFX, and ambient sounds intelligently.
        """
        emotion = scene_data.get("emotion", "neutral")
        context = scene_data.get("context", "")
        
        # Background music
        music = self.select_background_music(
            emotion,
            intensity=analysis.get("intensity", 0.5),
            cultural_context=context
        )
        
        # Sound effects from behaviors
        behaviors = [b.get("behavior", "") for b in analysis.get("behaviors", [])]
        sfx = self.select_sound_effects(behaviors, context)
        
        # Ambient sounds
        ambient = self.select_ambient_sound(
            location=scene_data.get("location", "village"),
            time_of_day=scene_data.get("time", "day"),
            weather=scene_data.get("weather", "clear"),
            emotion=emotion
        )
        
        # Mix levels (ensure dialogue clarity)
        mix = {
            "music": music,
            "sound_effects": sfx,
            "ambient": ambient,
            "dialogue_volume": 1.0,  # Always full volume for dialogue
            "mix_strategy": self.determine_mix_strategy(emotion, len(sfx))
        }
        
        return mix
    
    def determine_mix_strategy(
        self,
        emotion: str,
        sfx_count: int
    ) -> Dict[str, float]:
        """
        Determine optimal mixing levels for all audio layers.
        """
        strategy = {
            "dialogue": 1.0,  # Always prioritize dialogue
            "music": 0.6,
            "sfx": 0.7,
            "ambient": 0.3
        }
        
        # Adjust based on emotion
        if emotion in ["tense", "fearful"]:
            strategy["music"] = 0.4
            strategy["ambient"] = 0.5  # More ambient for tension
        elif emotion in ["happy", "celebratory"]:
            strategy["music"] = 0.7
            strategy["sfx"] = 0.8
        elif emotion in ["sad", "tragic"]:
            strategy["music"] = 0.5
            strategy["ambient"] = 0.2
        
        # Reduce music if many SFX
        if sfx_count > 3:
            strategy["music"] *= 0.7
        
        return strategy
    
    def learn_from_audio_feedback(
        self,
        audio_type: str,
        key: str,
        success: bool
    ):
        """
        Learn from feedback on audio choices.
        """
        if audio_type == "music":
            if key in self.music_library:
                data = self.music_library[key]
                current = data["success_rate"]
                count = data["usage_count"]
                if count > 0:
                    new_rate = (current * (count - 1) + (1.0 if success else 0.0)) / count
                    data["success_rate"] = new_rate
                    self.save_learning_data()
                    print(f"🎵 Learned: {key} music → {data['success_rate']:.1%} success")


class AudioIntelligenceBrain:
    """
    Master audio brain that coordinates all audio intelligence.
    """
    
    def __init__(self, brain_dir: str = "brain_memory"):
        self.brain_dir = Path(brain_dir)
        self.brain_dir.mkdir(exist_ok=True)
        
        print("🎵 Initializing Audio Intelligence Brain...")
        
        self.audio_intelligence = AudioIntelligence(brain_dir)
        
        print("✅ Audio Intelligence Brain ready!")
        print(f"🎼 {len(self.audio_intelligence.music_library)} music categories")
        print(f"🔊 {len(self.audio_intelligence.sfx_library)} SFX types")
        print(f"🌊 {len(self.audio_intelligence.ambient_sounds)} ambient sounds")
        print(f"🎻 {len(self.audio_intelligence.instruments)} instruments")
    
    def analyze_and_design_audio(
        self,
        scene_data: Dict,
        visual_analysis: Dict
    ) -> Dict[str, Any]:
        """
        Analyze scene and design complete audio.
        Works with visual brain's analysis.
        """
        print(f"\n🎵 Designing audio for scene {scene_data.get('scene_id', 0)}...")
        
        # Create audio mix
        audio_mix = self.audio_intelligence.create_audio_mix(scene_data, visual_analysis)
        
        # Log decisions
        print(f"   🎼 Music: {audio_mix['music']['track']} "
              f"(volume: {audio_mix['music']['volume']:.2f})")
        
        if audio_mix['sound_effects']:
            print(f"   🔊 SFX: {len(audio_mix['sound_effects'])} effects")
            for sfx in audio_mix['sound_effects']:
                print(f"      - {sfx['behavior']}: {sfx['sound']}")
        
        print(f"   🌊 Ambient: {audio_mix['ambient']['sound']} "
              f"({audio_mix['ambient']['location']}, {audio_mix['ambient']['time']})")
        
        return audio_mix
    
    def get_learning_report(self) -> str:
        """Get audio learning report."""
        report = "="*70 + "\n"
        report += "🎵 AUDIO INTELLIGENCE BRAIN - STATUS REPORT\n"
        report += "="*70 + "\n\n"
        
        report += "MUSIC SELECTIONS:\n"
        for emotion, data in self.audio_intelligence.music_library.items():
            if data["usage_count"] > 0:
                report += f"  {emotion}: {data['usage_count']} uses, "
                report += f"{data['success_rate']:.1%} success\n"
        
        report += "\nSOUND EFFECTS:\n"
        for sfx, data in self.audio_intelligence.sfx_library.items():
            if data.get("success_rate", 0) > 0:
                report += f"  {sfx}: {data['success_rate']:.1%} success\n"
        
        return report


def main():
    """Test audio intelligence brain."""
    print("="*70)
    print("🎵 AUDIO INTELLIGENCE BRAIN - Test Mode")
    print("="*70)
    
    # Initialize
    brain = AudioIntelligenceBrain()
    
    # Test scene
    test_scene = {
        "scene_id": 0,
        "emotion": "happy",
        "context": "celebration",
        "location": "village",
        "time": "day",
        "weather": "clear"
    }
    
    test_analysis = {
        "intensity": 0.8,
        "behaviors": [
            {"behavior": "laughing"},
            {"behavior": "celebration"}
        ]
    }
    
    # Design audio
    audio_mix = brain.analyze_and_design_audio(test_scene, test_analysis)
    
    print("\n📊 COMPLETE AUDIO MIX:")
    print(json.dumps(audio_mix, indent=2, ensure_ascii=False))
    
    # Learn from feedback
    brain.audio_intelligence.learn_from_audio_feedback("music", "happy", True)
    
    print("\n" + brain.get_learning_report())
    print("\n✅ Audio intelligence test complete!")


if __name__ == "__main__":
    main()
