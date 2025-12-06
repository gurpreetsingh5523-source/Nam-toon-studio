#!/usr/bin/env python3
"""
📦 AMRIT DATA ORGANIZER
Automatically organize all discovered data into proper structure
ਸਾਰਾ ਡਾਟਾ ਆਪਣੇ ਆਪ ਠੀਕ ਤਰੀਕੇ ਨਾਲ ਰੱਖਦਾ ਹੈ
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
import subprocess

class AmritDataOrganizer:
    def __init__(self, dry_run=True):
        """
        Initialize organizer
        
        Args:
            dry_run: If True, only show what would be done (don't actually move files)
        """
        self.home = Path.home()
        self.dry_run = dry_run
        
        # Master data folder
        self.master_folder = self.home / "AMRIT_MASTER_DATA"
        
        # Sub-folders
        self.folders = {
            'brain_knowledge': self.master_folder / "01_Brain_Knowledge",
            'gurbani_spiritual': self.master_folder / "02_Gurbani_Spiritual",
            'photos': self.master_folder / "03_Photos_Library",
            'audio_kirtan': self.master_folder / "04_Audio_Kirtan",
            'pdfs': self.master_folder / "05_PDFs_Documents",
            'json_data': self.master_folder / "06_JSON_Data",
            'training_videos': self.master_folder / "07_Training_Videos",
            'ai_models': self.master_folder / "08_AI_Models"
        }
        
        # Create sub-categories
        self.sub_folders = {
            'brain_knowledge': [
                '01_Brain_Knowledge/SGGS_Core',
                '01_Brain_Knowledge/Punjabi_Language',
                '01_Brain_Knowledge/Punjab_History',
                '01_Brain_Knowledge/Computing_Tech',
                '01_Brain_Knowledge/Health_Wellness',
                '01_Brain_Knowledge/Other'
            ],
            'gurbani_spiritual': [
                '02_Gurbani_Spiritual/SGGS_Knowledge',
                '02_Gurbani_Spiritual/Lessons',
                '02_Gurbani_Spiritual/Scripts'
            ],
            'audio_kirtan': [
                '04_Audio_Kirtan/Gurbani_Kirtan',
                '04_Audio_Kirtan/Raag_Based',
                '04_Audio_Kirtan/Path_Paath',
                '04_Audio_Kirtan/Background_Music'
            ],
            'pdfs': [
                '05_PDFs_Documents/Sikhi_History',
                '05_PDFs_Documents/General'
            ]
        }
        
        self.stats = {
            'folders_created': 0,
            'files_organized': 0,
            'total_size_mb': 0,
            'errors': []
        }
    
    def create_folder_structure(self):
        """Create master folder and all sub-folders"""
        print("\n📁 Creating Folder Structure...")
        print("="*70)
        
        # Create master folder
        if not self.dry_run:
            self.master_folder.mkdir(parents=True, exist_ok=True)
        print(f"✅ Master: {self.master_folder}")
        self.stats['folders_created'] += 1
        
        # Create main category folders
        for name, path in self.folders.items():
            if not self.dry_run:
                path.mkdir(parents=True, exist_ok=True)
            print(f"   ├─ {path.name}/")
            self.stats['folders_created'] += 1
        
        # Create sub-category folders
        for category, sub_folders in self.sub_folders.items():
            for sub_folder in sub_folders:
                full_path = self.master_folder / sub_folder
                if not self.dry_run:
                    full_path.mkdir(parents=True, exist_ok=True)
                print(f"      ├─ {sub_folder}")
                self.stats['folders_created'] += 1
        
        print(f"\n✅ Created {self.stats['folders_created']} folders")
    
    def organize_brain_files(self):
        """Organize brain knowledge TXT files"""
        print("\n🧠 Organizing Brain Knowledge Files...")
        print("="*70)
        
        brain_locations = [
            self.home / "Nam-toon-studio",
            self.home / "AmritCore_QuantumBrain_OS/quantum_brain"
        ]
        
        category_keywords = {
            'SGGS_Core': ['sggs', 'guru', 'granth'],
            'Punjabi_Language': ['punjabi', 'language', 'idioms'],
            'Punjab_History': ['punjab', 'history', 'itihaas'],
            'Computing_Tech': ['computing', 'tech', 'software'],
            'Health_Wellness': ['health', 'sehhat', 'wellness']
        }
        
        for location in brain_locations:
            if not location.exists():
                continue
            
            for brain_file in location.glob("brain_*.txt"):
                try:
                    # Determine category
                    category = 'Other'
                    for cat, keywords in category_keywords.items():
                        if any(k in brain_file.name.lower() for k in keywords):
                            category = cat
                            break
                    
                    dest_folder = self.master_folder / "01_Brain_Knowledge" / category
                    dest_file = dest_folder / brain_file.name
                    
                    # Check if already exists
                    if dest_file.exists() and dest_file.stat().st_size >= brain_file.stat().st_size:
                        print(f"   ⏭️  Skip (exists): {brain_file.name}")
                        continue
                    
                    size_kb = brain_file.stat().st_size / 1024
                    self.stats['total_size_mb'] += size_kb / 1024
                    
                    if not self.dry_run:
                        shutil.copy2(brain_file, dest_file)
                    
                    print(f"   ✅ {brain_file.name} → {category}/ ({size_kb:.1f} KB)")
                    self.stats['files_organized'] += 1
                    
                except Exception as e:
                    error = f"Error with {brain_file.name}: {e}"
                    self.stats['errors'].append(error)
                    print(f"   ❌ {error}")
        
        print(f"\n✅ Organized {self.stats['files_organized']} brain files")
    
    def organize_gurbani_files(self):
        """Organize Gurbani spiritual files"""
        print("\n🕉️  Organizing Gurbani Files...")
        print("="*70)
        
        gurbani_locations = [
            self.home / "Desktop/amritkaur_local",
            self.home / "AmritCore_QuantumBrain_OS/amrit_lessons",
            self.home / "Nam-toon-studio"
        ]
        
        gurbani_files = [
            'gurbani_knowledge.json',
            'amrit_gurbani_studio.py',
            'amrit_gurbani_studio_lite.py',
            'amrit_spiritual_gurbani_reasoning.py',
            'sikh_spirituality_&_gurbani_interactive.txt',
            'sikh_spirituality_&_gurbani_lesson.json'
        ]
        
        count = 0
        for location in gurbani_locations:
            if not location.exists():
                continue
            
            for file_pattern in gurbani_files:
                for file in location.glob(f"*{file_pattern}*"):
                    if file.is_file():
                        try:
                            # Determine sub-category
                            if file.suffix == '.json':
                                sub_cat = 'SGGS_Knowledge'
                            elif 'lesson' in file.name.lower():
                                sub_cat = 'Lessons'
                            else:
                                sub_cat = 'Scripts'
                            
                            dest_folder = self.master_folder / "02_Gurbani_Spiritual" / sub_cat
                            dest_file = dest_folder / file.name
                            
                            if dest_file.exists():
                                print(f"   ⏭️  Skip (exists): {file.name}")
                                continue
                            
                            size_kb = file.stat().st_size / 1024
                            self.stats['total_size_mb'] += size_kb / 1024
                            
                            if not self.dry_run:
                                shutil.copy2(file, dest_file)
                            
                            print(f"   ✅ {file.name} → {sub_cat}/ ({size_kb:.1f} KB)")
                            count += 1
                            
                        except Exception as e:
                            error = f"Error with {file.name}: {e}"
                            self.stats['errors'].append(error)
                            print(f"   ❌ {error}")
        
        print(f"\n✅ Organized {count} Gurbani files")
    
    def organize_audio_files(self):
        """Organize audio/kirtan files"""
        print("\n🎵 Organizing Audio/Kirtan Files...")
        print("="*70)
        
        audio_locations = {
            'Gurbani_Kirtan': [
                self.home / "Desktop/gurbani keertan",
                self.home / "Desktop/amritkaur_local/gurbani_keertan"
            ],
            'Background_Music': [
                self.home / "Nam-toon-studio/audio"
            ]
        }
        
        count = 0
        for category, locations in audio_locations.items():
            for location in locations:
                if not location.exists():
                    continue
                
                for audio_file in location.glob("*.mp3"):
                    try:
                        # Determine sub-category
                        name_lower = audio_file.name.lower()
                        if any(r in name_lower for r in ['raag', 'bhairavi', 'bilaskhani', 'chandrakouns']):
                            sub_cat = 'Raag_Based'
                        elif any(p in name_lower for p in ['path', 'paath', 'anand', 'sukhmani']):
                            sub_cat = 'Path_Paath'
                        else:
                            sub_cat = category
                        
                        dest_folder = self.master_folder / "04_Audio_Kirtan" / sub_cat
                        dest_file = dest_folder / audio_file.name
                        
                        if dest_file.exists():
                            continue
                        
                        size_mb = audio_file.stat().st_size / (1024 * 1024)
                        self.stats['total_size_mb'] += size_mb
                        
                        if not self.dry_run:
                            shutil.copy2(audio_file, dest_file)
                        
                        print(f"   ✅ {audio_file.name[:40]}... → {sub_cat}/ ({size_mb:.1f} MB)")
                        count += 1
                        
                        if count >= 10:  # Show first 10 only
                            break
                    except Exception as e:
                        pass
                
                if count >= 10:
                    print(f"   ... (showing first 10, more files available)")
                    break
        
        print(f"\n✅ Organized audio files (showing preview)")
    
    def organize_pdfs(self):
        """Organize PDF documents"""
        print("\n📚 Organizing PDF Documents...")
        print("="*70)
        
        pdf_locations = [
            self.home / "Downloads"
        ]
        
        sikhi_keywords = ['guru', 'gurbani', 'sikhi', 'sggs', 'punjabi', 'morcha', 'khalsa']
        
        count = 0
        for location in pdf_locations:
            if not location.exists():
                continue
            
            for pdf_file in location.glob("*.pdf"):
                try:
                    # Determine category
                    name_lower = pdf_file.name.lower()
                    if any(k in name_lower for k in sikhi_keywords):
                        sub_cat = 'Sikhi_History'
                    else:
                        sub_cat = 'General'
                    
                    dest_folder = self.master_folder / "05_PDFs_Documents" / sub_cat
                    dest_file = dest_folder / pdf_file.name
                    
                    if dest_file.exists():
                        continue
                    
                    size_mb = pdf_file.stat().st_size / (1024 * 1024)
                    self.stats['total_size_mb'] += size_mb
                    
                    if not self.dry_run:
                        shutil.copy2(pdf_file, dest_file)
                    
                    print(f"   ✅ {pdf_file.name[:40]}... → {sub_cat}/ ({size_mb:.1f} MB)")
                    count += 1
                    
                    if count >= 10:  # Show first 10 only
                        break
                except Exception as e:
                    pass
        
        print(f"\n✅ Organized PDF files (showing preview)")
    
    def check_disk_space(self):
        """Check available disk space"""
        print("\n💾 Checking Disk Space...")
        print("="*70)
        
        try:
            result = subprocess.run(
                ['df', '-h', '/'],
                capture_output=True,
                text=True
            )
            
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                total = parts[1]
                used = parts[2]
                avail = parts[3]
                percent = parts[4]
                
                print(f"   Total: {total}")
                print(f"   Used: {used} ({percent})")
                print(f"   Available: {avail}")
                
                # Check if safe to proceed
                avail_gb = int(avail.replace('Gi', ''))
                if avail_gb < 50:
                    print(f"\n   ⚠️  WARNING: Low disk space ({avail})")
                    return False
                else:
                    print(f"\n   ✅ Sufficient space available")
                    return True
        except Exception as e:
            print(f"   ❌ Error checking disk space: {e}")
            return True  # Proceed anyway
    
    def generate_inventory(self):
        """Generate inventory of organized data"""
        print("\n📊 Generating Inventory...")
        print("="*70)
        
        inventory = {
            'organized_date': datetime.now().isoformat(),
            'master_folder': str(self.master_folder),
            'stats': self.stats,
            'folder_structure': {},
            'disk_space': {}
        }
        
        # Count files in each folder
        for name, path in self.folders.items():
            if path.exists():
                file_count = len(list(path.rglob('*')))
                total_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                inventory['folder_structure'][name] = {
                    'path': str(path),
                    'file_count': file_count,
                    'size_mb': round(total_size / (1024 * 1024), 2)
                }
        
        # Save inventory
        inventory_file = self.master_folder / "INVENTORY.json"
        if not self.dry_run:
            with open(inventory_file, 'w', encoding='utf-8') as f:
                json.dump(inventory, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Inventory saved to: {inventory_file}")
        return inventory
    
    def print_summary(self):
        """Print summary of organization"""
        print("\n" + "="*70)
        print("📊 ORGANIZATION SUMMARY")
        print("="*70)
        
        print(f"\n✅ Folders Created: {self.stats['folders_created']}")
        print(f"✅ Files Organized: {self.stats['files_organized']}")
        print(f"✅ Total Size: {self.stats['total_size_mb']:.2f} MB")
        
        if self.stats['errors']:
            print(f"\n❌ Errors: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:
                print(f"   • {error}")
        
        print(f"\n📁 Master Folder: {self.master_folder}")
        
        if self.dry_run:
            print("\n⚠️  DRY RUN MODE - No files were actually moved!")
            print("   Run with --execute to perform actual organization")
        else:
            print("\n✅ Organization complete!")
        
        print("\n" + "="*70)
    
    def run(self):
        """Run complete organization process"""
        print("\n" + "="*70)
        print("📦 AMRIT DATA ORGANIZER")
        print("="*70)
        
        if self.dry_run:
            print("\n⚠️  DRY RUN MODE - Simulating organization")
            print("   No files will be moved\n")
        else:
            print("\n🚀 EXECUTE MODE - Files will be organized\n")
        
        # Check disk space
        if not self.check_disk_space():
            print("\n❌ Insufficient disk space. Aborting.")
            return False
        
        # Create folder structure
        self.create_folder_structure()
        
        # Organize different types of data
        self.organize_brain_files()
        self.organize_gurbani_files()
        self.organize_audio_files()
        self.organize_pdfs()
        
        # Generate inventory
        if not self.dry_run:
            self.generate_inventory()
        
        # Print summary
        self.print_summary()
        
        return True

def main():
    import sys
    
    # Check for --execute flag
    dry_run = '--execute' not in sys.argv
    
    organizer = AmritDataOrganizer(dry_run=dry_run)
    organizer.run()
    
    if dry_run:
        print("\n💡 To actually organize files, run:")
        print("   python3 amrit_organizer.py --execute")

if __name__ == "__main__":
    main()
