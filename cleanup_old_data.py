#!/usr/bin/env python3
"""
🧹 CLEANUP OLD DATA & VIDEOS 🧹
===============================

This script will:
1. Delete old test/unwanted video files
2. Reset brain memory (learned data) to start fresh
3. Remove temporary files
4. Keep ONLY:
   - All code files (.py)
   - Documentation files (.md)
   - Training data (media_training_data.json)
   - Latest final videos (Amandip_Full_Story.mp4, Communication_Test.mp4)

ਪੁਰਾਣਾ ਡੇਟਾ ਸਾਫ਼ ਕਰੋ, ਨਵਾਂ ਸ਼ੁਰੂ ਕਰੋ!
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    🧹 CLEANUP OLD DATA & VIDEOS 🧹                   ║
║                                                                      ║
║   This will DELETE:                                                  ║
║   ❌ Old test videos                                                ║
║   ❌ Temporary video files                                          ║
║   ❌ Brain learned memory (to start fresh)                          ║
║   ❌ Old story test files                                           ║
║                                                                      ║
║   This will KEEP:                                                    ║
║   ✅ All Python code files                                          ║
║   ✅ All documentation (.md files)                                  ║
║   ✅ Training data (media_training_data.json)                       ║
║   ✅ Final videos (Amandip_Full_Story.mp4, Communication_Test.mp4)  ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")

# Videos to KEEP (final versions)
KEEP_VIDEOS = [
    "Amandip_Full_Story.mp4",
    "Communication_Test.mp4"
]

# Videos to DELETE (old tests, temp files)
DELETE_VIDEO_PATTERNS = [
    "Aman_Story_Demo.mp4",
    "Aman_Story_Full.mp4",
    "Aman_Story_Full_CAPTIONS.mp4",
    "Aman_Story_Full_FIXED.mp4",
    "Aman_Story_Full_LEARN.mp4",
    "Aman_Story_Full_TTS_CAPTIONS.mp4",
    "Aman_Story_Say_Demo.mp4",
    "Amandip_Quick_Test.mp4",
    "Brain_Test_2Scenes.mp4",
    "Brain_Test_2ScenesTEMP_MPY_wvf_snd.mp4",
    "Brain_Test_NoCaption.mp4",
    "CreativeBrain_3Scenes.mp4",
    "CreativeBrain_3ScenesTEMP_MPY_wvf_snd.mp4",
    "Creative_Full.mp4",
    "Creative_FullTEMP_MPY_wvf_snd.mp4",
    "Diagnostic_10s.mp4",
    "Quick_Test.mp4",
    "TTS_3Scenes_Fast.mp4",
    "TTS_3Scenes_FastTEMP_MPY_wvf_snd.mp4",
    "TTS_Sample_Scene1.mp4",
    "TTS_Sample_Scene1TEMP_MPY_wvf_snd.mp4",
    "Visual_Sample.mp4",
    "Visual_SampleTEMP_MPY_wvf_snd.mp4",
    "Visual_Test.mp4",
    "Visual_Test_30s.mp4",
    "Visual_Test_30sTEMP_MPY_wvf_snd.mp4",
    "debug_clip_50s.mp4",
    "test_200s.mp4",
    "test_animation.mp4"
]

def cleanup_videos():
    """Delete old test videos, keep only final ones"""
    print("\n" + "="*70)
    print("🎬 CLEANING UP OLD VIDEOS")
    print("="*70)
    
    deleted_count = 0
    kept_count = 0
    freed_space = 0
    
    for video_file in DELETE_VIDEO_PATTERNS:
        if os.path.exists(video_file):
            file_size = os.path.getsize(video_file)
            freed_space += file_size
            os.remove(video_file)
            print(f"   ❌ Deleted: {video_file} ({file_size / 1024 / 1024:.1f} MB)")
            deleted_count += 1
    
    print(f"\n📊 Video Cleanup Results:")
    print(f"   ❌ Deleted: {deleted_count} old videos")
    print(f"   💾 Space Freed: {freed_space / 1024 / 1024:.1f} MB")
    
    print(f"\n✅ Videos KEPT:")
    for keep_video in KEEP_VIDEOS:
        if os.path.exists(keep_video):
            file_size = os.path.getsize(keep_video)
            print(f"   ✅ {keep_video} ({file_size / 1024 / 1024:.1f} MB)")
            kept_count += 1
    
    print(f"\n   Total Kept: {kept_count} final videos")

def reset_brain_memory():
    """Reset brain memory to start fresh learning"""
    print("\n" + "="*70)
    print("🧠 RESETTING BRAIN MEMORY")
    print("="*70)
    
    brain_memory_dir = Path("brain_memory")
    
    if brain_memory_dir.exists():
        # Create backup first
        backup_dir = Path(f"brain_memory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        shutil.copytree(brain_memory_dir, backup_dir)
        print(f"   💾 Backup created: {backup_dir}")
        
        # Clear brain memory files
        memory_files = [
            "audio_intelligence.json",
            "behavior_understanding.json",
            "brain_performance.json",
            "color_intelligence.json",
            "emotion_detection.json",
            "learning_mistakes.json",
            "master_validation.json",
            "voice_music_learning.json"
        ]
        
        reset_count = 0
        for memory_file in memory_files:
            file_path = brain_memory_dir / memory_file
            if file_path.exists():
                # Reset to empty but valid JSON
                with open(file_path, 'w', encoding='utf-8') as f:
                    if 'intelligence' in memory_file or 'understanding' in memory_file:
                        f.write('{}')
                    elif 'performance' in memory_file:
                        f.write('{"VISUAL_BRAIN": {}, "AUDIO_BRAIN": {}, "VOICE_MUSIC_BRAIN": {}, "CREATIVE_BRAIN": {}}')
                    else:
                        f.write('{}')
                print(f"   🔄 Reset: {memory_file}")
                reset_count += 1
        
        print(f"\n📊 Memory Reset Results:")
        print(f"   🔄 Reset: {reset_count} brain memory files")
        print(f"   💾 Backup: {backup_dir}")
        print(f"   ✅ Brains ready to learn from scratch!")

def cleanup_temp_files():
    """Remove temporary files"""
    print("\n" + "="*70)
    print("🗑️  CLEANING UP TEMP FILES")
    print("="*70)
    
    temp_patterns = [
        "scene_*.png",
        "scene_*.mp3",
        "temp-audio.m4a",
        "*TEMP_MPY*.mp4"
    ]
    
    deleted_count = 0
    
    import glob
    for pattern in temp_patterns:
        for temp_file in glob.glob(pattern):
            try:
                os.remove(temp_file)
                print(f"   ❌ Deleted: {temp_file}")
                deleted_count += 1
            except Exception as e:
                print(f"   ⚠️  Could not delete {temp_file}: {e}")
    
    print(f"\n📊 Temp Files Cleanup:")
    print(f"   ❌ Deleted: {deleted_count} temporary files")

def show_kept_files():
    """Show what important files we're keeping"""
    print("\n" + "="*70)
    print("✅ IMPORTANT FILES KEPT")
    print("="*70)
    
    keep_categories = {
        "Code Files": [
            "colab/master_orchestrator_brain.py",
            "colab/self_learning_visual_brain.py",
            "colab/audio_intelligence_brain.py",
            "colab/voice_music_intelligence_brain.py",
            "colab/brain_communication_hub.py",
            "colab/master_brain_code_fixer.py",
            "quick_render_amandip.py",
            "render_full_amandip.py"
        ],
        "Documentation": [
            "README.md",
            "BRAIN_COMMUNICATION.md",
            "MASTER_BRAIN_POWERS.md",
            "MASTER_BRAIN_LOGIC_MASTERY.md",
            "PUNJABI_AI_BRAIN.md"
        ],
        "Training Data": [
            "media_training_data.json",
            "amandip_story_data.json"
        ],
        "Final Videos": KEEP_VIDEOS
    }
    
    for category, files in keep_categories.items():
        print(f"\n{category}:")
        for file in files:
            if os.path.exists(file):
                file_size = os.path.getsize(file)
                if file_size > 1024 * 1024:
                    size_str = f"{file_size / 1024 / 1024:.1f} MB"
                elif file_size > 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size} bytes"
                print(f"   ✅ {file} ({size_str})")

def main():
    """Main cleanup process"""
    
    # Ask for confirmation
    print("\n⚠️  WARNING: This will delete old videos and reset brain memory!")
    print("   A backup of brain memory will be created.")
    response = input("\nProceed with cleanup? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\n❌ Cleanup cancelled.")
        return
    
    print("\n🚀 Starting cleanup process...")
    
    # 1. Cleanup old videos
    cleanup_videos()
    
    # 2. Reset brain memory
    reset_brain_memory()
    
    # 3. Cleanup temp files
    cleanup_temp_files()
    
    # 4. Show what we kept
    show_kept_files()
    
    print("\n" + "="*70)
    print("✅ CLEANUP COMPLETE!")
    print("="*70)
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                      ✨ CLEANUP SUCCESSFUL! ✨                       ║
║                                                                      ║
║   Your Nam-toon Studio is now clean and ready for fresh start!      ║
║                                                                      ║
║   ✅ Old test videos deleted                                        ║
║   ✅ Brain memory reset (backup created)                            ║
║   ✅ Temp files removed                                             ║
║   ✅ All code files safe                                            ║
║   ✅ Documentation preserved                                        ║
║   ✅ Training data kept                                             ║
║   ✅ Final videos saved                                             ║
║                                                                      ║
║   ਹੁਣ ਨਵੇਂ ਸਿਰੇ ਤੋਂ ਸ਼ੁਰੂ ਕਰੋ!                                         ║
║   (Now start fresh from the beginning!)                             ║
║                                                                      ║
║              ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ! ✨                               ║
║              ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ! 🙏                               ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    main()
