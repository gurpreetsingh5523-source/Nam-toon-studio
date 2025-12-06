#!/usr/bin/env python3
"""
📸 PHOTO LIBRARY ANALYZER
Analyzes Photos library and extracts valuable data for AI training
With love and trust! 🙏
"""

import subprocess
import json
import os
from pathlib import Path
from datetime import datetime

print("�� PHOTO LIBRARY ANALYZER")
print("ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ!")
print("=" * 70)

def get_photo_count():
    """Get total photo count"""
    script = 'tell application "Photos" to get the count of media items'
    result = subprocess.run(['osascript', '-e', script], 
                          capture_output=True, text=True)
    return result.stdout.strip()

def get_albums():
    """Get all album names"""
    script = '''
    tell application "Photos"
        set albumList to {}
        repeat with anAlbum in albums
            set end of albumList to name of anAlbum
        end repeat
        return albumList
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], 
                          capture_output=True, text=True)
    return result.stdout.strip()

def analyze_library():
    """Analyze the Photos library"""
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'total_photos': 0,
        'albums': [],
        'can_access': False
    }
    
    print("\n🔍 ANALYZING PHOTOS LIBRARY...")
    print("-" * 70)
    
    try:
        # Get count
        count = get_photo_count()
        analysis['total_photos'] = int(count) if count.isdigit() else 0
        analysis['can_access'] = True
        
        print(f"   ✅ Total Photos: {analysis['total_photos']:,}")
        
        # Get albums
        albums_raw = get_albums()
        if albums_raw:
            albums_list = [a.strip() for a in albums_raw.split(',')]
            analysis['albums'] = albums_list[:20]  # First 20
            
            print(f"   ✅ Total Albums: {len(albums_list)}")
            print(f"\n   📁 Sample Albums (first 10):")
            for i, album in enumerate(albums_list[:10], 1):
                print(f"      {i}. {album}")
        
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
        analysis['error'] = str(e)
    
    return analysis

def check_exported_photos():
    """Check for already exported photos"""
    print("\n\n📂 CHECKING FOR EXPORTED PHOTOS...")
    print("-" * 70)
    
    locations = [
        Path.home() / "Desktop" / "Nam-toon-studio" / "images",
        Path.home() / "Documents" / "AMRIT_Photos",
        Path.home() / "Downloads",
        Path.home() / "Desktop"
    ]
    
    found = {}
    
    for loc in locations:
        if loc.exists():
            # Count image files
            images = list(loc.glob("*.jpg")) + list(loc.glob("*.png")) + \
                    list(loc.glob("*.jpeg")) + list(loc.glob("*.heic"))
            
            if images:
                found[str(loc)] = len(images)
                print(f"   ✅ {loc.name}: {len(images)} images")
    
    if not found:
        print("   ⚠️  No exported images found")
    
    return found

def suggest_next_steps(analysis, exported):
    """Suggest what to do next"""
    print("\n\n💡 SUGGESTIONS FOR AI TRAINING:")
    print("=" * 70)
    
    if analysis['total_photos'] > 0:
        print(f"\n✅ You have {analysis['total_photos']:,} photos in library!")
        print("\n📋 RECOMMENDED ACTIONS:")
        print("   1. Export specific albums for AI training")
        print("   2. Create 'Punjab Culture' album → Export")
        print("   3. Create 'Punjabi People' album → Export")
        print("   4. Create 'Family' album → Export")
        print("\n   These can train AI for:")
        print("      • Realistic Punjabi faces")
        print("      • Authentic Punjab settings")
        print("      • Cultural elements (turbans, dresses)")
        print("      • Real village/city backgrounds")
    
    if exported:
        print(f"\n✅ Found {sum(exported.values())} exported images!")
        print("   Can use these immediately for training!")
    
    print("\n🎯 VALUE FOR AI TRAINING:")
    print("   • Photorealistic Punjabi characters")
    print("   • Authentic backgrounds")
    print("   • Cultural accuracy")
    print("   • Better than generic stock images")
    
    # Save analysis
    output_file = Path("photo_library_analysis.json")
    with open(output_file, 'w') as f:
        json.dump({
            'analysis': analysis,
            'exported_locations': exported,
            'recommendations': {
                'export_albums': ['Punjab Culture', 'Punjabi People', 'Family'],
                'use_for': ['character_training', 'background_generation', 'style_transfer']
            }
        }, f, indent=2)
    
    print(f"\n💾 Analysis saved: {output_file}")

# Main execution
if __name__ == "__main__":
    try:
        # Analyze
        analysis = analyze_library()
        
        # Check exported
        exported = check_exported_photos()
        
        # Suggestions
        suggest_next_steps(analysis, exported)
        
        print("\n" + "=" * 70)
        print("✅ ANALYSIS COMPLETE!")
        print("🙏 ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫ਼ਤਿਹ!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
