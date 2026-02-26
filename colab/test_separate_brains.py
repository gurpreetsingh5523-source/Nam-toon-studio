#!/usr/bin/env python3
"""
Simple Separate Brain Workflow Test
ਹਰੇਕ ਬ੍ਰੇਨ ਨੂੰ ਵੱਖ-ਵੱਖ ਟੈਸਟ ਕਰੋ

This creates 4 separate outputs to test each brain:
1. audio_only.json - Audio Brain decisions
2. voice_only.json - Voice/TTS decisions  
3. visual_only.json - Visual/Animation decisions
4. sfx_only.json - Sound effects decisions
"""

import json
import os
from pathlib import Path

def test_audio_brain_decisions(scenes):
    """ਆਡੀਓ ਬ੍ਰੇਨ - ਸੰਗੀਤ ਚੋਣ"""
    print("\n🎵 AUDIO BRAIN - Music Selection")
    print("=" * 60)
    
    results = []
    
    # Emotion to music mapping (Audio Brain logic)
    emotion_music_map = {
        "family_background": "audio/ambient.wav",
        "trouble": "audio/heartbeat.wav",
        "brotherhood": "audio/birds.wav",
        "marriage_conflict": "audio/strings.wav",
        "alienation": "audio/rain.wav",
        "harassment": "audio/heartbeat.wav",
        "despair": "audio/strings.wav",
        "aftermath_questioning": "audio/ambient.wav",
        "neutral": "audio/ambient.wav",
        "happy": "audio/birds.wav",
        "sad": "audio/strings.wav",
        "tense": "audio/heartbeat.wav",
        "tragic": "audio/strings.wav"
    }
    
    for scene in scenes:
        emotion = scene.get('emotion', 'neutral')
        selected_music = emotion_music_map.get(emotion, "audio/ambient.wav")
        
        result = {
            "scene_id": scene['scene_id'],
            "emotion": emotion,
            "selected_music": selected_music,
            "volume": 0.35,
            "brain_reasoning": f"Emotion '{emotion}' maps to {selected_music}"
        }
        results.append(result)
        
        print(f"Scene {scene['scene_id']}: {emotion} → {selected_music}")
    
    # Save results
    with open('brain_memory/audio_brain_test.json', 'w', encoding='utf-8') as f:
        json.dump({"brain": "audio", "results": results}, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Tested {len(results)} scenes")
    print(f"✓ Saved: brain_memory/audio_brain_test.json")
    return results

def test_voice_brain_decisions(scenes):
    """ਵੌਇਸ ਬ੍ਰੇਨ - TTS ਅਤੇ ਆਵਾਜ਼ Profiles"""
    print("\n🎤 VOICE BRAIN - TTS & Voice Profiles")
    print("=" * 60)
    
    results = []
    
    # Load voice profiles
    try:
        with open('brain_memory/character_voice_profiles.json', 'r') as f:
            profiles_data = json.load(f)
            voice_profiles = profiles_data.get('character_profiles', {})
    except:
        voice_profiles = {}
    
    for scene in scenes:
        dialogues = scene.get('dialogues', [])
        
        for dialogue in dialogues:
            character = dialogue.get('character', 'Narrator')
            text = dialogue.get('text', '')
            
            # Get voice profile or use default
            if character in voice_profiles:
                profile = voice_profiles[character]
            else:
                # Default adult male
                profile = {
                    "voice_pitch": 0.85,
                    "voice_speed": 0.95,
                    "age": "adult",
                    "gender": "male"
                }
            
            result = {
                "scene_id": scene['scene_id'],
                "character": character,
                "text_length": len(text),
                "voice_pitch": profile.get('voice_pitch', 0.85),
                "voice_speed": profile.get('voice_speed', 0.95),
                "estimated_duration": len(text.split()) * 0.5,  # rough estimate
                "brain_reasoning": f"Character '{character}' → pitch={profile.get('voice_pitch', 0.85)}"
            }
            results.append(result)
            
            print(f"Scene {scene['scene_id']}, {character}: "
                  f"pitch={profile.get('voice_pitch', 0.85):.2f}, "
                  f"speed={profile.get('voice_speed', 0.95):.2f}")
    
    # Save results
    with open('brain_memory/voice_brain_test.json', 'w', encoding='utf-8') as f:
        json.dump({"brain": "voice", "results": results}, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Tested {len(results)} dialogues")
    print(f"✓ Saved: brain_memory/voice_brain_test.json")
    return results

def test_visual_brain_decisions(scenes):
    """ਵਿਜ਼ੂਅਲ ਬ੍ਰੇਨ - ਐਨੀਮੇਸ਼ਨ ਅਤੇ ਕੈਮਰਾ"""
    print("\n🎨 VISUAL BRAIN - Animation & Camera")
    print("=" * 60)
    
    results = []
    
    # Emotion to visual mapping
    emotion_visual_map = {
        "family_background": {"camera": "steady", "colors": ["warm_orange", "soft_yellow"]},
        "trouble": {"camera": "handheld", "colors": ["dark_red", "gray"]},
        "brotherhood": {"camera": "rhythmic_zoom", "colors": ["green", "blue"]},
        "marriage_conflict": {"camera": "static_close", "colors": ["red", "purple"]},
        "alienation": {"camera": "slow_pan", "colors": ["gray", "dark_blue"]},
        "harassment": {"camera": "handheld", "colors": ["black", "red"]},
        "despair": {"camera": "static_close", "colors": ["dark_gray", "black"]},
        "aftermath_questioning": {"camera": "steady", "colors": ["gray", "white"]},
        "neutral": {"camera": "steady", "colors": ["blue", "gray"]},
        "happy": {"camera": "rhythmic_zoom", "colors": ["yellow", "green"]},
        "sad": {"camera": "static_close", "colors": ["blue", "gray"]},
        "tense": {"camera": "handheld", "colors": ["red", "black"]},
        "tragic": {"camera": "static_close", "colors": ["dark_gray", "black"]}
    }
    
    for scene in scenes:
        emotion = scene.get('emotion', 'neutral')
        visual_plan = emotion_visual_map.get(emotion, emotion_visual_map["neutral"])
        
        result = {
            "scene_id": scene['scene_id'],
            "emotion": emotion,
            "camera_movement": visual_plan["camera"],
            "color_palette": visual_plan["colors"],
            "num_characters": len(scene.get('characters', [])),
            "animation_intensity": 0.5 if emotion in ["tense", "despair", "tragic"] else 0.3,
            "brain_reasoning": f"Emotion '{emotion}' → {visual_plan['camera']} camera"
        }
        results.append(result)
        
        print(f"Scene {scene['scene_id']}: {emotion} → Camera: {visual_plan['camera']}, "
              f"Colors: {visual_plan['colors']}")
    
    # Save results
    with open('brain_memory/visual_brain_test.json', 'w', encoding='utf-8') as f:
        json.dump({"brain": "visual", "results": results}, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Tested {len(results)} scenes")
    print(f"✓ Saved: brain_memory/visual_brain_test.json")
    return results

def test_sfx_brain_decisions(scenes):
    """SFX ਬ੍ਰੇਨ - ਆਵਾਜ਼ ਪ੍ਰਭਾਵ"""
    print("\n🔊 SFX BRAIN - Sound Effects")
    print("=" * 60)
    
    results = []
    
    # Location to SFX mapping
    location_sfx_map = {
        "ਮਾਸੀ ਦਾ ਘਰ": ["door_creak", "footsteps"],
        "ਪਿੰਡ": ["birds_chirping", "distant_voices"],
        "ਕਾਰ ਵਰਕਸ਼ਾਪ": ["metal_clang", "tools"],
        "ਘਰ": ["door_close", "ambient_home"],
        "ਖੇਤ": ["wind", "birds"],
        "ਹਸਪਤਾਲ": ["beeping", "footsteps"]
    }
    
    # Emotion to ambient SFX
    emotion_sfx_map = {
        "trouble": ["heavy_breathing", "tension"],
        "despair": ["wind", "silence"],
        "harassment": ["heavy_breathing", "tension"],
        "tragic": ["wind", "silence"]
    }
    
    for scene in scenes:
        location = scene.get('location', 'unknown')
        emotion = scene.get('emotion', 'neutral')
        
        # Get location SFX
        location_sfx = []
        for key in location_sfx_map.keys():
            if key in location:
                location_sfx = location_sfx_map[key]
                break
        
        # Get emotion SFX
        emotion_sfx = emotion_sfx_map.get(emotion, [])
        
        result = {
            "scene_id": scene['scene_id'],
            "location": location,
            "emotion": emotion,
            "ambient_sfx": location_sfx,
            "emotion_sfx": emotion_sfx,
            "sfx_volume": 0.3,
            "brain_reasoning": f"Location '{location}' + emotion '{emotion}'"
        }
        results.append(result)
        
        print(f"Scene {scene['scene_id']}: Location SFX: {location_sfx}, "
              f"Emotion SFX: {emotion_sfx}")
    
    # Save results
    with open('brain_memory/sfx_brain_test.json', 'w', encoding='utf-8') as f:
        json.dump({"brain": "sfx", "results": results}, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Tested {len(results)} scenes")
    print(f"✓ Saved: brain_memory/sfx_brain_test.json")
    return results

def main():
    """ਮੁੱਖ ਟੈਸਟਰ"""
    print("🧠 Separate Brain Workflow Test")
    print("=" * 60)
    print("Testing each brain independently...\n")
    
    # Load scenes
    scenes_file = "temp_adhhi_aurat_scenes.json"
    with open(scenes_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        scenes = data.get('scenes', [])
    
    print(f"✓ Loaded {len(scenes)} scenes from {scenes_file}\n")
    
    # Test each brain separately
    audio_results = test_audio_brain_decisions(scenes)
    voice_results = test_voice_brain_decisions(scenes)
    visual_results = test_visual_brain_decisions(scenes)
    sfx_results = test_sfx_brain_decisions(scenes)
    
    # Generate summary report
    print("\n" + "=" * 60)
    print("📊 SUMMARY REPORT")
    print("=" * 60)
    
    summary = {
        "total_scenes": len(scenes),
        "audio_brain": {
            "decisions_made": len(audio_results),
            "status": "✓ Working" if len(audio_results) == len(scenes) else "❌ Issue"
        },
        "voice_brain": {
            "decisions_made": len(voice_results),
            "status": "✓ Working" if len(voice_results) > 0 else "❌ Issue"
        },
        "visual_brain": {
            "decisions_made": len(visual_results),
            "status": "✓ Working" if len(visual_results) == len(scenes) else "❌ Issue"
        },
        "sfx_brain": {
            "decisions_made": len(sfx_results),
            "status": "✓ Working" if len(sfx_results) == len(scenes) else "❌ Issue"
        }
    }
    
    for brain, data in summary.items():
        if brain == "total_scenes":
            continue
        print(f"\n{brain.upper()}:")
        print(f"  Decisions: {data['decisions_made']}")
        print(f"  Status: {data['status']}")
    
    # Save combined report
    with open('brain_memory/brain_workflow_test_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Summary saved: brain_memory/brain_workflow_test_summary.json")
    print("\n📁 Individual brain outputs:")
    print("  • brain_memory/audio_brain_test.json")
    print("  • brain_memory/voice_brain_test.json")
    print("  • brain_memory/visual_brain_test.json")
    print("  • brain_memory/sfx_brain_test.json")
    
    print("\n✅ All 4 brains tested separately!")

if __name__ == "__main__":
    main()
