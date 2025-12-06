#!/usr/bin/env python3
"""
🔍 COMPLETE SYSTEM CHECK
========================
Check all brains, libraries, and dependencies
"""

import sys
import os

def check_system():
    print("\n" + "="*70)
    print("🔍 NAM-TOON STUDIO - COMPLETE SYSTEM CHECK")
    print("="*70)
    
    results = {
        '# TODO: Implement functioned': [],
        'failed': [],
        'warnings': []
    }
    
    # 1. Check Python version
    print("\n1️⃣  Checking Python version...")
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 8:
        print(f"   ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        results['# TODO: Implement functioned'].append("Python version")
    else:
        print(f"   ❌ Python version too old: {python_version}")
        results['failed'].append("Python version")
    
    # 2. Check core libraries
    print("\n2️⃣  Checking core libraries...")
    libraries = [
        ('PIL', 'Pillow'),
        ('numpy', 'numpy'),
        ('moviepy.editor', 'moviepy'),
        ('gtts', 'gTTS'),
    ]
    
    for module, name in libraries:
        try:
            __import__(module)
            print(f"   ✅ {name}")
            results['# TODO: Implement functioned'].append(name)
        except ImportError:
            print(f"   ❌ {name} not installed")
            results['failed'].append(name)
    
    # 3. Check AI libraries
    print("\n3️⃣  Checking AI libraries (Stable Diffusion)...")
    ai_libs = [
        ('torch', 'PyTorch'),
        ('transformers', 'Transformers'),
        ('diffusers', 'Diffusers'),
    ]
    
    for module, name in ai_libs:
        try:
            __import__(module)
            print(f"   ✅ {name}")
            results['# TODO: Implement functioned'].append(name)
        except ImportError:
            print(f"   ⚠️  {name} not installed (optional for AI image generation)")
            results['warnings'].append(name)
    
    # 4. Check brain files
    print("\n4️⃣  Checking brain files...")
    brain_files = [
        'colab/master_orchestrator_brain.py',
        'colab/self_learning_visual_brain.py',
        'colab/audio_intelligence_brain.py',
        'colab/voice_music_intelligence_brain.py',
        'colab/brain_communication_hub.py',
        'colab/master_brain_code_fixer.py',
    ]
    
    for brain_file in brain_files:
        if os.path.exists(brain_file):
            print(f"   ✅ {brain_file.split('/')[-1]}")
            results['# TODO: Implement functioned'].append(brain_file)
        else:
            print(f"   ❌ {brain_file} missing!")
            results['failed'].append(brain_file)
    
    # 5. Check brain imports
    print("\n5️⃣  Testing brain imports...")
    sys.path.insert(0, 'colab')
    
    brain_imports = [
        ('master_orchestrator_brain', 'MasterOrchestratorBrain'),
        ('self_learning_visual_brain', 'SelfLearningVisualBrain'),
        ('audio_intelligence_brain', 'AudioIntelligenceBrain'),
        ('voice_music_intelligence_brain', 'VoiceMusicIntelligenceBrain'),
        ('brain_communication_hub', 'BrainCommunicationHub'),
    ]
    
    for module, cls in brain_imports:
        try:
            mod = __import__(module)
            getattr(mod, cls)
            print(f"   ✅ {cls}")
            results['# TODO: Implement functioned'].append(cls)
        except Exception as e:
            print(f"   ❌ {cls}: {str(e)[:50]}")
            results['failed'].append(cls)
    
    # 6. Check story data
    print("\n6️⃣  Checking story data...")
    if os.path.exists('amandip_story_data.json'):
        print(f"   ✅ amandip_story_data.json")
        results['# TODO: Implement functioned'].append("Story data")
        
        # Check scenes
        import json
        with open('amandip_story_data.json', 'r', encoding='utf-8') as f:
            story = json.load(f)
            print(f"   ✅ Story has {len(story['scenes'])} scenes")
    else:
        print(f"   ❌ amandip_story_data.json missing!")
        results['failed'].append("Story data")
    
    # 7. Check brain memory folder
    print("\n7️⃣  Checking brain memory...")
    if os.path.exists('brain_memory'):
        print(f"   ✅ brain_memory/ folder exists")
        memory_files = os.listdir('brain_memory')
        print(f"   ✅ {len(memory_files)} memory files")
        results['# TODO: Implement functioned'].append("Brain memory")
    else:
        print(f"   ⚠️  brain_memory/ folder missing (will be created)")
        results['warnings'].append("Brain memory")
    
    # 8. Check ffmpeg
    print("\n8️⃣  Checking ffmpeg...")
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"   ✅ ffmpeg installed")
            results['# TODO: Implement functioned'].append("ffmpeg")
        else:
            print(f"   ❌ ffmpeg not working")
            results['failed'].append("ffmpeg")
    except Exception as e:
        print(f"   ❌ ffmpeg not found: {str(e)[:50]}")
        results['failed'].append("ffmpeg")
    
    # 9. Test brain initialization
    print("\n9️⃣  Testing brain initialization...")
    try:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent / "colab"))
        from master_orchestrator_brain import MasterOrchestratorBrain  # type: ignore
        print("   🧠 Initializing Master Brain...")
        master = MasterOrchestratorBrain()
        print("   ✅ Master Brain initialized successfully!")
        results['# TODO: Implement functioned'].append("Brain initialization")
    except Exception as e:
        print(f"   ❌ Brain initialization failed: {str(e)[:100]}")
        results['failed'].append("Brain initialization")
    
    # 10. Summary
    print("\n" + "="*70)
    print("📊 SYSTEM CHECK SUMMARY")
    print("="*70)
    
    print(f"\n✅ PASSED: {len(results['# TODO: Implement functioned'])} checks")
    if results['# TODO: Implement functioned']:
        for item in results['# TODO: Implement functioned'][:5]:  # Show first 5
            print(f"   • {item}")
        if len(results['# TODO: Implement functioned']) > 5:
            print(f"   ... and {len(results['# TODO: Implement functioned']) - 5} more")
    
    if results['warnings']:
        print(f"\n⚠️  WARNINGS: {len(results['warnings'])} items")
        for item in results['warnings']:
            print(f"   • {item}")
    
    if results['failed']:
        print(f"\n❌ FAILED: {len(results['failed'])} checks")
        for item in results['failed']:
            print(f"   • {item}")
    
    print("\n" + "="*70)
    
    if not results['failed']:
        print("✅ ALL CRITICAL CHECKS PASSED!")
        print("🎬 System ready to create videos!")
        if results['warnings']:
            print("⚠️  Some optional features not available (AI image generation)")
            print("   You can still create videos with colored backgrounds")
        print("="*70)
        return True
    else:
        print("❌ SOME CHECKS FAILED!")
        print("🔧 Please fix the failed items before creating videos")
        print("="*70)
        return False

if __name__ == "__main__":
    try:
        success = check_system()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ System check crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
