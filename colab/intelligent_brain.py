"""Intelligent Brain for Nam-toon Studio (Enhanced with Creative Logic)
Automatically analyzes story context and makes smart decisions about:
- Voice characteristics (age, gender, emotion → pitch/speed modulation)
- Animation style (mood → movement type)
- Background music (scene emotion → audio selection)
- Visual timing (rhythm and pacing)
- Behavior learning (character action patterns)
- Multi-sensory perception (audio-visual synchronization)
"""
import re
import json
import time
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class IntelligentBrain:
    """The thinking brain that analyzes story context and makes production decisions."""
    
    def __init__(self):
        self.character_profiles = {}  # Learned character traits
        self.scene_emotions = {}      # Scene-by-scene emotional analysis
        self.music_library = self._init_music_library()
        self.behavior_database = self._init_behavior_database()  # Character actions
        self.timing_patterns = {}     # Rhythm and pacing memory
        self.learning_memory = {}     # Cross-scene learning and patterns
        self.visual_hints = {}        # Camera movement and visual style hints
        
    def _init_music_library(self):
        """Define available background music by mood."""
        return {
            'happy': {'file': 'birds.wav', 'volume': 0.15, 'rhythm': '4/4', 'tempo': 'allegro'},
            'sad': {'file': 'rain.wav', 'volume': 0.12, 'rhythm': '3/4', 'tempo': 'adagio'},
            'tense': {'file': 'heartbeat.wav', 'volume': 0.18, 'rhythm': 'irregular', 'tempo': 'presto'},
            'peaceful': {'file': 'flute.wav', 'volume': 0.10, 'rhythm': '6/8', 'tempo': 'andante'},
            'tragic': {'file': 'strings.wav', 'volume': 0.20, 'rhythm': '4/4', 'tempo': 'largo'},
            'angry': {'file': 'drums.wav', 'volume': 0.22, 'rhythm': '2/4', 'tempo': 'vivace'},
            'neutral': {'file': 'ambient.wav', 'volume': 0.08, 'rhythm': 'free', 'tempo': 'moderato'},
        }
    
    def _init_behavior_database(self):
        """Initialize behavior patterns (character actions and movements)."""
        return {
            # Emotional behaviors
            'crying': {'animation': 'shake_subtle', 'duration': 2.5, 'visual_hint': 'facial contort, tears'},
            'laughing': {'animation': 'bounce_gentle', 'duration': 1.8, 'visual_hint': 'facial relax, joy'},
            'shouting': {'animation': 'pulse_intense', 'duration': 1.2, 'visual_hint': 'mouth open, aggressive'},
            'whispering': {'animation': 'still_close', 'duration': 3.0, 'visual_hint': 'minimal movement'},
            
            # Physical behaviors
            'walking': {'animation': 'pan_smooth', 'duration': 4.5, 'visual_hint': 'lateral movement'},
            'running': {'animation': 'pan_fast', 'duration': 2.0, 'visual_hint': 'rapid lateral shift'},
            'sitting': {'animation': 'zoom_in_slow', 'duration': 3.5, 'visual_hint': 'stable, focused'},
            'standing': {'animation': 'zoom_out', 'duration': 2.0, 'visual_hint': 'establishing presence'},
            
            # Contextual behaviors (Punjabi cultural)
            'prayer': {'animation': 'still_sacred', 'duration': 5.0, 'visual_hint': 'hands folded, calm'},
            'farming': {'animation': 'sway_rhythmic', 'duration': 6.0, 'visual_hint': 'repetitive motion'},
            'celebration': {'animation': 'bounce_energetic', 'duration': 3.0, 'visual_hint': 'dynamic, colorful'},
            'mourning': {'animation': 'drift_down', 'duration': 4.5, 'visual_hint': 'slow descent, muted'},
        }
    
    # ========== CHARACTER ANALYSIS ==========
    
    def analyze_character(self, name: str, dialogue_text: str = '', context_text: str = ''):
        """Analyze character traits from name and context.
        
        Returns profile with:
        - age_group: 'child', 'young_adult', 'adult', 'elder'
        - gender: 'male', 'female', 'neutral'
        - base_emotion: 'calm', 'energetic', 'sad', 'angry'
        """
        profile = {
            'name': name,
            'age_group': 'adult',      # default
            'gender': 'neutral',       # default
            'base_emotion': 'calm',    # default
            'voice_pitch': 1.0,        # 1.0 = normal, <1.0 = lower, >1.0 = higher
            'voice_speed': 1.0,        # 1.0 = normal, <1.0 = slower, >1.0 = faster
        }
        
        name_lower = name.lower()
        combined_text = (dialogue_text + ' ' + context_text).lower()
        
        # === AGE DETECTION ===
        # Punjabi age indicators
        if any(word in combined_text for word in ['ਬੱਚਾ', 'ਬੱਚੀ', 'child', 'kid']):
            profile['age_group'] = 'child'
        elif any(word in combined_text for word in ['ਬੁੱਢਾ', 'ਬੁੱਢੀ', 'ਬਜ਼ੁਰਗ', 'old', 'elder', 'grandfather', 'grandmother']):
            profile['age_group'] = 'elder'
        elif any(word in combined_text for word in ['ਜਵਾਨ', 'young', 'youth']):
            profile['age_group'] = 'young_adult'
        
        # Age from name patterns (Punjabi names)
        if 'ਦੀਪ' in name or 'deep' in name_lower:
            profile['age_group'] = 'young_adult'  # -deep suffix common in young names
        
        # === GENDER DETECTION ===
        # Punjabi gender indicators
        if any(word in name for word in ['ਕੌਰ', 'ਦੇਵੀ']) or any(word in name_lower for word in ['kaur', 'devi', 'preet', 'jeet']):
            profile['gender'] = 'female'
        elif any(word in name for word in ['ਸਿੰਘ']) or any(word in name_lower for word in ['singh', 'deep', 'pal', 'jit']):
            profile['gender'] = 'male'
        
        # Gender from context
        if any(word in combined_text for word in ['ਉਹ ਇੱਕ ਔਰਤ', 'she', 'her', 'wife', 'mother', 'sister', 'ਪਤਨੀ', 'ਮਾਂ', 'ਭੈਣ']):
            profile['gender'] = 'female'
        elif any(word in combined_text for word in ['ਉਹ ਇੱਕ ਆਦਮੀ', 'he', 'him', 'husband', 'father', 'brother', 'ਪਤੀ', 'ਪਿਤਾ', 'ਭਰਾ']):
            profile['gender'] = 'male'
        
        # === EMOTION DETECTION ===
        # Look for emotional keywords in dialogue/context
        if any(word in combined_text for word in ['ਖੁਸ਼', 'ਹੱਸ', 'happy', 'laugh', 'smile', 'joy']):
            profile['base_emotion'] = 'happy'
        elif any(word in combined_text for word in ['ਗੁੱਸਾ', 'ਕ੍ਰੋਧ', 'angry', 'furious', 'rage', 'shout']):
            profile['base_emotion'] = 'angry'
        elif any(word in combined_text for word in ['ਦੁੱਖ', 'ਉਦਾਸ', 'sad', 'cry', 'tears', 'grief', 'ਰੋ']):
            profile['base_emotion'] = 'sad'
        elif any(word in combined_text for word in ['ਡਰ', 'ਘਬਰਾ', 'fear', 'scared', 'panic', 'worried']):
            profile['base_emotion'] = 'fearful'
        
        # === VOICE MODULATION CALCULATION ===
        # Age affects pitch and speed
        if profile['age_group'] == 'child':
            profile['voice_pitch'] = 1.3   # Higher pitch
            profile['voice_speed'] = 1.2   # Faster speech
        elif profile['age_group'] == 'elder':
            profile['voice_pitch'] = 0.85  # Lower pitch
            profile['voice_speed'] = 0.85  # Slower speech
        elif profile['age_group'] == 'young_adult':
            profile['voice_pitch'] = 1.1
            profile['voice_speed'] = 1.05
        
        # Gender affects pitch
        if profile['gender'] == 'female':
            profile['voice_pitch'] *= 1.15  # 15% higher for female
        elif profile['gender'] == 'male':
            profile['voice_pitch'] *= 0.90  # 10% lower for male
        
        # Emotion affects speed and pitch
        if profile['base_emotion'] == 'angry':
            profile['voice_speed'] *= 1.15
            profile['voice_pitch'] *= 1.05
        elif profile['base_emotion'] == 'sad':
            profile['voice_speed'] *= 0.85
            profile['voice_pitch'] *= 0.95
        elif profile['base_emotion'] == 'happy':
            profile['voice_speed'] *= 1.1
            profile['voice_pitch'] *= 1.08
        elif profile['base_emotion'] == 'fearful':
            profile['voice_speed'] *= 1.2
            profile['voice_pitch'] *= 1.12
        
        # Cache the profile
        self.character_profiles[name] = profile
        return profile
    
    # ========== SCENE EMOTION ANALYSIS ==========
    
    def analyze_scene_emotion(self, scene_text: str, scene_title: str = '') -> dict:
        """Analyze emotional tone of entire scene.
        
        Returns:
        - emotion: 'happy', 'sad', 'tense', 'peaceful', 'tragic', 'angry', 'neutral'
        - intensity: 0.0 to 1.0
        - music_choice: recommended background music
        """
        text_lower = scene_text.lower()
        title_lower = scene_title.lower()
        
        emotion_scores = {
            'happy': 0,
            'sad': 0,
            'tense': 0,
            'peaceful': 0,
            'tragic': 0,
            'angry': 0,
            'neutral': 0,
        }
        
        # === KEYWORD ANALYSIS ===
        # Happy indicators
        happy_words = ['ਖੁਸ਼', 'ਹੱਸ', 'ਮੁਸਕਾਨ', 'happy', 'joy', 'smile', 'laugh', 'celebration', 'ਤਿਉਹਾਰ', 'ਵਿਆਹ']
        emotion_scores['happy'] = sum(1 for w in happy_words if w in text_lower or w in title_lower)
        
        # Sad indicators
        sad_words = ['ਦੁੱਖ', 'ਉਦਾਸ', 'ਰੋ', 'sad', 'cry', 'tears', 'grief', 'sorrow', 'ਅੱਥਰੂ']
        emotion_scores['sad'] = sum(1 for w in sad_words if w in text_lower or w in title_lower)
        
        # Tragic indicators
        tragic_words = ['ਮੌਤ', 'ਅੱਗ', 'ਜਲ', 'ਹਾਦਸਾ', 'death', 'fire', 'tragedy', 'accident', 'kill', 'die', 'ਖ਼ਤਮ']
        emotion_scores['tragic'] = sum(2 for w in tragic_words if w in text_lower or w in title_lower)  # 2x weight
        
        # Angry indicators
        angry_words = ['ਗੁੱਸਾ', 'ਕ੍ਰੋਧ', 'ਚੀਕ', 'angry', 'rage', 'furious', 'shout', 'fight', 'ਲੜਾਈ', 'ਜ਼ੁਲਮ']
        emotion_scores['angry'] = sum(1 for w in angry_words if w in text_lower or w in title_lower)
        
        # Tense indicators
        tense_words = ['ਡਰ', 'ਘਬਰਾ', 'ਪੁਲਿਸ', 'fear', 'scared', 'police', 'threat', 'danger', 'ਖ਼ਤਰਾ', 'ਧਮਕੀ']
        emotion_scores['tense'] = sum(1 for w in tense_words if w in text_lower or w in title_lower)
        
        # Peaceful indicators
        peaceful_words = ['ਸ਼ਾਂਤ', 'ਸੁਕੂਨ', 'ਬਾਗ', 'peaceful', 'calm', 'quiet', 'garden', 'nature', 'ਪ੍ਰਕਿਰਤੀ']
        emotion_scores['peaceful'] = sum(1 for w in peaceful_words if w in text_lower or w in title_lower)
        
        # Find dominant emotion
        max_score = max(emotion_scores.values())
        if max_score == 0:
            dominant_emotion = 'neutral'
            intensity = 0.3
        else:
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            intensity = min(1.0, max_score / 5.0)  # Normalize to 0-1
        
        # Special case: multiple strong emotions = tense
        strong_emotions = [k for k, v in emotion_scores.items() if v >= 2]
        if len(strong_emotions) >= 2:
            dominant_emotion = 'tense'
            intensity = 0.8
        
        # Select music
        music_choice = self.music_library.get(dominant_emotion, self.music_library['neutral'])
        
        result = {
            'emotion': dominant_emotion,
            'intensity': intensity,
            'music_file': music_choice['file'],
            'music_volume': music_choice['volume'] * intensity,
            'scores': emotion_scores,
        }
        
        return result
    
    # ========== ANIMATION STYLE DECISION ==========
    
    def decide_animation_style(self, emotion: str, intensity: float) -> dict:
        """Decide animation parameters based on emotion.
        
        Returns:
        - movement_type: 'still', 'gentle', 'normal', 'intense', 'chaotic'
        - zoom_speed: multiplier for Ken Burns zoom
        - pan_direction: 'left', 'right', 'up', 'down', 'center'
        - color_intensity: tint strength (0.0-1.0)
        """
        style = {
            'movement_type': 'normal',
            'zoom_speed': 1.0,
            'pan_direction': 'center',
            'color_intensity': 0.3,
        }
        
        if emotion == 'peaceful':
            style['movement_type'] = 'gentle'
            style['zoom_speed'] = 0.7
            style['pan_direction'] = 'center'
            style['color_intensity'] = 0.2
        
        elif emotion == 'happy':
            style['movement_type'] = 'normal'
            style['zoom_speed'] = 1.2
            style['pan_direction'] = 'up'
            style['color_intensity'] = 0.15
        
        elif emotion == 'sad':
            style['movement_type'] = 'gentle'
            style['zoom_speed'] = 0.8
            style['pan_direction'] = 'down'
            style['color_intensity'] = 0.4
        
        elif emotion == 'angry':
            style['movement_type'] = 'intense'
            style['zoom_speed'] = 1.5
            style['pan_direction'] = 'right'
            style['color_intensity'] = 0.5
        
        elif emotion == 'tragic':
            style['movement_type'] = 'intense'
            style['zoom_speed'] = 1.3
            style['pan_direction'] = 'center'
            style['color_intensity'] = 0.6
        
        elif emotion == 'tense':
            style['movement_type'] = 'chaotic'
            style['zoom_speed'] = 1.4
            style['pan_direction'] = 'left'
            style['color_intensity'] = 0.45
        
        # Scale by intensity
        style['zoom_speed'] *= (0.8 + intensity * 0.4)  # 0.8x to 1.2x
        style['color_intensity'] *= intensity
        
        return style
    
    # ========== BEHAVIOR LEARNING (Character Actions) ==========
    
    def detect_character_behavior(self, dialogue_text: str, scene_text: str = '') -> Optional[str]:
        """Detect what action the character is performing from text context.
        
        Returns behavior name if detected, else None.
        """
        combined = (dialogue_text + ' ' + scene_text).lower()
        
        # Punjabi action keywords
        action_map = {
            'crying': ['ਰੋ', 'ਅੱਥਰੂ', 'cry', 'tears', 'weep'],
            'laughing': ['ਹੱਸ', 'ਮੁਸਕਾਨ', 'laugh', 'smile', 'giggle'],
            'shouting': ['ਚੀਕ', 'ਚਿੱਲਾ', 'shout', 'yell', 'scream'],
            'whispering': ['ਸਰਗੋਸ਼', 'whisper', 'murmur'],
            'walking': ['ਤੁਰ', 'ਚੱਲ', 'walk', 'move', 'step'],
            'running': ['ਦੌੜ', 'run', 'rush', 'flee'],
            'sitting': ['ਬੈਠ', 'sit', 'seated'],
            'standing': ['ਖੜ੍ਹ', 'stand', 'stood'],
            'prayer': ['ਅਰਦਾਸ', 'ਪ੍ਰਾਰਥਨਾ', 'pray', 'worship', 'ਵਾਹਿਗੁਰੂ'],
            'farming': ['ਖੇਤ', 'ਵਾਹੀ', 'farm', 'harvest', 'plow'],
            'celebration': ['ਜਸ਼ਨ', 'ਤਿਉਹਾਰ', 'celebrate', 'festival', 'ਵਿਆਹ'],
            'mourning': ['ਸੋਗ', 'ਮਾਤਮ', 'mourn', 'grief', 'funeral'],
        }
        
        for behavior, keywords in action_map.items():
            if any(kw in combined for kw in keywords):
                return behavior
        
        return None
    
    def learn_new_behavior(self, behavior_name: str, context: str) -> dict:
        """Learn a new behavior pattern from context (self-learning capability).
        
        This simulates the brain observing and learning new actions.
        """
        if behavior_name.lower() in self.behavior_database:
            # Already know this behavior
            return self.behavior_database[behavior_name.lower()]
        
        # Create new behavior profile based on context analysis
        new_behavior = {
            'animation': f'custom_{behavior_name.lower()}',
            'duration': 3.0 + random.uniform(-1.0, 2.0),  # Random but plausible
            'visual_hint': f'Learned from: {context[:50]}...',
            'learned_at': time.time(),
        }
        
        self.behavior_database[behavior_name.lower()] = new_behavior
        self.learning_memory[behavior_name] = {
            'context': context,
            'timestamp': time.time(),
            'usage_count': 0,
        }
        
        return new_behavior
    
    # ========== TIMING AND RHYTHM ANALYSIS ==========
    
    def analyze_dialogue_rhythm(self, dialogues: List[dict]) -> dict:
        """Analyze the rhythm and pacing pattern of dialogues.
        
        Returns timing patterns for dramatic effect.
        """
        if not dialogues:
            return {'pattern': 'steady', 'pace': 'normal'}
        
        # Calculate text length variance (indicates rhythm)
        lengths = [len(d.get('text', '')) for d in dialogues]
        if not lengths:
            return {'pattern': 'steady', 'pace': 'normal'}
        
        avg_len = sum(lengths) / len(lengths)
        variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
        
        # Determine rhythm pattern
        if variance < 100:
            pattern = 'steady'  # Consistent lengths
        elif variance < 500:
            pattern = 'varied'  # Some variation
        else:
            pattern = 'dynamic'  # High variation (dramatic)
        
        # Determine pace from average length
        if avg_len < 30:
            pace = 'rapid'      # Short dialogues = fast pace
        elif avg_len < 80:
            pace = 'normal'     # Medium dialogues
        else:
            pace = 'slow'       # Long dialogues = contemplative
        
        # Store for learning
        rhythm_key = f"{pattern}_{pace}"
        if rhythm_key not in self.timing_patterns:
            self.timing_patterns[rhythm_key] = {'count': 0, 'scenes': []}
        self.timing_patterns[rhythm_key]['count'] += 1
        
        return {
            'pattern': pattern,
            'pace': pace,
            'avg_length': avg_len,
            'variance': variance,
            'dialogue_count': len(dialogues),
            'suggested_pause_duration': 0.5 if pace == 'rapid' else (1.0 if pace == 'normal' else 1.5),
        }
    
    def calculate_scene_timing(self, emotion: str, intensity: float, dialogue_rhythm: dict) -> dict:
        """Calculate optimal timing for scene transitions and pauses.
        
        Combines emotion, intensity, and dialogue rhythm for cinematic timing.
        """
        base_transition = 1.0  # Default 1 second
        
        # Emotion affects transition speed
        emotion_factors = {
            'happy': 0.8,      # Quick cuts
            'sad': 1.5,        # Slow dissolves
            'tragic': 2.0,     # Very slow, heavy
            'angry': 0.6,      # Rapid, jarring
            'tense': 0.7,      # Quick, suspenseful
            'peaceful': 1.3,   # Gentle, flowing
            'neutral': 1.0,    # Standard
        }
        
        transition_duration = base_transition * emotion_factors.get(emotion, 1.0) * (0.8 + intensity * 0.4)
        
        # Rhythm affects internal pacing
        pace = dialogue_rhythm.get('pace', 'normal')
        pace_multiplier = {'rapid': 0.7, 'normal': 1.0, 'slow': 1.3}.get(pace, 1.0)
        
        return {
            'transition_duration': transition_duration,
            'internal_pace_multiplier': pace_multiplier,
            'suggested_fade_in': transition_duration * 0.3,
            'suggested_fade_out': transition_duration * 0.3,
            'pause_before_speech': dialogue_rhythm.get('suggested_pause_duration', 1.0) * pace_multiplier,
        }
    
    # ========== VISUAL PERCEPTION (Camera Logic) ==========
    
    def suggest_camera_movement(self, emotion: str, behavior: Optional[str], intensity: float) -> dict:
        """Suggest camera movement based on emotion, character behavior, and intensity.
        
        This simulates a director's vision for camera work.
        """
        # Base camera style per emotion
        camera_styles = {
            'happy': {'type': 'smooth_pan', 'speed': 'medium', 'direction': 'up_right'},
            'sad': {'type': 'slow_zoom', 'speed': 'slow', 'direction': 'down'},
            'tragic': {'type': 'static_close', 'speed': 'very_slow', 'direction': 'center'},
            'angry': {'type': 'shaky_zoom', 'speed': 'fast', 'direction': 'aggressive'},
            'tense': {'type': 'handheld', 'speed': 'varied', 'direction': 'unpredictable'},
            'peaceful': {'type': 'drift', 'speed': 'very_slow', 'direction': 'circular'},
            'neutral': {'type': 'steady', 'speed': 'medium', 'direction': 'forward'},
        }
        
        base_style = camera_styles.get(emotion, camera_styles['neutral']).copy()
        
        # Modify based on character behavior
        if behavior:
            behavior_data = self.behavior_database.get(behavior, {})
            animation = behavior_data.get('animation', 'zoom_normal')
            
            # Override camera for specific behaviors
            if 'walk' in animation or 'pan' in animation:
                base_style['type'] = 'tracking_shot'
                base_style['direction'] = 'lateral'
            elif 'still' in animation:
                base_style['type'] = 'static_hold'
                base_style['speed'] = 'none'
            elif 'bounce' in animation or 'pulse' in animation:
                base_style['type'] = 'rhythmic_zoom'
        
        # Intensity affects speed and magnitude
        speed_multiplier = 0.5 + intensity * 1.0  # 0.5x to 1.5x
        
        return {
            'camera_type': base_style['type'],
            'camera_speed': base_style['speed'],
            'speed_multiplier': speed_multiplier,
            'camera_direction': base_style['direction'],
            'focal_length': 'wide' if intensity < 0.4 else ('normal' if intensity < 0.7 else 'tight'),
            'suggested_fov': 60 if intensity < 0.4 else (50 if intensity < 0.7 else 35),  # Field of view in degrees
        }
    
    # ========== CROSS-SCENE LEARNING ==========
    
    def learn_from_previous_scenes(self, current_scene_idx: int, all_scenes: List[dict]) -> dict:
        """Learn patterns from previous scenes to inform current scene decisions.
        
        This gives the brain memory and context awareness.
        """
        if current_scene_idx == 0:
            return {'has_context': False, 'suggestion': 'This is the opening scene'}
        
        # Analyze previous scene
        prev_scene = all_scenes[current_scene_idx - 1] if current_scene_idx - 1 < len(all_scenes) else None
        if not prev_scene:
            return {'has_context': False}
        
        prev_analysis = prev_scene.get('brain_analysis', {})
        prev_emotion = prev_analysis.get('emotion', {}).get('emotion', 'neutral')
        
        current_analysis = all_scenes[current_scene_idx].get('brain_analysis', {})
        current_emotion = current_analysis.get('emotion', {}).get('emotion', 'neutral')
        
        # Detect emotional arc transitions
        emotional_shift = self._calculate_emotional_distance(prev_emotion, current_emotion)
        
        learning = {
            'has_context': True,
            'previous_emotion': prev_emotion,
            'current_emotion': current_emotion,
            'emotional_shift': emotional_shift,
            'transition_type': None,
            'narrative_suggestion': '',
        }
        
        # Classify transition type
        if emotional_shift < 0.3:
            learning['transition_type'] = 'continuation'
            learning['narrative_suggestion'] = 'Maintain visual continuity, smooth transition'
        elif emotional_shift < 0.7:
            learning['transition_type'] = 'shift'
            learning['narrative_suggestion'] = 'Gradual change in tone, use crossfade'
        else:
            learning['transition_type'] = 'dramatic_turn'
            learning['narrative_suggestion'] = 'Sharp contrast needed, use hard cut or dramatic pause'
        
        # Store in memory
        transition_key = f"{prev_emotion}_to_{current_emotion}"
        if transition_key not in self.learning_memory:
            self.learning_memory[transition_key] = {'count': 0, 'effectiveness': 0.5}
        self.learning_memory[transition_key]['count'] += 1
        
        return learning
    
    def _calculate_emotional_distance(self, emotion1: str, emotion2: str) -> float:
        """Calculate how different two emotions are (0.0 = same, 1.0 = opposite)."""
        # Emotion similarity map (simplified)
        emotion_coords = {
            'happy': (1.0, 0.8),      # high energy, positive
            'sad': (-0.8, -0.5),      # low energy, negative
            'tragic': (-1.0, -0.9),   # very low energy, very negative
            'angry': (0.8, -0.7),     # high energy, negative
            'tense': (0.6, -0.4),     # medium-high energy, negative
            'peaceful': (-0.5, 0.7),  # low energy, positive
            'neutral': (0.0, 0.0),    # center
        }
        
        coord1 = emotion_coords.get(emotion1, (0, 0))
        coord2 = emotion_coords.get(emotion2, (0, 0))
        
        # Euclidean distance, normalized
        distance = ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5
        max_distance = 2.0  # Approximate max in our space
        
        return min(1.0, distance / max_distance)
    
    # ========== FULL SCENE ANALYSIS (ENHANCED) ==========
    
    def analyze_full_scene(self, scene_data: dict, full_story_text: str = '', scene_index: int = 0, all_scenes: List[dict] = None) -> dict:
        """Complete analysis of a scene with all creative brain decisions.
        
        Input: scene_data from scenes.json
        Returns: enriched scene_data with comprehensive brain decisions
        """
        scene_text = ' '.join([d.get('text', '') for d in scene_data.get('dialogues', [])])
        scene_title = scene_data.get('title', '')
        dialogues = scene_data.get('dialogues', [])
        
        # === EMOTIONAL ANALYSIS ===
        emotion_analysis = self.analyze_scene_emotion(scene_text, scene_title)
        
        # === BASIC ANIMATION STYLE ===
        animation_style = self.decide_animation_style(
            emotion_analysis['emotion'],
            emotion_analysis['intensity']
        )
        
        # === CHARACTER ANALYSIS (with behavior detection) ===
        character_analyses = {}
        character_behaviors = {}
        for dialogue in dialogues:
            char_name = dialogue.get('character', 'Narrator')
            if char_name not in character_analyses:
                char_profile = self.analyze_character(
                    char_name,
                    dialogue.get('text', ''),
                    scene_text
                )
                character_analyses[char_name] = char_profile
                
                # Detect what this character is doing
                behavior = self.detect_character_behavior(dialogue.get('text', ''), scene_text)
                if behavior:
                    character_behaviors[char_name] = self.behavior_database.get(behavior, {})
                    character_behaviors[char_name]['action'] = behavior
        
        # === RHYTHM AND TIMING ANALYSIS ===
        dialogue_rhythm = self.analyze_dialogue_rhythm(dialogues)
        scene_timing = self.calculate_scene_timing(
            emotion_analysis['emotion'],
            emotion_analysis['intensity'],
            dialogue_rhythm
        )
        
        # === CAMERA MOVEMENT SUGGESTION ===
        # Use primary character's behavior (or first character)
        primary_behavior = None
        if character_behaviors:
            primary_behavior = list(character_behaviors.values())[0].get('action')
        
        camera_suggestion = self.suggest_camera_movement(
            emotion_analysis['emotion'],
            primary_behavior,
            emotion_analysis['intensity']
        )
        
        # === CROSS-SCENE LEARNING (if context available) ===
        context_learning = {}
        if all_scenes and scene_index > 0:
            context_learning = self.learn_from_previous_scenes(scene_index, all_scenes)
        
        # === ENRICH THE SCENE DATA ===
        enriched = scene_data.copy()
        enriched['brain_analysis'] = {
            'emotion': emotion_analysis,
            'animation': animation_style,
            'characters': character_analyses,
            'behaviors': character_behaviors,
            'rhythm': dialogue_rhythm,
            'timing': scene_timing,
            'camera': camera_suggestion,
            'context': context_learning,
            'creative_notes': self._generate_creative_notes(
                emotion_analysis,
                character_behaviors,
                dialogue_rhythm,
                context_learning
            )
        }
        
        return enriched
    
    def _generate_creative_notes(self, emotion_analysis: dict, behaviors: dict, 
                                  rhythm: dict, context: dict) -> List[str]:
        """Generate human-readable creative direction notes.
        
        These are suggestions for how to film/animate the scene.
        """
        notes = []
        
        # Emotion-based note
        emotion = emotion_analysis['emotion']
        intensity = emotion_analysis['intensity']
        if intensity > 0.8:
            notes.append(f"⚠️ HIGH INTENSITY {emotion.upper()} scene - maximize dramatic impact")
        elif intensity < 0.3:
            notes.append(f"Subtle {emotion} tone - use restraint in effects")
        else:
            notes.append(f"Moderate {emotion} emotion - balanced approach")
        
        # Behavior-based note
        if behaviors:
            actions = [b.get('action', 'unknown') for b in behaviors.values()]
            notes.append(f"Character actions: {', '.join(actions)} - match camera to movement")
        
        # Rhythm-based note
        pace = rhythm.get('pace', 'normal')
        pattern = rhythm.get('pattern', 'steady')
        notes.append(f"Dialogue rhythm: {pattern} pattern, {pace} pace - adjust cuts accordingly")
        
        # Context-based note
        if context.get('has_context'):
            transition = context.get('transition_type', 'unknown')
            notes.append(f"Narrative: {transition} from previous scene - {context.get('narrative_suggestion', '')}")
        
        return notes
    
    # ========== EXPORT FOR RENDERER ==========
    
    def export_decisions(self, output_path: Path):
        """Save brain decisions to JSON file."""
        decisions = {
            'character_profiles': self.character_profiles,
            'scene_emotions': self.scene_emotions,
        }
        output_path.write_text(json.dumps(decisions, indent=2, ensure_ascii=False))
        print(f"🧠 Brain decisions exported to: {output_path}")


# ========== STANDALONE TEST ==========
if __name__ == '__main__':
    brain = IntelligentBrain()
    
    # Test character analysis
    print("=== CHARACTER ANALYSIS ===")
    test_chars = [
        ('ਅਮਨਦੀਪ', 'ਉਹ ਇੱਕ ਜਵਾਨ ਲੜਕਾ ਸੀ।', 'He was a young boy.'),
        ('ਦਲਜੀਤ ਕੌਰ', 'ਉਹ ਬਹੁਤ ਗੁੱਸੇ ਵਿੱਚ ਸੀ।', 'She was very angry.'),
        ('ਕੁਲਵੰਤ (Narrator)', 'ਕਹਾਣੀ ਸ਼ੁਰੂ ਹੁੰਦੀ ਹੈ।', 'The story begins.'),
    ]
    
    for name, dialogue, context in test_chars:
        profile = brain.analyze_character(name, dialogue, context)
        print(f"\n{name}:")
        print(f"  Age: {profile['age_group']}, Gender: {profile['gender']}, Emotion: {profile['base_emotion']}")
        print(f"  Voice: Pitch={profile['voice_pitch']:.2f}, Speed={profile['voice_speed']:.2f}")
    
    # Test scene emotion analysis
    print("\n\n=== SCENE EMOTION ANALYSIS ===")
    test_scenes = [
        ('ਸ਼ੁਰੂਆਤ', 'ਅਮਨਦੀਪ ਇੱਕ ਖੁਸ਼ ਬੱਚਾ ਸੀ। ਉਹ ਹੱਸਦਾ ਰਹਿੰਦਾ ਸੀ।'),
        ('ਹਾਦਸਾ', 'ਅੱਗ ਲੱਗ ਗਈ। ਉਹ ਜਲ ਕੇ ਮਰ ਗਿਆ। ਬਹੁਤ ਦੁੱਖ ਦੀ ਗੱਲ ਹੈ।'),
        ('ਪੁਲਿਸ', 'ਪੁਲਿਸ ਨੇ ਧਮਕੀ ਦਿੱਤੀ। ਉਹ ਬਹੁਤ ਡਰ ਗਿਆ।'),
    ]
    
    for title, text in test_scenes:
        analysis = brain.analyze_scene_emotion(text, title)
        print(f"\n{title}:")
        print(f"  Emotion: {analysis['emotion']} (intensity: {analysis['intensity']:.2f})")
        print(f"  Music: {analysis['music_file']} @ {analysis['music_volume']:.2f}")
        style = brain.decide_animation_style(analysis['emotion'], analysis['intensity'])
        print(f"  Animation: {style['movement_type']}, zoom={style['zoom_speed']:.2f}, pan={style['pan_direction']}")
    
    # Test behavior detection
    print("\n\n=== BEHAVIOR DETECTION ===")
    test_behaviors = [
        ('ਉਹ ਰੋ ਰਿਹਾ ਸੀ।', 'crying'),
        ('ਪੁਲਿਸ ਨੇ ਧਮਕੀ ਦਿੱਤੀ।', 'shouting'),
        ('ਉਹ ਅਰਦਾਸ ਕਰ ਰਿਹਾ ਸੀ।', 'prayer'),
        ('ਖੇਤਾਂ ਵਿੱਚ ਕੰਮ ਕਰ ਰਿਹਾ ਸੀ।', 'farming'),
    ]
    
    for text, expected in test_behaviors:
        detected = brain.detect_character_behavior(text)
        print(f"{text}")
        print(f"  Detected: {detected} {'✓' if detected == expected else '✗'}")
        if detected:
            behavior_data = brain.behavior_database.get(detected, {})
            print(f"  Animation: {behavior_data.get('animation', 'N/A')}, Duration: {behavior_data.get('duration', 0):.1f}s")
    
    # Test rhythm analysis
    print("\n\n=== DIALOGUE RHYTHM ANALYSIS ===")
    test_dialogues = [
        {'text': 'ਸਲਾਮ।'},  # Very short
        {'text': 'ਕਿਵੇਂ ਹੋ ਤੁਸੀਂ?'},  # Short
        {'text': 'ਮੈਂ ਠੀਕ ਹਾਂ, ਪਰ ਦੁੱਖ ਹੈ।'},  # Medium
    ]
    rhythm = brain.analyze_dialogue_rhythm(test_dialogues)
    print(f"Pattern: {rhythm['pattern']}, Pace: {rhythm['pace']}")
    print(f"Average length: {rhythm['avg_length']:.1f} chars")
    print(f"Suggested pause: {rhythm['suggested_pause_duration']:.1f}s")
    
    # Test camera suggestions
    print("\n\n=== CAMERA MOVEMENT SUGGESTIONS ===")
    camera1 = brain.suggest_camera_movement('happy', 'laughing', 0.6)
    print("Happy scene with laughing:")
    print(f"  Type: {camera1['camera_type']}, Speed: {camera1['camera_speed']}")
    print(f"  Direction: {camera1['camera_direction']}, FOV: {camera1['suggested_fov']}°")
    
    camera2 = brain.suggest_camera_movement('tragic', 'crying', 0.9)
    print("\nTragic scene with crying:")
    print(f"  Type: {camera2['camera_type']}, Speed: {camera2['camera_speed']}")
    print(f"  Direction: {camera2['camera_direction']}, FOV: {camera2['suggested_fov']}°")
    
    # Test cross-scene learning
    print("\n\n=== CROSS-SCENE LEARNING ===")
    mock_scenes = [
        {'brain_analysis': {'emotion': {'emotion': 'happy'}}},
        {'brain_analysis': {'emotion': {'emotion': 'tragic'}}},
    ]
    learning = brain.learn_from_previous_scenes(1, mock_scenes)
    print(f"Transition: {learning['previous_emotion']} → {learning['current_emotion']}")
    print(f"Type: {learning['transition_type']} (shift distance: {learning['emotional_shift']:.2f})")
    print(f"Suggestion: {learning['narrative_suggestion']}")
    
    print("\n✅ Enhanced brain test complete!")
    print(f"📊 Brain memory: {len(brain.behavior_database)} behaviors, {len(brain.learning_memory)} learned patterns")
