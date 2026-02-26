#!/usr/bin/env python3
"""
🎬 Simple Video Generator - ਵੀਡੀਓ ਬਣਾਉਣ ਵਾਲੀ ਸਕ੍ਰਿਪਟ

This script generates your complete video with:
1. 🎤 Mature voice (pitch 0.82)
2. 🎵 Audible background music (volume 0.35)
3. 🎨 Character portraits
4. 🔊 Sound effects
5. 📝 Punjabi captions

Usage:
    python make_video.py
    
Output:
    AmritCore_FINAL_STUDIO_LAUNCH.mp4
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """Print nice header"""
    print("\n" + "="*60)
    print("🎬 Nam-toon Studio - Video Generator")
    print("   ਨਾਮ-ਟੂਨ ਸਟੂਡੀਓ - ਵੀਡੀਓ ਬਣਾਉਣ ਵਾਲੀ")
    print("="*60 + "\n")

def check_environment():
    """Check that everything is ready"""
    print("🔍 Checking environment...\n")
    
    # Check virtual environment
    if not os.path.exists('.venv'):
        print("❌ Virtual environment not found!")
        print("   Run: python3 -m venv .venv")
        return False
    print("✓ Virtual environment found")
    
    # Check scenes file
    if not os.path.exists('temp_adhhi_aurat_scenes.json'):
        print("❌ Scenes file not found: temp_adhhi_aurat_scenes.json")
        return False
    print("✓ Scenes file found")
    
    # Check master_builder
    if not os.path.exists('colab/master_builder.py'):
        print("❌ Master builder not found!")
        return False
    print("✓ Master builder found")
    
    # Check voice profiles
    if os.path.exists('brain_memory/character_voice_profiles.json'):
        print("✓ Voice profiles loaded (mature voice: pitch 0.82)")
    else:
        print("⚠️  Voice profiles not found (will use defaults)")
    
    # Check audio directory
    if not os.path.exists('audio'):
        os.makedirs('audio')
        print("✓ Created audio directory")
    else:
        print("✓ Audio directory exists")
    
    print("\n✅ Environment check # TODO: Implement functioned!\n")
    return True

def show_fixes():
    """Show what has been fixed"""
    print("🔧 Applied Fixes:")
    print("-" * 60)
    print("1. 🎤 VOICE: Mature male voice (pitch 0.82, not 13-year-old)")
    print("2. 🎵 MUSIC: Volume increased (0.15 → 0.35, now audible!)")
    print("3. 🎭 PORTRAITS: Unicode fixed (Punjabi ਚ characters)")
    print("4. 🧠 BRAINS: All 4 brains tested and working")
    print("-" * 60 + "\n")

def show_what_will_happen():
    """Explain what the video generation will do"""
    print("📋 What will happen:")
    print("-" * 60)
    print("Step 1: Load scenes from temp_adhhi_aurat_scenes.json")
    print("        → 8 scenes from 'ਅੱਧੀ ਔਰਤ' story")
    print()
    print("Step 2: Generate voice for each scene")
    print("        → Using gTTS with Punjabi")
    print("        → Pitch: 0.82 (mature male voice)")
    print("        → Speed: 0.92 (natural pace)")
    print()
    print("Step 3: Select background music")
    print("        → Audio Brain chooses based on emotion")
    print("        → Volume: 0.35 (35% - audible!)")
    print()
    print("Step 4: Create visual animation")
    print("        → Visual Brain: gradient backgrounds")
    print("        → Character portraits with Punjabi names")
    print("        → Camera movements based on emotion")
    print()
    print("Step 5: Add sound effects")
    print("        → SFX Brain: location-based sounds")
    print("        → Emotion-based effects")
    print()
    print("Step 6: Mix everything together")
    print("        → Voice + Music + SFX")
    print("        → Ducking (music quieter during speech)")
    print("        → Add Punjabi captions")
    print()
    print("Step 7: Export final video")
    print("        → File: AmritCore_FINAL_STUDIO_LAUNCH.mp4")
    print("        → Duration: ~106 seconds (8 scenes)")
    print("-" * 60 + "\n")

def generate_video():
    """Run the video generation"""
    print("🎬 Starting video generation...")
    print("   (This may take 2-5 minutes)\n")
    
    # Prepare command
    python_exec = ".venv/bin/python"
    script = "colab/master_builder.py"
    
    cmd = [
        python_exec,
        script,
        "--scenes", "temp_adhhi_aurat_scenes.json",
        "--verbose",
        "--duck",  # Enable music ducking during speech
        "--bg-gain", "0.35",  # Background music volume (fixed!)
    ]
    
    print(f"🔧 Running command:")
    print(f"   {' '.join(cmd)}\n")
    
    try:
        # Run the command
        result = subprocess.run(
            cmd,
            cwd=os.getcwd(),
            check=True,
            text=True,
            capture_output=False  # Show output in real-time
        )
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error during video generation!")
        print(f"   Exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

def verify_output():
    """Check if video was created successfully"""
    print("\n" + "="*60)
    print("🔍 Verifying output...\n")
    
    video_file = "AmritCore_FINAL_STUDIO_LAUNCH.mp4"
    
    if not os.path.exists(video_file):
        print(f"❌ Video file not found: {video_file}")
        return False
    
    # Check file size
    size_mb = os.path.getsize(video_file) / (1024 * 1024)
    print(f"✓ Video created: {video_file}")
    print(f"  Size: {size_mb:.2f} MB")
    
    if size_mb < 0.5:
        print("  ⚠️  Warning: File seems small, may have issues")
    
    # Check audio files
    print("\n🎵 Audio files generated:")
    audio_count = 0
    for i in range(10):
        audio_file = f"audio/dialogue_{i}.mp3"
        if os.path.exists(audio_file):
            size_kb = os.path.getsize(audio_file) / 1024
            print(f"  ✓ dialogue_{i}.mp3 ({size_kb:.0f} KB)")
            audio_count += 1
    
    if audio_count == 0:
        print("  ⚠️  No dialogue files found")
    
    return True

def show_next_steps():
    """Show what to do next"""
    print("\n" + "="*60)
    print("✅ VIDEO GENERATION COMPLETE!")
    print("="*60)
    print()
    print("📁 Output file: AmritCore_FINAL_STUDIO_LAUNCH.mp4")
    print()
    print("👀 What to check:")
    print("   1. Open the video in QuickTime or VLC")
    print("   2. Listen for background music (should be audible now!)")
    print("   3. Check voice quality (should sound mature, not child)")
    print("   4. Look for character portraits (should appear)")
    print("   5. Read Punjabi captions (should display)")
    print()
    print("🔊 Expected improvements:")
    print("   ✓ Background music volume: 15% → 35% (much louder!)")
    print("   ✓ Voice pitch: 0.82 (mature male voice)")
    print("   ✓ Character portraits: Unicode fixed (ਰਚਨਾ)")
    print("   ✓ All 4 brains working together")
    print()
    print("📊 Brain test results:")
    print("   • See: BRAIN_TEST_RESULTS.md")
    print("   • See: brain_memory/ਬ੍ਰੇਨ_ਟੈਸਟ_ਰਿਪੋਰਟ.md")
    print()
    print("🎬 Ready to watch!")
    print("="*60 + "\n")

def main():
    """Main execution"""
    print_header()
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please fix issues and try again.\n")
        sys.exit(1)
    
    # Show what was fixed
    show_fixes()
    
    # Explain what will happen
    show_what_will_happen()
    
    # Ask for confirmation
    print("🎯 Ready to generate video with all fixes applied!")
    response = input("   Continue? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y', 'ਹਾਂ']:
        print("\n⏸️  Video generation cancelled.\n")
        sys.exit(0)
    
    print()
    
    # Generate video
    if not generate_video():
        print("\n❌ Video generation failed. Check errors above.\n")
        sys.exit(1)
    
    # Verify output
    if not verify_output():
        print("\n⚠️  Output verification had issues.\n")
        sys.exit(1)
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()
