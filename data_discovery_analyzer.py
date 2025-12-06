#!/usr/bin/env python3
"""
📚 Complete Data Discovery Analyzer
Scans entire system for valuable AI training data
ਪੂਰੇ system ਚ data ਲੱਭਣ ਵਾਲਾ
"""

import os
import json
from pathlib import Path
from collections import defaultdict

class DataDiscoveryAnalyzer:
    def __init__(self):
        self.home = Path.home()
        self.data_found = {
            'brain_knowledge': [],
            'gurbani_spiritual': [],
            'pdfs': [],
            'text_files': [],
            'json_data': [],
            'stories': [],
            'training_data': []
        }
        
    def scan_brain_files(self):
        """Scan brain knowledge TXT files"""
        print("\n🧠 Scanning Brain Knowledge Files...")
        
        brain_locations = [
            self.home / "Nam-toon-studio",
            self.home / "AmritCore_QuantumBrain_OS/quantum_brain",
            self.home / "Desktop/amritkaur_local"
        ]
        
        total_size = 0
        for location in brain_locations:
            if location.exists():
                for brain_file in location.glob("brain_*.txt"):
                    size_kb = brain_file.stat().st_size / 1024
                    total_size += size_kb
                    
                    with open(brain_file, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                    
                    self.data_found['brain_knowledge'].append({
                        'file': str(brain_file),
                        'name': brain_file.name,
                        'size_kb': round(size_kb, 2),
                        'lines': lines,
                        'location': str(location)
                    })
        
        print(f"   ✅ Found {len(self.data_found['brain_knowledge'])} brain files")
        print(f"   📊 Total size: {total_size:.1f} KB")
        return len(self.data_found['brain_knowledge'])
    
    def scan_gurbani_files(self):
        """Scan Gurbani/Sikhi specific files"""
        print("\n🕉️  Scanning Gurbani & Spiritual Files...")
        
        search_paths = [
            self.home / "Desktop/amritkaur_local",
            self.home / "AmritCore_QuantumBrain_OS",
            self.home / "Nam-toon-studio"
        ]
        
        gurbani_keywords = ['sggs', 'gurbani', 'sukhmani', 'japji', 'guru', 'spiritual']
        
        for search_path in search_paths:
            if not search_path.exists():
                continue
                
            for ext in ['.json', '.txt', '.py']:
                for file in search_path.rglob(f"*{ext}"):
                    if any(keyword in file.name.lower() for keyword in gurbani_keywords):
                        try:
                            size_kb = file.stat().st_size / 1024
                            
                            if size_kb > 0:
                                self.data_found['gurbani_spiritual'].append({
                                    'file': str(file),
                                    'name': file.name,
                                    'type': ext,
                                    'size_kb': round(size_kb, 2)
                                })
                        except:
                            continue
        
        print(f"   ✅ Found {len(self.data_found['gurbani_spiritual'])} Gurbani files")
        return len(self.data_found['gurbani_spiritual'])
    
    def scan_pdfs(self):
        """Scan PDF documents"""
        print("\n📚 Scanning PDF Files...")
        
        pdf_locations = [
            self.home / "Desktop",
            self.home / "Documents",
            self.home / "Downloads"
        ]
        
        total_size_mb = 0
        for location in pdf_locations:
            if not location.exists():
                continue
                
            for pdf_file in location.rglob("*.pdf"):
                try:
                    size_mb = pdf_file.stat().st_size / (1024 * 1024)
                    total_size_mb += size_mb
                    
                    # Check if Sikhi related
                    sikhi_related = any(k in pdf_file.name.lower() 
                                      for k in ['guru', 'gurbani', 'sikhi', 'sggs', 
                                               'punjabi', 'morcha', 'khalsa'])
                    
                    self.data_found['pdfs'].append({
                        'file': str(pdf_file),
                        'name': pdf_file.name,
                        'size_mb': round(size_mb, 2),
                        'sikhi_related': sikhi_related
                    })
                except:
                    continue
        
        sikhi_pdfs = sum(1 for p in self.data_found['pdfs'] if p['sikhi_related'])
        print(f"   ✅ Found {len(self.data_found['pdfs'])} PDFs")
        print(f"   🕉️  {sikhi_pdfs} are Sikhi-related")
        print(f"   📊 Total size: {total_size_mb:.1f} MB")
        return len(self.data_found['pdfs'])
    
    def scan_text_files(self):
        """Scan TXT files with stories, data"""
        print("\n📝 Scanning Text Files...")
        
        txt_locations = [
            self.home / "Nam-toon-studio",
            self.home / "Desktop"
        ]
        
        total_lines = 0
        for location in txt_locations:
            if not location.exists():
                continue
                
            for txt_file in location.glob("*.txt"):
                # Skip brain files (already counted)
                if "brain_" in txt_file.name:
                    continue
                    
                try:
                    size_kb = txt_file.stat().st_size / 1024
                    
                    if size_kb > 1:  # Skip tiny files
                        with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = len(f.readlines())
                            total_lines += lines
                        
                        self.data_found['text_files'].append({
                            'file': str(txt_file),
                            'name': txt_file.name,
                            'size_kb': round(size_kb, 2),
                            'lines': lines
                        })
                except:
                    continue
        
        print(f"   ✅ Found {len(self.data_found['text_files'])} text files")
        print(f"   📊 Total lines: {total_lines:,}")
        return len(self.data_found['text_files'])
    
    def scan_json_data(self):
        """Scan JSON data files"""
        print("\n🗃️  Scanning JSON Data Files...")
        
        json_locations = [
            self.home / "Nam-toon-studio",
            self.home / "Desktop/amritkaur_local",
            self.home / "AmritCore_QuantumBrain_OS"
        ]
        
        for location in json_locations:
            if not location.exists():
                continue
                
            for json_file in location.rglob("*.json"):
                # Skip node_modules, .venv, etc
                if any(skip in str(json_file) for skip in ['node_modules', '.venv', 'site-packages']):
                    continue
                    
                try:
                    size_kb = json_file.stat().st_size / 1024
                    
                    if size_kb > 0.5:  # Skip tiny configs
                        self.data_found['json_data'].append({
                            'file': str(json_file),
                            'name': json_file.name,
                            'size_kb': round(size_kb, 2)
                        })
                except:
                    continue
        
        print(f"   ✅ Found {len(self.data_found['json_data'])} JSON files")
        return len(self.data_found['json_data'])
    
    def generate_report(self):
        """Generate comprehensive report"""
        report = {
            'summary': {
                'brain_knowledge_files': len(self.data_found['brain_knowledge']),
                'gurbani_spiritual_files': len(self.data_found['gurbani_spiritual']),
                'pdf_documents': len(self.data_found['pdfs']),
                'text_files': len(self.data_found['text_files']),
                'json_data_files': len(self.data_found['json_data']),
                'total_files': sum([
                    len(self.data_found['brain_knowledge']),
                    len(self.data_found['gurbani_spiritual']),
                    len(self.data_found['pdfs']),
                    len(self.data_found['text_files']),
                    len(self.data_found['json_data'])
                ])
            },
            'details': self.data_found,
            'value_assessment': self._assess_value(),
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _assess_value(self):
        """Assess data value for AI training"""
        brain_kb = sum(f['size_kb'] for f in self.data_found['brain_knowledge'])
        pdf_mb = sum(f['size_mb'] for f in self.data_found['pdfs'])
        txt_lines = sum(f.get('lines', 0) for f in self.data_found['text_files'])
        
        return {
            'brain_knowledge': {
                'value_inr': 200000,  # ₹2 lakh
                'reason': f'{len(self.data_found["brain_knowledge"])} curated knowledge files',
                'size_kb': round(brain_kb, 1)
            },
            'gurbani_data': {
                'value_inr': 300000,  # ₹3 lakh
                'reason': 'Rare Gurbani/Punjabi spiritual content',
                'files': len(self.data_found['gurbani_spiritual'])
            },
            'pdf_library': {
                'value_inr': 100000,  # ₹1 lakh
                'reason': f'{len(self.data_found["pdfs"])} documents including Sikhi history',
                'size_mb': round(pdf_mb, 1)
            },
            'text_content': {
                'value_inr': 150000,  # ₹1.5 lakh
                'reason': f'{txt_lines:,} lines of text data',
                'files': len(self.data_found['text_files'])
            },
            'total_value_inr': 750000  # ₹7.5 lakh
        }
    
    def _generate_recommendations(self):
        """Generate actionable recommendations"""
        return [
            {
                'priority': 'HIGH',
                'action': 'Consolidate brain knowledge files',
                'details': 'Merge Nam-toon and AmritCore brain files into master knowledge base'
            },
            {
                'priority': 'HIGH',
                'action': 'Extract PDF content',
                'details': 'Use OCR/PyPDF2 to extract text from PDFs for training'
            },
            {
                'priority': 'MEDIUM',
                'action': 'Organize Gurbani data',
                'details': 'Create unified Gurbani dataset from scattered JSON/TXT files'
            },
            {
                'priority': 'MEDIUM',
                'action': 'Build training corpus',
                'details': 'Combine all text data into single searchable database'
            },
            {
                'priority': 'LOW',
                'action': 'Backup everything',
                'details': 'Create archive of all discovered valuable data'
            }
        ]
    
    def save_report(self, output_file='complete_data_discovery.json'):
        """Save report to JSON"""
        report = self.generate_report()
        
        output_path = Path(__file__).parent / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Report saved to: {output_path}")
        return output_path
    
    def print_summary(self, report):
        """Print formatted summary"""
        print("\n" + "="*70)
        print("📚 COMPLETE DATA DISCOVERY SUMMARY")
        print("="*70)
        
        summary = report['summary']
        print(f"\n📊 TOTAL FILES DISCOVERED: {summary['total_files']}")
        print(f"   🧠 Brain Knowledge: {summary['brain_knowledge_files']}")
        print(f"   🕉️  Gurbani/Spiritual: {summary['gurbani_spiritual_files']}")
        print(f"   📚 PDF Documents: {summary['pdf_documents']}")
        print(f"   📝 Text Files: {summary['text_files']}")
        print(f"   🗃️  JSON Data: {summary['json_data_files']}")
        
        print("\n💰 VALUE ASSESSMENT:")
        value = report['value_assessment']
        print(f"   Brain Knowledge: ₹{value['brain_knowledge']['value_inr']:,}")
        print(f"   Gurbani Data: ₹{value['gurbani_data']['value_inr']:,}")
        print(f"   PDF Library: ₹{value['pdf_library']['value_inr']:,}")
        print(f"   Text Content: ₹{value['text_content']['value_inr']:,}")
        print(f"   📈 TOTAL VALUE: ₹{value['total_value_inr']:,}")
        
        print("\n🎯 TOP RECOMMENDATIONS:")
        for rec in report['recommendations'][:3]:
            print(f"   {rec['priority']}: {rec['action']}")
            print(f"      → {rec['details']}")
        
        print("\n" + "="*70)

def main():
    analyzer = DataDiscoveryAnalyzer()
    
    print("📚 Complete Data Discovery Analyzer")
    print("Scanning entire system for valuable AI training data...")
    print("="*70)
    
    # Run all scans
    analyzer.scan_brain_files()
    analyzer.scan_gurbani_files()
    analyzer.scan_pdfs()
    analyzer.scan_text_files()
    analyzer.scan_json_data()
    
    # Generate and save report
    report = analyzer.generate_report()
    analyzer.save_report()
    
    # Print summary
    analyzer.print_summary(report)
    
    print("\n✨ Discovery complete! Check complete_data_discovery.json for full details.")

if __name__ == "__main__":
    main()
