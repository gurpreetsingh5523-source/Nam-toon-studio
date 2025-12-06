#!/usr/bin/env python3
"""
Brain Diagnostic Mode - Test each brain separately
ਹਰੇਕ ਬ੍ਰੇਨ ਨੂੰ ਵੱਖਰੇ ਤੌਰ 'ਤੇ ਟੈਸਟ ਕਰੋ

This script tests each of the 4 brains individually:
1. Audio Brain - Background music selection
2. Voice Brain - Dialogue/TTS generation
3. Visual Brain - Animation and effects
4. SFX Brain - Sound effects selection

Purpose: Find which brain is not understanding the logic properly
"""

import sys
import os
import json
from pathlib import Path
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger("brain_diagnostic")

class BrainDiagnostic:
    """ਹਰੇਕ ਬ੍ਰੇਨ ਨੂੰ ਵੱਖਰੇ ਤੌਰ 'ਤੇ ਟੈਸਟ ਕਰੋ"""
    
    def __init__(self, scenes_file):
        self.scenes_file = scenes_file
        self.scenes = []
        self.results = {
            "audio_brain": [],
            "voice_brain": [],
            "visual_brain": [],
            "sfx_brain": []
        }
        
    def load_scenes(self):
        """Load scenes from JSON"""
        with open(self.scenes_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.scenes = data.get('scenes', [])
        log.info(f"✓ Loaded {len(self.scenes)} scenes\n")
    
    def test_audio_brain(self):
        """Test Audio Brain - Music Selection
        ਆਡੀਓ ਬ੍ਰੇਨ ਟੈਸਟ - ਸੰਗੀਤ ਚੋਣ
        """
        log.info("=" * 60)
        log.info("🎵 TESTING AUDIO BRAIN (Music Selection)")
        log.info("=" * 60)
        
        try:
            from colab.master_orchestrator_brain import MasterOrchestratorBrain
            master = MasterOrchestratorBrain()
            
            for scene in self.scenes:
                scene_id = scene.get('scene_id', 0)
                emotion = scene.get('emotion', 'neutral')
                
                # Ask Audio Brain to select music
                result = master.audio_brain.select_background_music(
                    emotion=emotion,
                    scene_duration=10.0,
                    intensity=0.5
                )
                
                self.results["audio_brain"].append({
                    "scene_id": scene_id,
                    "emotion": emotion,
                    "selected_music": result.get('music_path', 'none'),
                    "category": result.get('category', 'unknown'),
                    "reasoning": result.get('reasoning', 'no reasoning')
                })
                
                log.info(f"\nScene {scene_id} (Emotion: {emotion}):")
                log.info(f"  Selected: {result.get('music_path', 'none')}")
                log.info(f"  Category: {result.get('category', 'unknown')}")
                log.info(f"  Reason: {result.get('reasoning', 'no reasoning')}")
            
            log.info(f"\n✅ Audio Brain Test Complete")
            return True
            
        except Exception as e:
            log.error(f"❌ Audio Brain Failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_voice_brain(self):
        """Test Voice Brain - TTS and Voice Profiles
        ਵੌਇਸ ਬ੍ਰੇਨ ਟੈਸਟ - TTS ਅਤੇ ਆਵਾਜ਼
        """
        log.info("\n" + "=" * 60)
        log.info("🎤 TESTING VOICE BRAIN (TTS & Voice Profiles)")
        log.info("=" * 60)
        
        try:
            from colab.master_orchestrator_brain import MasterOrchestratorBrain
            master = MasterOrchestratorBrain()
            
            for scene in self.scenes:
                scene_id = scene.get('scene_id', 0)
                dialogues = scene.get('dialogues', [])
                
                if not dialogues:
                    continue
                
                log.info(f"\nScene {scene_id}:")
                
                for idx, dialogue in enumerate(dialogues):
                    character = dialogue.get('character', 'Unknown')
                    text = dialogue.get('text', '')[:50] + '...'
                    
                    # Ask Voice Brain for voice profile
                    voice_profile = master.voice_music_brain.suggest_voice_profile(
                        character=character,
                        emotion=scene.get('emotion', 'neutral'),
                        age="adult"
                    )
                    
                    self.results["voice_brain"].append({
                        "scene_id": scene_id,
                        "character": character,
                        "voice_profile": voice_profile,
                        "text_sample": text
                    })
                    
                    log.info(f"  Dialogue {idx}: {character}")
                    log.info(f"    Voice: pitch={voice_profile.get('pitch', 1.0)}, "
                           f"speed={voice_profile.get('speed', 1.0)}")
            
            log.info(f"\n✅ Voice Brain Test Complete")
            return True
            
        except Exception as e:
            log.error(f"❌ Voice Brain Failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_visual_brain(self):
        """Test Visual Brain - Animation & Camera
        ਵਿਜ਼ੂਅਲ ਬ੍ਰੇਨ ਟੈਸਟ - ਐਨੀਮੇਸ਼ਨ ਅਤੇ ਕੈਮਰਾ
        """
        log.info("\n" + "=" * 60)
        log.info("🎨 TESTING VISUAL BRAIN (Animation & Camera)")
        log.info("=" * 60)
        
        try:
            from colab.master_orchestrator_brain import MasterOrchestratorBrain
            master = MasterOrchestratorBrain()
            
            for scene in self.scenes:
                scene_id = scene.get('scene_id', 0)
                emotion = scene.get('emotion', 'neutral')
                characters = scene.get('characters', [])
                
                # Ask Visual Brain for animation plan
                visual_plan = master.visual_brain.suggest_scene_visual(
                    emotion=emotion,
                    characters=characters,
                    location=scene.get('location', 'unknown')
                )
                
                self.results["visual_brain"].append({
                    "scene_id": scene_id,
                    "emotion": emotion,
                    "camera_angle": visual_plan.get('camera_angle', 'static'),
                    "animation_style": visual_plan.get('animation_style', 'none'),
                    "color_scheme": visual_plan.get('color_scheme', 'default'),
                    "transitions": visual_plan.get('transitions', [])
                })
                
                log.info(f"\nScene {scene_id} (Emotion: {emotion}):")
                log.info(f"  Camera: {visual_plan.get('camera_angle', 'static')}")
                log.info(f"  Animation: {visual_plan.get('animation_style', 'none')}")
                log.info(f"  Colors: {visual_plan.get('color_scheme', 'default')}")
                log.info(f"  Characters: {len(characters)}")
            
            log.info(f"\n✅ Visual Brain Test Complete")
            return True
            
        except Exception as e:
            log.error(f"❌ Visual Brain Failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_sfx_brain(self):
        """Test SFX Brain - Sound Effects Selection
        SFX ਬ੍ਰੇਨ ਟੈਸਟ - ਆਵਾਜ਼ ਪ੍ਰਭਾਵ
        """
        log.info("\n" + "=" * 60)
        log.info("🔊 TESTING SFX BRAIN (Sound Effects)")
        log.info("=" * 60)
        
        try:
            from colab.master_orchestrator_brain import MasterOrchestratorBrain
            master = MasterOrchestratorBrain()
            
            for scene in self.scenes:
                scene_id = scene.get('scene_id', 0)
                emotion = scene.get('emotion', 'neutral')
                location = scene.get('location', 'unknown')
                
                # Ask SFX Brain for sound effects
                sfx_plan = master.audio_brain.suggest_scene_sfx(
                    emotion=emotion,
                    location=location,
                    actions=[]
                )
                
                self.results["sfx_brain"].append({
                    "scene_id": scene_id,
                    "emotion": emotion,
                    "location": location,
                    "ambient_sfx": sfx_plan.get('ambient', []),
                    "action_sfx": sfx_plan.get('actions', [])
                })
                
                log.info(f"\nScene {scene_id}:")
                log.info(f"  Location: {location}")
                log.info(f"  Ambient SFX: {sfx_plan.get('ambient', [])}")
                log.info(f"  Action SFX: {sfx_plan.get('actions', [])}")
            
            log.info(f"\n✅ SFX Brain Test Complete")
            return True
            
        except Exception as e:
            log.error(f"❌ SFX Brain Failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_report(self):
        """Generate diagnostic report
        ਡਾਇਗਨੋਸਟਿਕ ਰਿਪੋਰਟ ਬਣਾਓ
        """
        log.info("\n" + "=" * 60)
        log.info("📊 BRAIN DIAGNOSTIC REPORT")
        log.info("=" * 60)
        
        report = {
            "timestamp": "2025-11-03",
            "scenes_tested": len(self.scenes),
            "results": self.results,
            "summary": {
                "audio_brain": {
                    "tested_scenes": len(self.results["audio_brain"]),
                    "status": "✓" if self.results["audio_brain"] else "❌"
                },
                "voice_brain": {
                    "tested_scenes": len(self.results["voice_brain"]),
                    "status": "✓" if self.results["voice_brain"] else "❌"
                },
                "visual_brain": {
                    "tested_scenes": len(self.results["visual_brain"]),
                    "status": "✓" if self.results["visual_brain"] else "❌"
                },
                "sfx_brain": {
                    "tested_scenes": len(self.results["sfx_brain"]),
                    "status": "✓" if self.results["sfx_brain"] else "❌"
                }
            }
        }
        
        # Save report
        report_file = "brain_memory/brain_diagnostic_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        log.info(f"\n✓ Report saved: {report_file}")
        
        # Print summary
        log.info("\n📋 SUMMARY:")
        for brain, data in report["summary"].items():
            log.info(f"  {brain}: {data['status']} ({data['tested_scenes']} scenes)")
        
        return report

def main():
    """Main diagnostic runner"""
    log.info("🧠 Starting Brain Diagnostic Test\n")
    
    # Use existing scenes file
    scenes_file = "temp_adhhi_aurat_scenes.json"
    
    if not os.path.exists(scenes_file):
        log.error(f"❌ Scenes file not found: {scenes_file}")
        return
    
    diagnostic = BrainDiagnostic(scenes_file)
    diagnostic.load_scenes()
    
    # Test each brain separately
    results = {
        "audio": diagnostic.test_audio_brain(),
        "voice": diagnostic.test_voice_brain(),
        "visual": diagnostic.test_visual_brain(),
        "sfx": diagnostic.test_sfx_brain()
    }
    
    # Generate report
    report = diagnostic.generate_report()
    
    # Final summary
    log.info("\n" + "=" * 60)
    log.info("🎯 DIAGNOSTIC COMPLETE")
    log.info("=" * 60)
    
    # TODO: Implement functioned = sum(1 for v in results.values() if v)
    total = len(results)
    
    log.info(f"\nBrains Passed: {# TODO: Implement functioned}/{total}")
    
    if # TODO: Implement functioned == total:
        log.info("✅ All brains working correctly!")
    else:
        log.info("⚠️  Some brains need training:")
        for brain, # TODO: Implement functioned in results.items():
            if not # TODO: Implement functioned:
                log.info(f"  ❌ {brain.upper()} Brain needs attention")
    
    log.info(f"\n📄 Full report: brain_memory/brain_diagnostic_report.json")

if __name__ == "__main__":
    main()
