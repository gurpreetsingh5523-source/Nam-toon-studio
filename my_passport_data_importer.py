#!/usr/bin/env python3
"""
💾 MY PASSPORT DATA IMPORTER
Import all training data from My Passport external drive

ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ! 🙏
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json

class MyPassportDataImporter:
    """Import data from My Passport drive"""
    
    def __init__(self):
        self.passport_path = Path("/Volumes/My Passport")
        self.workspace = Path(__file__).parent
        
        # Create organized folders
        self.training_photos = self.workspace / "training_photos"
        self.training_audio = self.workspace / "training_audio"
        self.training_video = self.workspace / "training_video"
        self.training_pdfs = self.workspace / "training_pdfs"
        
        for folder in [self.training_photos, self.training_audio, 
                      self.training_video, self.training_pdfs]:
            folder.mkdir(exist_ok=True)
        
        print("💾 My Passport Data Importer initialized")
        print(f"   Source: {self.passport_path}")
    
    def check_drive_connected(self):
        """Check if My Passport is connected"""
        if not self.passport_path.exists():
            print("❌ My Passport drive not found!")
            print("   Please connect the drive and try again")
            return False
        
        print("✅ My Passport drive connected")
        return True
    
    def scan_drive(self):
        """Scan entire drive for data"""
        print("\n🔍 Scanning My Passport drive...")
        print("   This might take a few minutes...")
        print()
        
        stats = {
            "photos": [],
            "videos": [],
            "audio": [],
            "pdfs": [],
            "total_size": 0
        }
        
        # Important folders
        important_folders = [
            "gurpreet pics",
            "keertan",
            "katha",
            "ਭਾਈ ਗੁਰਦਾਸ ਕੰਪਿਊਟਰ ਲਾਇਬਰੇਰੀ",
            "New folder"
        ]
        
        for folder_name in important_folders:
            folder_path = self.passport_path / folder_name
            if not folder_path.exists():
                continue
            
            print(f"📂 Scanning: {folder_name}")
            
            # Find all files
            for ext_group, extensions in [
                ("photos", ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]),
                ("videos", ["*.mp4", "*.mov", "*.avi", "*.mkv", "*.MP4", "*.MOV"]),
                ("audio", ["*.mp3", "*.wav", "*.m4a", "*.MP3", "*.WAV"]),
                ("pdfs", ["*.pdf", "*.PDF"])
            ]:
                for ext in extensions:
                    try:
                        files = list(folder_path.glob(f"**/{ext}"))
                        for f in files:
                            stats[ext_group].append(f)
                            stats["total_size"] += f.stat().st_size
                    except Exception as e:
                        continue
        
        print(f"\n📊 Scan Complete:")
        print(f"   📸 Photos: {len(stats['photos']):,}")
        print(f"   🎬 Videos: {len(stats['videos']):,}")
        print(f"   🎵 Audio: {len(stats['audio']):,}")
        print(f"   📄 PDFs: {len(stats['pdfs']):,}")
        print(f"   💾 Total: {stats['total_size']/(1024**3):.2f} GB")
        
        return stats
    
    def import_photos_for_training(self, max_photos=500):
        """Import photos for AI training"""
        print(f"\n📸 Importing up to {max_photos} photos for training...")
        
        gurpreet_pics = self.passport_path / "gurpreet pics"
        if not gurpreet_pics.exists():
            print("❌ gurpreet pics folder not found")
            return 0
        
        # Find all photos
        photo_extensions = ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]
        all_photos = []
        
        for ext in photo_extensions:
            all_photos.extend(gurpreet_pics.glob(f"**/{ext}"))
        
        print(f"   Found {len(all_photos):,} photos")
        
        # Copy photos
        copied = 0
        skipped = 0
        
        for photo in all_photos[:max_photos]:
            try:
                # Skip very small files (probably icons)
                if photo.stat().st_size < 10000:  # < 10KB
                    skipped += 1
                    continue
                
                dest = self.training_photos / photo.name
                
                # Skip if already exists
                if dest.exists():
                    skipped += 1
                    continue
                
                # Copy
                shutil.copy2(photo, dest)
                copied += 1
                
                if copied % 50 == 0:
                    print(f"   Copied: {copied}/{max_photos}")
                
            except Exception as e:
                print(f"   ⚠️  Error with {photo.name}: {e}")
                continue
        
        print(f"\n✅ Import complete:")
        print(f"   Copied: {copied} photos")
        print(f"   Skipped: {skipped} (duplicates/small files)")
        
        return copied
    
    def import_keertan_audio(self, max_files=100):
        """Import Gurbani Keertan audio for AI learning"""
        print(f"\n🎵 Importing Keertan audio files...")
        
        keertan_path = self.passport_path / "keertan"
        if not keertan_path.exists():
            print("❌ keertan folder not found")
            return 0
        
        # Find audio files
        audio_files = []
        for ext in ["*.mp3", "*.wav", "*.m4a", "*.MP3"]:
            audio_files.extend(keertan_path.glob(f"**/{ext}"))
        
        print(f"   Found {len(audio_files):,} audio files")
        
        # Copy files
        copied = 0
        for audio in audio_files[:max_files]:
            try:
                dest = self.training_audio / audio.name
                if not dest.exists():
                    shutil.copy2(audio, dest)
                    copied += 1
                    
                    if copied % 10 == 0:
                        print(f"   Copied: {copied}/{max_files}")
            except Exception as e:
                continue
        
        print(f"✅ Imported {copied} keertan files")
        return copied
    
    def import_gurbani_pdfs(self, max_files=50):
        """Import Gurbani PDFs for AI learning"""
        print(f"\n📄 Importing Gurbani PDFs...")
        
        bhai_gurdas_path = self.passport_path / "ਭਾਈ ਗੁਰਦਾਸ ਕੰਪਿਊਟਰ ਲਾਇਬਰੇਰੀ"
        
        pdf_files = []
        for folder in [bhai_gurdas_path]:
            if folder.exists():
                pdf_files.extend(folder.glob("**/*.pdf"))
                pdf_files.extend(folder.glob("**/*.PDF"))
        
        print(f"   Found {len(pdf_files):,} PDF files")
        
        # Copy PDFs
        copied = 0
        for pdf in pdf_files[:max_files]:
            try:
                dest = self.training_pdfs / pdf.name
                if not dest.exists():
                    shutil.copy2(pdf, dest)
                    copied += 1
            except Exception as e:
                continue
        
        print(f"✅ Imported {copied} PDF files")
        return copied
    
    def create_training_report(self, stats):
        """Create detailed training report"""
        report = {
            "import_date": datetime.now().isoformat(),
            "source": str(self.passport_path),
            "imported_data": {
                "photos": len(list(self.training_photos.glob("*"))),
                "audio": len(list(self.training_audio.glob("*"))),
                "videos": len(list(self.training_video.glob("*"))),
                "pdfs": len(list(self.training_pdfs.glob("*")))
            },
            "available_on_drive": {
                "photos": len(stats["photos"]),
                "audio": len(stats["audio"]),
                "videos": len(stats["videos"]),
                "pdfs": len(stats["pdfs"])
            },
            "ready_for_training": True,
            "next_steps": [
                "Run: python3 ai_training_orchestrator.py",
                "AI will learn from photos, keertan, and PDFs",
                "Training time: 2-3 hours (overnight recommended)"
            ]
        }
        
        report_file = self.workspace / "MY_PASSPORT_IMPORT_REPORT.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Report saved: {report_file}")
        return report


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("💾 MY PASSPORT DATA IMPORTER")
    print("   Training AI with Your Personal Data")
    print("   ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ")
    print("="*70)
    
    importer = MyPassportDataImporter()
    
    # Check drive
    if not importer.check_drive_connected():
        return
    
    # Scan drive
    stats = importer.scan_drive()
    
    # Import data
    print("\n" + "="*70)
    print("📥 IMPORTING DATA")
    print("="*70)
    
    photos_imported = importer.import_photos_for_training(max_photos=500)
    audio_imported = importer.import_keertan_audio(max_files=100)
    pdfs_imported = importer.import_gurbani_pdfs(max_files=50)
    
    # Create report
    report = importer.create_training_report(stats)
    
    # Summary
    print("\n" + "="*70)
    print("✅ DATA IMPORT COMPLETE!")
    print("="*70)
    print()
    print(f"📊 Imported:")
    print(f"   📸 Photos: {photos_imported}")
    print(f"   🎵 Keertan Audio: {audio_imported}")
    print(f"   📄 Gurbani PDFs: {pdfs_imported}")
    print()
    print("🧠 Ready for AI Training!")
    print()
    print("🚀 Next Steps:")
    print("   1. Check imported data in folders:")
    print("      • training_photos/")
    print("      • training_audio/")
    print("      • training_pdfs/")
    print()
    print("   2. Start AI training (overnight recommended):")
    print("      python3 ai_training_orchestrator.py")
    print()
    print("   3. This will train all 7 AI brains on:")
    print("      • Your photos (faces, people, diversity)")
    print("      • Gurbani Keertan (voice, pronunciation)")
    print("      • Sikh texts (cultural context, language)")
    print()
    print("🙏 ਵਾਹਿਗੁਰੂ ਮਿਹਰ ਕਰੇ!")


if __name__ == "__main__":
    main()
