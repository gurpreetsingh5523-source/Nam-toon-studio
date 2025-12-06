#!/usr/bin/env python3
"""
🎵 Audio Library Analyzer - Kirtan & Music Value Assessment
Scans audio files across the system and analyzes their value for AI training.
"""

import os
import json
import subprocess
from pathlib import Path
from collections import defaultdict

class AudioLibraryAnalyzer:
    def __init__(self):
        self.audio_locations = {
            'gurbani_keertan_desktop': '~/Desktop/gurbani keertan',
            'gurbani_keertan_amritkaur': '~/Desktop/amritkaur_local/gurbani_keertan',
            'test_nano_audio': '~/Desktop/amritkaur_local/test_nano_audio',
            'nam_toon_audio': '~/Desktop/Nam-toon-studio/audio',
            'music_library': '~/Music',
            'downloads': '~/Downloads'
        }
        self.audio_extensions = ['.mp3', '.m4a', '.wav', '.m4r', '.aac', '.flac']
        
    def scan_folder(self, folder_name, folder_path):
        """Scan a specific folder for audio files"""
        expanded_path = os.path.expanduser(folder_path)
        
        if not os.path.exists(expanded_path):
            return None
            
        result = {
            'folder': folder_name,
            'path': folder_path,
            'files': [],
            'total_count': 0,
            'total_size_mb': 0,
            'by_format': defaultdict(int),
            'sample_files': []
        }
        
        try:
            for root, dirs, files in os.walk(expanded_path):
                for file in files:
                    file_path = Path(root) / file
                    ext = file_path.suffix.lower()
                    
                    if ext in self.audio_extensions:
                        try:
                            size_mb = file_path.stat().st_size / (1024 * 1024)
                            result['files'].append({
                                'name': file,
                                'size_mb': round(size_mb, 2),
                                'format': ext,
                                'relative_path': str(file_path.relative_to(expanded_path))
                            })
                            result['total_size_mb'] += size_mb
                            result['by_format'][ext] += 1
                            
                            # Keep first 10 as samples
                            if len(result['sample_files']) < 10:
                                result['sample_files'].append(file)
                        except Exception as e:
                            continue
            
            result['total_count'] = len(result['files'])
            result['total_size_mb'] = round(result['total_size_mb'], 2)
            result['by_format'] = dict(result['by_format'])
            
            return result if result['total_count'] > 0 else None
            
        except Exception as e:
            print(f"❌ Error scanning {folder_name}: {e}")
            return None
    
    def categorize_kirtan_files(self, files):
        """Categorize files into Kirtan, Raag, Path, etc."""
        categories = {
            'gurbani_kirtan': [],
            'raag_kirtan': [],
            'path_paath': [],
            'simran': [],
            'dhadi_vaaran': [],
            'other': []
        }
        
        kirtan_keywords = ['kirtan', 'keertan', 'satguru', 'gur', 'har', 'vaheguru']
        raag_keywords = ['raag', 'bilaskhani', 'bhairavi', 'chandrakouns']
        path_keywords = ['path', 'paath', 'anand sahib', 'sukhmani', 'japji']
        simran_keywords = ['simran', 'naam', 'waheguru']
        
        for file_info in files:
            filename = file_info['name'].lower()
            
            if any(k in filename for k in raag_keywords):
                categories['raag_kirtan'].append(file_info)
            elif any(k in filename for k in path_keywords):
                categories['path_paath'].append(file_info)
            elif any(k in filename for k in simran_keywords):
                categories['simran'].append(file_info)
            elif any(k in filename for k in kirtan_keywords):
                categories['gurbani_kirtan'].append(file_info)
            else:
                categories['other'].append(file_info)
        
        return {k: v for k, v in categories.items() if v}
    
    def analyze_all(self):
        """Scan all audio locations and generate comprehensive report"""
        results = {}
        total_files = 0
        total_size_mb = 0
        
        print("🎵 Scanning Audio Libraries...")
        print("=" * 60)
        
        for folder_name, folder_path in self.audio_locations.items():
            print(f"\n📁 Checking {folder_name}...")
            result = self.scan_folder(folder_name, folder_path)
            
            if result:
                results[folder_name] = result
                total_files += result['total_count']
                total_size_mb += result['total_size_mb']
                print(f"   ✅ Found {result['total_count']} files ({result['total_size_mb']} MB)")
            else:
                print(f"   ⚠️  No audio files or folder not found")
        
        # Analyze Gurbani Kirtan specifically
        gurbani_files = []
        if 'gurbani_keertan_desktop' in results:
            gurbani_files.extend(results['gurbani_keertan_desktop']['files'])
        if 'gurbani_keertan_amritkaur' in results:
            gurbani_files.extend(results['gurbani_keertan_amritkaur']['files'])
        
        categorized_kirtan = self.categorize_kirtan_files(gurbani_files) if gurbani_files else {}
        
        # Generate recommendations
        recommendations = self.generate_recommendations(results, categorized_kirtan)
        
        report = {
            'summary': {
                'total_audio_files': total_files,
                'total_size_mb': round(total_size_mb, 2),
                'total_size_gb': round(total_size_mb / 1024, 2),
                'locations_scanned': len(self.audio_locations),
                'locations_with_files': len(results)
            },
            'by_location': results,
            'gurbani_kirtan_analysis': {
                'total_kirtan_files': len(gurbani_files),
                'categorized': categorized_kirtan
            },
            'recommendations': recommendations
        }
        
        return report
    
    def generate_recommendations(self, results, categorized_kirtan):
        """Generate AI training and usage recommendations"""
        recommendations = {
            'voice_ai_training': {
                'suitable_files': [],
                'estimated_training_hours': 0,
                'use_cases': [
                    'Punjabi voice synthesis (Gurbani pronunciation)',
                    'Kirtan singing voice models',
                    'Accent and intonation training',
                    'Raag recognition and classification'
                ]
            },
            'background_music': {
                'suitable_files': [],
                'use_cases': [
                    'Nam-toon video background music',
                    'Meditation/spiritual app background',
                    'Cultural content soundtracks'
                ]
            },
            'speech_recognition': {
                'suitable_files': [],
                'use_cases': [
                    'Punjabi speech-to-text training',
                    'Gurbani word recognition',
                    'Multilingual ASR models'
                ]
            },
            'estimated_value': {
                'currency': 'INR',
                'training_data_value': 500000,  # ₹5 lakh for voice training
                'licensing_value': 200000,  # ₹2 lakh for commercial use
                'total_value': 700000,
                'explanation': 'Authentic Gurbani Kirtan is rare training data for AI'
            },
            'next_steps': [
                '1. Export high-quality kirtan files for voice AI training',
                '2. Create metadata with lyrics/raag information',
                '3. Organize by singer, raag, and length',
                '4. Use for Punjabi TTS (Text-to-Speech) model',
                '5. Background music for Nam-toon Studio videos'
            ]
        }
        
        # Calculate training hours (assuming avg 5 min per kirtan)
        if categorized_kirtan:
            total_kirtan = sum(len(v) for v in categorized_kirtan.values())
            recommendations['voice_ai_training']['estimated_training_hours'] = round(total_kirtan * 5 / 60, 2)
        
        return recommendations
    
    def save_report(self, report, output_file='audio_library_analysis.json'):
        """Save report to JSON file"""
        output_path = Path(__file__).parent / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Report saved to: {output_path}")
        return output_path
    
    def print_summary(self, report):
        """Print formatted summary"""
        print("\n" + "="*60)
        print("🎵 AUDIO LIBRARY ANALYSIS SUMMARY")
        print("="*60)
        
        summary = report['summary']
        print(f"\n📊 Total Audio Files: {summary['total_audio_files']}")
        print(f"💾 Total Size: {summary['total_size_gb']:.2f} GB ({summary['total_size_mb']:.2f} MB)")
        print(f"📁 Locations with Files: {summary['locations_with_files']}/{summary['locations_scanned']}")
        
        print("\n🎼 BY LOCATION:")
        for location, data in report['by_location'].items():
            print(f"\n  📂 {location}")
            print(f"     Files: {data['total_count']}")
            print(f"     Size: {data['total_size_mb']} MB")
            print(f"     Formats: {', '.join(data['by_format'].keys())}")
            if data['sample_files']:
                print(f"     Samples: {', '.join(data['sample_files'][:3])}...")
        
        if report['gurbani_kirtan_analysis']['total_kirtan_files'] > 0:
            print("\n🕉️  GURBANI KIRTAN ANALYSIS:")
            kirtan_analysis = report['gurbani_kirtan_analysis']
            print(f"   Total Kirtan Files: {kirtan_analysis['total_kirtan_files']}")
            
            if kirtan_analysis['categorized']:
                print("\n   Categories:")
                for category, files in kirtan_analysis['categorized'].items():
                    print(f"     • {category}: {len(files)} files")
        
        print("\n💰 ESTIMATED VALUE:")
        value = report['recommendations']['estimated_value']
        print(f"   Training Data Value: ₹{value['training_data_value']:,}")
        print(f"   Licensing Value: ₹{value['licensing_value']:,}")
        print(f"   Total Value: ₹{value['total_value']:,}")
        
        print("\n🎯 TOP USE CASES:")
        for use_case in report['recommendations']['voice_ai_training']['use_cases']:
            print(f"   • {use_case}")
        
        print("\n📝 NEXT STEPS:")
        for step in report['recommendations']['next_steps']:
            print(f"   {step}")
        
        print("\n" + "="*60)

def main():
    analyzer = AudioLibraryAnalyzer()
    
    print("🎵 Audio Library Analyzer for Nam-toon Studio")
    print("Analyzing Gurbani Kirtan, Music, and Audio Files...\n")
    
    # Run analysis
    report = analyzer.analyze_all()
    
    # Save report
    analyzer.save_report(report)
    
    # Print summary
    analyzer.print_summary(report)
    
    print("\n✨ Analysis complete! Check audio_library_analysis.json for full details.")

if __name__ == "__main__":
    main()
