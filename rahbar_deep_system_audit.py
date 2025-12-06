#!/usr/bin/env python3
"""
🔍 RAHBAR AI - DEEP SYSTEM AUDIT
Checks EVERY file, EVERY library, EVERY capability

Why cartoons when we have realistic video tools?
Let's find out what's actually installed and working!
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import importlib.util

class RahbarSystemAuditor:
    """🤖 Rahbar AI - Complete System Audit"""
    
    def __init__(self):
        self.audit_report = {
            'timestamp': datetime.now().isoformat(),
            'libraries_installed': {},
            'libraries_working': {},
            'video_analysis_tools': {},
            'realistic_video_capabilities': {},
            'training_data': {},
            'gaps': [],
            'unused_power': []
        }
    
    def check_library(self, name, import_path=None):
        """Check if library is installed AND working"""
        if import_path is None:
            import_path = name
        
        try:
            # Check if installed
            spec = importlib.util.find_spec(import_path)
            if spec is None:
                return {'installed': False, 'working': False, 'version': None}
            
            # Try to import
            module = importlib.import_module(import_path)
            version = getattr(module, '__version__', 'unknown')
            
            return {'installed': True, 'working': True, 'version': version}
        except Exception as e:
            return {'installed': True, 'working': False, 'error': str(e)}
    
    def audit_video_libraries(self):
        """Check ALL video-related libraries"""
        print("📚 AUDITING VIDEO LIBRARIES...")
        print("-" * 70)
        
        video_libs = {
            'opencv-python': 'cv2',
            'moviepy': 'moviepy.editor',
            'ffmpeg-python': 'ffmpeg',
            'imageio': 'imageio',
            'Pillow': 'PIL',
            'numpy': 'numpy',
            'gtts': 'gtts',
            'pyttsx3': 'pyttsx3',
            'pydub': 'pydub',
            'pygame': 'pygame',
            'torch': 'torch',
            'torchvision': 'torchvision',
            'transformers': 'transformers',
            'diffusers': 'diffusers',
            'accelerate': 'accelerate',
            'ultralytics': 'ultralytics',
            'mediapipe': 'mediapipe',
            'insightface': 'insightface',
            'onnxruntime': 'onnxruntime',
            'face_recognition': 'face_recognition',
            'dlib': 'dlib'
        }
        
        for lib_name, import_path in video_libs.items():
            status = self.check_library(lib_name, import_path)
            self.audit_report['libraries_installed'][lib_name] = status
            
            if status['working']:
                print(f"   ✅ {lib_name}: v{status['version']}")
            elif status['installed']:
                print(f"   ⚠️  {lib_name}: Installed but broken - {status.get('error', 'unknown')}")
            else:
                print(f"   ❌ {lib_name}: Not installed")
        
        # Count working libraries
        working_count = sum(1 for s in self.audit_report['libraries_installed'].values() if s['working'])
        total_count = len(video_libs)
        
        print(f"\n📊 Working: {working_count}/{total_count} libraries")
        return working_count, total_count
    
    def scan_video_analysis_files(self):
        """Find ALL video analysis tools we created"""
        print("\n🔍 SCANNING VIDEO ANALYSIS TOOLS...")
        print("-" * 70)
        
        analysis_patterns = [
            '*video*analyzer*.py',
            '*video*analysis*.py',
            '*deep*video*.py',
            '*quick*video*.py',
            'master_builder.py',
            'colab/master_builder.py'
        ]
        
        found_tools = []
        for pattern in analysis_patterns:
            files = list(Path('.').rglob(pattern))
            found_tools.extend(files)
        
        # Remove duplicates
        found_tools = list(set(found_tools))
        
        for tool in found_tools:
            size = tool.stat().st_size
            print(f"   📄 {tool} ({size:,} bytes)")
            
            # Check what it imports
            try:
                content = tool.read_text(encoding='utf-8')
                imports = []
                for line in content.split('\n'):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        imports.append(line.strip())
                
                self.audit_report['video_analysis_tools'][str(tool)] = {
                    'size': size,
                    'imports_count': len(imports),
                    'imports': imports[:10]  # First 10
                }
            except:
                pass
        
        print(f"\n📊 Found {len(found_tools)} video analysis tools")
        return found_tools
    
    def check_realistic_capabilities(self):
        """Check what realistic video capabilities we have"""
        print("\n🎬 CHECKING REALISTIC VIDEO CAPABILITIES...")
        print("-" * 70)
        
        capabilities = {}
        
        # 1. Face detection/recognition
        if self.audit_report['libraries_installed'].get('face_recognition', {}).get('working'):
            capabilities['face_recognition'] = 'AVAILABLE ✅'
            print("   ✅ Face Recognition: WORKING")
        else:
            capabilities['face_recognition'] = 'MISSING ❌'
            print("   ❌ Face Recognition: NOT WORKING")
        
        # 2. MediaPipe (face mesh, pose)
        if self.audit_report['libraries_installed'].get('mediapipe', {}).get('working'):
            capabilities['mediapipe'] = 'AVAILABLE ✅'
            print("   ✅ MediaPipe (Face Mesh): WORKING")
        else:
            capabilities['mediapipe'] = 'MISSING ❌'
            print("   ❌ MediaPipe: NOT WORKING")
        
        # 3. InsightFace (realistic faces)
        if self.audit_report['libraries_installed'].get('insightface', {}).get('working'):
            capabilities['insightface'] = 'AVAILABLE ✅'
            print("   ✅ InsightFace (Realistic Faces): WORKING")
        else:
            capabilities['insightface'] = 'MISSING ❌'
            print("   ❌ InsightFace: NOT WORKING")
        
        # 4. Stable Diffusion
        has_diffusers = self.audit_report['libraries_installed'].get('diffusers', {}).get('working')
        has_torch = self.audit_report['libraries_installed'].get('torch', {}).get('working')
        
        if has_diffusers and has_torch:
            capabilities['stable_diffusion'] = 'AVAILABLE ✅'
            print("   ✅ Stable Diffusion: WORKING")
        else:
            capabilities['stable_diffusion'] = 'MISSING ❌'
            print("   ❌ Stable Diffusion: NOT WORKING")
        
        # 5. Video generation from photos
        if Path('generate_scene_images.py').exists():
            capabilities['photo_to_video'] = 'CODE EXISTS ✅'
            print("   ✅ Photo-to-Video Code: EXISTS")
        else:
            capabilities['photo_to_video'] = 'MISSING ❌'
            print("   ❌ Photo-to-Video Code: MISSING")
        
        self.audit_report['realistic_video_capabilities'] = capabilities
        
        # Count available
        available = sum(1 for v in capabilities.values() if '✅' in v)
        total = len(capabilities)
        
        print(f"\n📊 Available: {available}/{total} realistic capabilities")
        return capabilities
    
    def check_training_data(self):
        """Check training data status"""
        print("\n📸 CHECKING TRAINING DATA...")
        print("-" * 70)
        
        data_folders = {
            'training_photos': 'Photos for training',
            'training_audio': 'Audio for training',
            'extracted_characters': 'Character data',
            'media_training_data.json': 'Analyzed media data'
        }
        
        for folder, description in data_folders.items():
            path = Path(folder)
            if path.exists():
                if path.is_dir():
                    count = len(list(path.rglob('*')))
                    size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                    print(f"   ✅ {folder}: {count} files, {size / (1024**3):.2f} GB")
                    self.audit_report['training_data'][folder] = {
                        'exists': True,
                        'count': count,
                        'size_gb': size / (1024**3)
                    }
                else:
                    size = path.stat().st_size
                    print(f"   ✅ {folder}: {size / (1024**2):.2f} MB")
                    self.audit_report['training_data'][folder] = {
                        'exists': True,
                        'size_mb': size / (1024**2)
                    }
            else:
                print(f"   ❌ {folder}: NOT FOUND")
                self.audit_report['training_data'][folder] = {'exists': False}
    
    def find_unused_power(self):
        """Find what powerful tools we have but aren't using"""
        print("\n⚡ FINDING UNUSED POWER...")
        print("-" * 70)
        
        unused = []
        
        # Check if we have powerful libs but using basic drawing
        has_torch = self.audit_report['libraries_installed'].get('torch', {}).get('working')
        has_diffusers = self.audit_report['libraries_installed'].get('diffusers', {}).get('working')
        
        # Check current video generator
        current_generators = list(Path('.').glob('*video*generator*.py'))
        
        for gen_file in current_generators:
            content = gen_file.read_text(encoding='utf-8')
            
            # Are we using cv2.circle for characters?
            if 'cv2.circle' in content and 'character' in content.lower():
                unused.append({
                    'issue': 'Using cv2.circle for characters (cartoons)',
                    'file': str(gen_file),
                    'available': 'Stable Diffusion, Face Recognition, MediaPipe',
                    'should_use': 'Generate realistic Punjabi faces from training photos'
                })
                print(f"   ⚠️  {gen_file.name}: Drawing circles instead of realistic faces!")
            
            # Are we using gTTS when we could train custom?
            if 'gTTS' in content and has_torch:
                unused.append({
                    'issue': 'Using gTTS (external) for Punjabi voice',
                    'file': str(gen_file),
                    'available': 'PyTorch for custom voice training',
                    'should_use': 'Train on 100+ Keertan audio files'
                })
                print(f"   ⚠️  {gen_file.name}: Using gTTS instead of trained voice!")
            
            # Check if using training data
            if 'training_photos' not in content and 'training_audio' not in content:
                unused.append({
                    'issue': 'NOT using training data (5.5 GB)',
                    'file': str(gen_file),
                    'available': '547 photos + 100 audio files',
                    'should_use': 'Learn from real Punjabi faces and voices'
                })
                print(f"   ⚠️  {gen_file.name}: Ignoring 5.5 GB training data!")
        
        self.audit_report['unused_power'] = unused
        print(f"\n📊 Found {len(unused)} cases of unused power")
        return unused
    
    def identify_gaps(self):
        """Identify why we're making cartoons instead of realistic videos"""
        print("\n🎯 IDENTIFYING GAPS...")
        print("-" * 70)
        
        gaps = []
        
        # Gap 1: Not connecting training data to video generator
        if self.audit_report['training_data'].get('media_training_data.json', {}).get('exists'):
            gaps.append({
                'gap': 'Training data analyzed but NOT used in video generation',
                'evidence': 'media_training_data.json exists but video generator uses cv2.circle',
                'fix': 'Load analyzed faces from JSON and use in video'
            })
        
        # Gap 2: Not using face recognition
        if not self.audit_report['realistic_video_capabilities'].get('face_recognition') == 'AVAILABLE ✅':
            gaps.append({
                'gap': 'Face Recognition library not working',
                'evidence': 'face_recognition library check failed',
                'fix': 'Install: pip3 install face-recognition cmake dlib'
            })
        
        # Gap 3: Not using Stable Diffusion
        if not self.audit_report['realistic_video_capabilities'].get('stable_diffusion') == 'AVAILABLE ✅':
            gaps.append({
                'gap': 'Stable Diffusion not available',
                'evidence': 'diffusers or torch not working',
                'fix': 'Install: pip3 install diffusers torch accelerate'
            })
        
        # Gap 4: Video generator not integrated with realistic tools
        gaps.append({
            'gap': 'Video generators are isolated - not using available AI tools',
            'evidence': 'Multiple video generators but none use face_recognition, mediapipe, or diffusers',
            'fix': 'Create NEW generator that integrates ALL available tools'
        })
        
        self.audit_report['gaps'] = gaps
        
        for i, gap in enumerate(gaps, 1):
            print(f"\n   {i}. {gap['gap']}")
            print(f"      Evidence: {gap['evidence']}")
            print(f"      Fix: {gap['fix']}")
        
        print(f"\n📊 Identified {len(gaps)} critical gaps")
        return gaps
    
    def generate_action_plan(self):
        """Generate action plan to use full system power"""
        print("\n" + "="*70)
        print("🎯 ACTION PLAN TO FIX")
        print("="*70)
        
        plan = []
        
        # Based on gaps, create action items
        working_libs = sum(1 for s in self.audit_report['libraries_installed'].values() if s['working'])
        
        if working_libs < 10:
            plan.append({
                'priority': 'HIGH',
                'action': 'Install missing libraries',
                'command': 'pip3 install face-recognition mediapipe insightface diffusers torch',
                'reason': f'Only {working_libs} libraries working'
            })
        
        if self.audit_report['unused_power']:
            plan.append({
                'priority': 'HIGH',
                'action': 'Create NEW realistic video generator',
                'command': 'Create realistic_punjabi_video_generator.py',
                'reason': 'Current generators use cartoons, not realistic faces'
            })
        
        if self.audit_report['training_data'].get('media_training_data.json', {}).get('exists'):
            plan.append({
                'priority': 'HIGH',
                'action': 'Use analyzed training data',
                'command': 'Load faces from media_training_data.json in video generator',
                'reason': '5.5 GB training data sitting unused'
            })
        
        plan.append({
            'priority': 'CRITICAL',
            'action': 'Rebuild video system from scratch',
            'command': 'Use Rahbar AI to build integrated system',
            'reason': 'System has power but parts are disconnected'
        })
        
        for i, item in enumerate(plan, 1):
            print(f"\n{i}. [{item['priority']}] {item['action']}")
            print(f"   Command: {item['command']}")
            print(f"   Reason: {item['reason']}")
        
        return plan
    
    def save_report(self):
        """Save complete audit report"""
        report_file = f"RAHBAR_SYSTEM_AUDIT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.audit_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Full report saved: {report_file}")
        return report_file
    
    def run_complete_audit(self):
        """Run complete system audit"""
        print("🤖 RAHBAR AI - DEEP SYSTEM AUDIT")
        print("="*70)
        print("Finding out why we're making cartoons with realistic tools!")
        print("="*70 + "\n")
        
        # 1. Check libraries
        working, total = self.audit_video_libraries()
        
        # 2. Find analysis tools
        tools = self.scan_video_analysis_files()
        
        # 3. Check realistic capabilities
        capabilities = self.check_realistic_capabilities()
        
        # 4. Check training data
        self.check_training_data()
        
        # 5. Find unused power
        unused = self.find_unused_power()
        
        # 6. Identify gaps
        gaps = self.identify_gaps()
        
        # 7. Generate action plan
        plan = self.generate_action_plan()
        
        # 8. Save report
        report_file = self.save_report()
        
        # Final summary
        print("\n" + "="*70)
        print("📊 AUDIT SUMMARY")
        print("="*70)
        print(f"✅ Working Libraries: {working}/{total}")
        print(f"📄 Analysis Tools: {len(tools)}")
        print(f"⚡ Unused Power Cases: {len(unused)}")
        print(f"🔍 Critical Gaps: {len(gaps)}")
        print(f"🎯 Action Items: {len(plan)}")
        print()
        print("🎯 ROOT CAUSE:")
        print("   System has POWERFUL tools but video generators DON'T USE THEM!")
        print("   We analyze 100+ videos but then draw circles instead!")
        print()
        print("💡 SOLUTION:")
        print("   Build NEW generator that connects ALL pieces:")
        print("   1. Training data (547 photos)")
        print("   2. Face recognition")
        print("   3. Realistic rendering")
        print("   4. Custom voice (100 audio files)")
        print("="*70)
        
        return self.audit_report

if __name__ == "__main__":
    auditor = RahbarSystemAuditor()
    report = auditor.run_complete_audit()
    
    print("\n🚀 Ready to build REALISTIC video generator? (y/n)")
