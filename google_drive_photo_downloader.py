#!/usr/bin/env python3
"""
📥 GOOGLE DRIVE PHOTO DOWNLOADER
Downloads training photos from Google Drive for AI training

ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ! 🙏
"""

import os
from pathlib import Path
import json

class GoogleDrivePhotoDownloader:
    """Download photos from Google Drive"""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path(__file__).parent
        self.photos_dir = self.workspace / "training_photos"
        self.photos_dir.mkdir(exist_ok=True)
        
        # Categories for organization
        self.categories = {
            "punjabi_men": self.photos_dir / "punjabi_men",
            "punjabi_women": self.photos_dir / "punjabi_women",
            "kids": self.photos_dir / "kids",
            "elderly": self.photos_dir / "elderly",
            "groups": self.photos_dir / "groups",
            "turbans": self.photos_dir / "turbans",
            "suits": self.photos_dir / "suits",
            "traditional": self.photos_dir / "traditional",
            "modern": self.photos_dir / "modern"
        }
        
        # Create category folders
        for cat_path in self.categories.values():
            cat_path.mkdir(exist_ok=True)
        
        print("📥 Google Drive Photo Downloader initialized")
        print(f"📂 Photos will be saved to: {self.photos_dir}")
    
    def setup_drive_api(self):
        """Setup Google Drive API (requires google-auth)"""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            import pickle
            
            SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
            
            creds = None
            token_file = self.workspace / 'token.pickle'
            
            # Load existing credentials
            if token_file.exists():
                with open(token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            # Get new credentials if needed
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    print("\n⚠️  Need Google Drive authentication")
                    print("   Please follow instructions to authorize")
                    # Would need credentials.json file
                    return None
            
            # Build service
            service = build('drive', 'v3', credentials=creds)
            print("✅ Google Drive API connected")
            return service
            
        except ImportError:
            print("⚠️  Google Drive libraries not installed")
            print("   Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
            return None
        except Exception as e:
            print(f"❌ Drive API setup failed: {e}")
            return None
    
    def download_from_folder(self, service, folder_id):
        """Download all photos from a Google Drive folder"""
        if not service:
            print("❌ No Drive service available")
            return []
        
        try:
            # List files in folder
            results = service.files().list(
                q=f"'{folder_id}' in parents and (mimeType='image/jpeg' or mimeType='image/png')",
                pageSize=1000,
                fields="files(id, name, mimeType)"
            ).execute()
            
            files = results.get('files', [])
            print(f"📊 Found {len(files)} photos in Drive folder")
            
            downloaded = []
            for i, file in enumerate(files, 1):
                print(f"   Downloading {i}/{len(files)}: {file['name']}")
                
                # Download file
                request = service.files().get_media(fileId=file['id'])
                file_path = self.photos_dir / file['name']
                
                import io
                from googleapiclient.http import MediaIoBaseDownload
                
                fh = io.FileIO(file_path, 'wb')
                downloader = MediaIoBaseDownload(fh, request)
                
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                
                downloaded.append(file_path)
                
            print(f"✅ Downloaded {len(downloaded)} photos")
            return downloaded
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return []
    
    def use_local_photos(self, photos_folder=None):
        """Use photos from local folder instead of Drive"""
        if photos_folder:
            source = Path(photos_folder)
        else:
            # Check common locations
            possible_locations = [
                Path.home() / "Pictures" / "Punjabi_Photos",
                Path.home() / "Downloads" / "photos",
                self.workspace / "photos",
            ]
            
            source = None
            for loc in possible_locations:
                if loc.exists():
                    source = loc
                    break
        
        if not source or not source.exists():
            print("❌ No local photos folder found")
            print("\n📝 Please put your photos in one of:")
            print(f"   {Path.home()}/Pictures/Punjabi_Photos/")
            print(f"   {self.workspace}/photos/")
            return []
        
        print(f"📂 Using local photos from: {source}")
        
        # Copy photos
        photos = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.PNG']:
            photos.extend(source.glob(f'**/{ext}'))
        
        print(f"📊 Found {len(photos)} photos locally")
        
        # Copy to training folder
        import shutil
        copied = []
        for photo in photos:
            dest = self.photos_dir / photo.name
            if not dest.exists():
                shutil.copy2(photo, dest)
            copied.append(dest)
        
        print(f"✅ Copied {len(copied)} photos to training folder")
        return copied
    
    def analyze_photos(self):
        """Analyze downloaded photos"""
        photos = list(self.photos_dir.glob('*.jpg')) + list(self.photos_dir.glob('*.png'))
        
        if not photos:
            print("⚠️  No photos found in training folder")
            return
        
        print(f"\n📊 PHOTO ANALYSIS:")
        print(f"   Total photos: {len(photos)}")
        
        # Calculate total size
        total_size = sum(p.stat().st_size for p in photos)
        print(f"   Total size: {total_size / (1024*1024):.1f} MB")
        
        # Group by size for quality check
        high_quality = [p for p in photos if p.stat().st_size > 500000]  # > 500KB
        medium_quality = [p for p in photos if 100000 < p.stat().st_size <= 500000]
        low_quality = [p for p in photos if p.stat().st_size <= 100000]
        
        print(f"\n   Quality distribution:")
        print(f"   High (>500KB): {len(high_quality)}")
        print(f"   Medium (100-500KB): {len(medium_quality)}")
        print(f"   Low (<100KB): {len(low_quality)}")
        
        if len(high_quality) < 50:
            print("\n   ⚠️  Need more high-quality photos (at least 50)")
        
        return {
            "total": len(photos),
            "high_quality": len(high_quality),
            "medium_quality": len(medium_quality),
            "low_quality": len(low_quality),
            "total_size_mb": total_size / (1024*1024)
        }
    
    def create_dataset_info(self):
        """Create dataset info file"""
        info = {
            "dataset_name": "Punjabi People Training Dataset",
            "created": str(Path(__file__).parent),
            "photos_location": str(self.photos_dir),
            "categories": {k: str(v) for k, v in self.categories.items()},
            "purpose": "Train AI to generate diverse realistic Punjabi characters",
            "usage": "For Nam-toon-studio video generation"
        }
        
        info_file = self.photos_dir / "dataset_info.json"
        with open(info_file, 'w') as f:
            json.dump(info, f, indent=2)
        
        print(f"✅ Dataset info saved: {info_file}")
        return info


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("📥 GOOGLE DRIVE PHOTO DOWNLOADER")
    print("   Training AI with Real Photos")
    print("   ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ")
    print("="*70)
    
    downloader = GoogleDrivePhotoDownloader()
    
    print("\n📋 OPTION 1: Download from Google Drive")
    print("   Requires: Google API credentials and folder ID")
    print()
    print("📋 OPTION 2: Use local photos")
    print("   Put photos in: ~/Pictures/Punjabi_Photos/")
    print()
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        folder_id = input("Enter Google Drive folder ID: ").strip()
        service = downloader.setup_drive_api()
        if service:
            photos = downloader.download_from_folder(service, folder_id)
        else:
            print("❌ Cannot connect to Google Drive")
            print("   Falling back to local photos...")
            photos = downloader.use_local_photos()
    else:
        photos_folder = input("Enter photos folder path (or press Enter for default): ").strip()
        photos = downloader.use_local_photos(photos_folder if photos_folder else None)
    
    if photos:
        # Analyze photos
        analysis = downloader.analyze_photos()
        
        # Create dataset info
        downloader.create_dataset_info()
        
        print("\n✅ PHOTO DOWNLOAD COMPLETE!")
        print(f"   Photos ready for AI training: {len(photos)}")
        print(f"   Location: {downloader.photos_dir}")
        print()
        print("📚 Next steps:")
        print("   1. Run photo_analyzer.py to categorize photos")
        print("   2. Run ai_training_orchestrator.py to train all brains")
        print("   3. Generate diverse realistic characters!")
    else:
        print("\n❌ No photos available")
        print("   Please provide photos to train AI")


if __name__ == "__main__":
    main()
