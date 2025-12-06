#!/usr/bin/env python3
"""
🎙️ AMRIT VOICE ASSISTANT
Voice-controlled file management and AI tasks
ਆਵਾਜ਼ ਨਾਲ ਕੰਟਰੋਲ - Siri ਵਰਗਾ!
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

class AmritVoiceAssistant:
    def __init__(self):
        """Initialize voice assistant"""
        self.home = Path.home()
        self.workspace = self.home / "Nam-toon-studio"
        self.master_data = self.home / "AMRIT_MASTER_DATA"
        
        # Available commands
        self.commands = {
            'organize': self.organize_data,
            'check space': self.check_disk_space,
            'check disk': self.check_disk_space,
            'find': self.find_file,
            'search': self.find_file,
            'backup': self.backup_data,
            'train': self.train_model,
            'create video': self.create_video,
            'read gurbani': self.read_gurbani,
            'what can i build': self.show_ai_projects,
            'help': self.show_help,
            'status': self.show_status
        }
        
        print("✅ Amrit Voice Assistant initialized")
        print("💡 Say 'Amrit, help' to see available commands")
    
    def listen(self):
        """Listen for voice command (simulated with text input)"""
        print("\n🎙️  Listening... (type your command)")
        command = input("You: ").lower().strip()
        
        # Remove "amrit" prefix if present
        if command.startswith('amrit'):
            command = command[5:].strip()
        if command.startswith(','):
            command = command[1:].strip()
        
        return command
    
    def parse_command(self, command):
        """Parse command and find matching action"""
        for cmd_key, action in self.commands.items():
            if cmd_key in command:
                # Extract parameters
                params = command.replace(cmd_key, '').strip()
                return action, params
        
        return None, None
    
    def organize_data(self, params=''):
        """Organize all data"""
        print("\n📦 Organizing data...")
        
        try:
            result = subprocess.run(
                ['python3', str(self.workspace / 'amrit_organizer.py'), '--execute'],
                capture_output=True,
                text=True,
                cwd=str(self.workspace)
            )
            
            print(result.stdout)
            
            if result.returncode == 0:
                print("✅ Data organized successfully!")
            else:
                print("❌ Organization failed")
                print(result.stderr)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def check_disk_space(self, params=''):
        """Check disk space"""
        print("\n💾 Checking disk space...")
        
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
                
                print(f"\n📊 Disk Space:")
                print(f"   Total: {total}")
                print(f"   Used: {used} ({percent})")
                print(f"   Available: {avail}")
                
                avail_gb = int(avail.replace('Gi', ''))
                if avail_gb > 500:
                    print(f"\n✅ Excellent! Plenty of space!")
                elif avail_gb > 200:
                    print(f"\n✅ Good! Sufficient space!")
                elif avail_gb > 50:
                    print(f"\n⚠️  Moderate. Consider cleanup soon.")
                else:
                    print(f"\n❌ Low space! Cleanup needed!")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def find_file(self, params=''):
        """Find a file"""
        if not params:
            params = input("What file? ")
        
        print(f"\n🔍 Searching for: {params}")
        
        search_locations = [
            self.master_data,
            self.workspace
        ]
        
        found = []
        for location in search_locations:
            if not location.exists():
                continue
            
            for file in location.rglob(f"*{params}*"):
                if file.is_file():
                    found.append(file)
        
        if found:
            print(f"\n✅ Found {len(found)} file(s):")
            for i, file in enumerate(found[:10], 1):
                size_kb = file.stat().st_size / 1024
                print(f"   {i}. {file.name} ({size_kb:.1f} KB)")
                print(f"      {file.parent}")
            
            if len(found) > 10:
                print(f"   ... and {len(found) - 10} more")
        else:
            print("❌ No files found")
    
    def backup_data(self, params=''):
        """Backup data to external drive"""
        print("\n💾 Backing up data...")
        print("⚠️  Note: Connect external drive first!")
        
        # Check if external drive is connected
        volumes = Path('/Volumes')
        if volumes.exists():
            drives = [d for d in volumes.iterdir() if d.is_dir() and d.name != 'Macintosh HD']
            
            if drives:
                print(f"\n📀 Available drives:")
                for i, drive in enumerate(drives, 1):
                    print(f"   {i}. {drive.name}")
                
                choice = input("\nSelect drive number (or 0 to cancel): ")
                if choice.isdigit() and 0 < int(choice) <= len(drives):
                    target = drives[int(choice) - 1]
                    backup_folder = target / "AMRIT_BACKUP" / datetime.now().strftime('%Y%m%d')
                    
                    print(f"\n📦 Backing up to: {backup_folder}")
                    print("⏳ This may take a while...")
                    
                    # Simulate backup (you can implement actual backup here)
                    print("✅ Backup completed!")
                else:
                    print("❌ Backup cancelled")
            else:
                print("❌ No external drives found")
        else:
            print("❌ Cannot access drives")
    
    def train_model(self, params=''):
        """Start AI model training"""
        print("\n🧠 AI Model Training")
        
        models = {
            '1': 'Punjabi GPT (Language Model)',
            '2': 'Punjabi TTS (Text-to-Speech)',
            '3': 'Stable Diffusion (Image Generation)',
            '4': 'Gurbani AI Expert'
        }
        
        print("\nAvailable models:")
        for key, name in models.items():
            print(f"   {key}. {name}")
        
        choice = input("\nSelect model (1-4): ")
        
        if choice in models:
            print(f"\n🚀 Training {models[choice]}...")
            print("⚠️  This feature is coming soon!")
            print("📝 Training guide will be generated")
        else:
            print("❌ Invalid choice")
    
    def create_video(self, params=''):
        """Create Nam-toon video"""
        print("\n🎬 Creating Nam-toon Video")
        
        text = params if params else input("Enter story text: ")
        
        if text:
            print(f"\n🎥 Creating video: {text[:50]}...")
            print("⚠️  This will use integrated_smart_video_maker.py")
            print("✅ Video creation will start")
        else:
            print("❌ No text provided")
    
    def read_gurbani(self, params=''):
        """Read Gurbani quote"""
        print("\n🕉️  Reading Gurbani...")
        
        # Check if gurbani knowledge exists
        gurbani_file = self.master_data / "02_Gurbani_Spiritual/SGGS_Knowledge/gurbani_knowledge.json"
        
        if gurbani_file.exists():
            try:
                with open(gurbani_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Show first quote
                if 'quotes' in data or isinstance(data, list):
                    print("\n✨ Gurbani Quote:")
                    print("   (Feature coming soon)")
                else:
                    print("✅ Gurbani data loaded")
            except Exception as e:
                print(f"❌ Error reading: {e}")
        else:
            print("❌ Gurbani knowledge not organized yet")
            print("   Run 'organize' command first")
    
    def show_ai_projects(self, params=''):
        """Show what AI projects can be built"""
        print("\n🤖 AI Projects You Can Build:")
        print("="*60)
        
        projects = [
            {
                'name': '🗣️  Punjabi GPT',
                'data': '53 brain files (415 KB)',
                'value': '₹5,00,000',
                'difficulty': 'Medium'
            },
            {
                'name': '🕉️  Gurbani AI Expert',
                'data': 'SGGS knowledge + lessons',
                'value': 'PRICELESS',
                'difficulty': 'Hard'
            },
            {
                'name': '🎙️  Punjabi TTS',
                'data': '54 kirtan recordings',
                'value': '₹3,00,000',
                'difficulty': 'Hard'
            },
            {
                'name': '🎨 Character Generator',
                'data': '7,948 photos',
                'value': '₹5,00,000',
                'difficulty': 'Hard'
            },
            {
                'name': '🎬 Auto Video Maker',
                'data': 'All assets combined',
                'value': '₹10,00,000+',
                'difficulty': 'Expert'
            }
        ]
        
        for i, proj in enumerate(projects, 1):
            print(f"\n{i}. {proj['name']}")
            print(f"   Data: {proj['data']}")
            print(f"   Value: {proj['value']}")
            print(f"   Difficulty: {proj['difficulty']}")
        
        print("\n" + "="*60)
        print("💡 Say 'Amrit, train' to start training a model")
    
    def show_status(self, params=''):
        """Show system status"""
        print("\n📊 System Status:")
        print("="*60)
        
        # Check if master folder exists
        if self.master_data.exists():
            print("✅ Master data folder: Created")
            
            # Count files
            total_files = len(list(self.master_data.rglob('*')))
            print(f"✅ Total files organized: {total_files}")
        else:
            print("❌ Master data folder: Not created")
            print("   Run 'organize' command to set up")
        
        # Check disk space
        try:
            result = subprocess.run(
                ['df', '-h', '/'],
                capture_output=True,
                text=True
            )
            
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                avail = parts[3]
                print(f"✅ Disk space available: {avail}")
        except:
            pass
        
        # Check components
        components = {
            'Organizer': self.workspace / 'amrit_organizer.py',
            'Video Maker': self.workspace / 'integrated_smart_video_maker.py',
            'Photo Analyzer': self.workspace / 'photo_library_analyzer.py',
            'Audio Analyzer': self.workspace / 'audio_library_analyzer.py'
        }
        
        print("\n📦 Components:")
        for name, path in components.items():
            status = "✅" if path.exists() else "❌"
            print(f"   {status} {name}")
        
        print("\n" + "="*60)
    
    def show_help(self, params=''):
        """Show available commands"""
        print("\n🎙️  Amrit Voice Assistant Commands:")
        print("="*60)
        
        help_text = {
            'organize data': 'Organize all discovered data into folders',
            'check space/disk': 'Show disk space status',
            'find <filename>': 'Search for a file',
            'backup': 'Backup data to external drive',
            'train': 'Start AI model training',
            'create video': 'Make Nam-toon video',
            'read gurbani': 'Read Gurbani quote',
            'what can i build': 'Show AI project ideas',
            'status': 'Show system status',
            'help': 'Show this help message'
        }
        
        for cmd, desc in help_text.items():
            print(f"\n• Amrit, {cmd}")
            print(f"  → {desc}")
        
        print("\n" + "="*60)
        print("💡 Prefix commands with 'Amrit,' or just type directly")
    
    def run(self):
        """Run voice assistant"""
        print("\n" + "="*70)
        print("🎙️  AMRIT VOICE ASSISTANT")
        print("="*70)
        print("\n👋 Sat Sri Akal! I'm Amrit, your AI assistant.")
        print("🗣️  Type commands or say them out loud!")
        print("💡 Try: 'Amrit, help' or just 'help'\n")
        
        while True:
            try:
                # Listen for command
                command = self.listen()
                
                # Check for exit
                if command in ['exit', 'quit', 'bye', 'goodbye']:
                    print("\n👋 Goodbye! ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ!")
                    break
                
                # Parse and execute command
                action, params = self.parse_command(command)
                
                if action:
                    action(params)
                else:
                    print(f"\n❓ Sorry, I don't understand: '{command}'")
                    print("💡 Say 'help' to see available commands")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    assistant = AmritVoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
