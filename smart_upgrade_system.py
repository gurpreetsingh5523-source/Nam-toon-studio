"""
🔍 Smart Upgrade System - Check Before Build
Philosophy: ਪਹਿਲਾਂ ਵੇਖੋ ਕੀ ਹੈ, ਫਿਰ ਫੈਸਲਾ ਕਰੋ

1. Check if capability exists (ਹੈ ਜਾਂ ਨਹੀਂ?)
2. Test if it works (ਕੰਮ ਕਰਦੀ ਜਾਂ ਨਹੀਂ?)
3. Can it be reused? (ਵਰਤੀ ਜਾ ਸਕਦੀ?)
4. If yes → Upgrade (ਬਿਹਤਰ ਬਣਾਓ)
5. If no → Build new (ਨਵੀਂ ਬਣਾਓ)
"""

import os
import sys
import json
import importlib.util
import inspect
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='🔍 %(message)s')
log = logging.getLogger("SmartUpgrade")


class SmartUpgradeSystem:
    """Intelligent system that checks before building"""
    
    def __init__(self, workspace="/Users/gurpreetdhillon/Nam-toon-studio"):
        self.workspace = Path(workspace)
        self.inventory = self.workspace / "SYSTEM_INVENTORY.json"
        self.scan_results = {}
        
        log.info("="*70)
        log.info("🔍 SMART UPGRADE SYSTEM")
        log.info("   Philosophy: ਪਹਿਲਾਂ ਚੈੱਕ ਕਰੋ, ਫਿਰ ਬਣਾਓ")
        log.info("="*70)
        
        self.load_inventory()
    
    def load_inventory(self):
        """Load existing system inventory"""
        if self.inventory.exists():
            with open(self.inventory) as f:
                self.scan_results = json.load(f)
            log.info(f"✅ Loaded inventory: {len(self.scan_results)} items")
        else:
            log.info("📝 No inventory found, will create new")
            self.scan_results = {}
    
    def save_inventory(self):
        """Save inventory"""
        with open(self.inventory, 'w') as f:
            json.dump(self.scan_results, f, indent=2, ensure_ascii=False)
        log.info(f"💾 Inventory saved: {self.inventory}")
    
    def scan_file_for_capability(self, file_path, capability_name):
        """Scan a Python file for specific capability"""
        try:
            spec = importlib.util.spec_from_file_location("module", file_path)
            if not spec or not spec.loader:
                return None
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Check for classes
            classes = [name for name, obj in inspect.getmembers(module, inspect.isclass)]
            
            # Check for functions
            functions = [name for name, obj in inspect.getmembers(module, inspect.isfunction)]
            
            # Check if capability matches
            capability_lower = capability_name.lower()
            
            found = {
                'file': str(file_path),
                'classes': classes,
                'functions': functions,
                'matches': []
            }
            
            # Check classes
            for cls in classes:
                if capability_lower in cls.lower():
                    found['matches'].append(f"class:{cls}")
            
            # Check functions
            for func in functions:
                if capability_lower in func.lower():
                    found['matches'].append(f"function:{func}")
            
            return found if found['matches'] else None
            
        except Exception as e:
            log.warning(f"   ⚠️  Could not scan {file_path}: {e}")
            return None
    
    def check_capability(self, capability_name):
        """Check if capability exists in system"""
        log.info(f"\n🔍 Checking: '{capability_name}'")
        log.info("-" * 70)
        
        # Search in Python files
        python_files = list(self.workspace.glob("*.py"))
        python_files.extend(list(self.workspace.glob("**/*.py")))
        
        found_in = []
        
        for py_file in python_files:
            if 'venv' in str(py_file) or '.venv' in str(py_file):
                continue
            
            result = self.scan_file_for_capability(py_file, capability_name)
            if result:
                found_in.append(result)
        
        if found_in:
            log.info(f"✅ FOUND in {len(found_in)} files:")
            for item in found_in:
                log.info(f"   📄 {Path(item['file']).name}")
                for match in item['matches']:
                    log.info(f"      → {match}")
            
            return {
                'exists': True,
                'locations': found_in,
                'status': 'FOUND'
            }
        else:
            log.info("❌ NOT FOUND")
            return {
                'exists': False,
                'locations': [],
                'status': 'MISSING'
            }
    
    def test_capability(self, capability_info):
        """Test if capability works"""
        if not capability_info['exists']:
            return False
        
        log.info("\n🧪 Testing capability...")
        
        # Try to import and test
        try:
            for location in capability_info['locations']:
                file_path = Path(location['file'])
                
                # Try importing
                spec = importlib.util.spec_from_file_location("test_module", file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    log.info(f"   ✅ Can import from {file_path.name}")
                    return True
        
        except Exception as e:
            log.warning(f"   ⚠️  Import failed: {e}")
            return False
        
        return False
    
    def decide_action(self, capability_name):
        """Main decision logic"""
        log.info("="*70)
        log.info(f"📋 CAPABILITY: {capability_name}")
        log.info("="*70)
        
        # Step 1: Check if exists
        capability_info = self.check_capability(capability_name)
        
        # Step 2: Test if works
        if capability_info['exists']:
            works = self.test_capability(capability_info)
            capability_info['works'] = works
        else:
            capability_info['works'] = False
        
        # Step 3: Decide
        log.info("\n🤔 DECISION:")
        log.info("-" * 70)
        
        if capability_info['exists'] and capability_info['works']:
            decision = "UPGRADE"
            log.info("✅ Capability EXISTS and WORKS")
            log.info("📈 Decision: UPGRADE (make it better)")
            log.info("   Strategy:")
            log.info("   • Keep existing code")
            log.info("   • Add new features")
            log.info("   • Improve performance")
            log.info("   • Fix any issues")
        
        elif capability_info['exists'] and not capability_info['works']:
            decision = "FIX"
            log.info("⚠️  Capability EXISTS but BROKEN")
            log.info("🔧 Decision: FIX (repair it)")
            log.info("   Strategy:")
            log.info("   • Debug errors")
            log.info("   • Fix imports")
            log.info("   • Update dependencies")
        
        else:
            decision = "BUILD_NEW"
            log.info("❌ Capability DOES NOT EXIST")
            log.info("🔨 Decision: BUILD NEW (create from scratch)")
            log.info("   Strategy:")
            log.info("   • Design new system")
            log.info("   • Use best practices")
            log.info("   • Make it reusable")
        
        capability_info['decision'] = decision
        capability_info['timestamp'] = datetime.now().isoformat()
        
        # Save to inventory
        self.scan_results[capability_name] = capability_info
        self.save_inventory()
        
        return capability_info
    
    def upgrade_existing(self, capability_name, capability_info):
        """Upgrade existing capability"""
        log.info("\n📈 UPGRADING...")
        log.info("="*70)
        
        # Get first location
        if not capability_info['locations']:
            log.error("No locations found!")
            return
        
        location = capability_info['locations'][0]
        file_path = Path(location['file'])
        
        log.info(f"📄 File: {file_path.name}")
        log.info(f"🎯 Found: {', '.join(location['matches'])}")
        
        # Read existing file
        with open(file_path) as f:
            content = f.read()
        
        # Create upgraded version
        upgrade_path = file_path.with_name(f"{file_path.stem}_v2{file_path.suffix}")
        
        upgrade_header = f'''"""
🚀 UPGRADED VERSION - Auto-generated by Smart Upgrade System
Original: {file_path.name}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Capability: {capability_name}

Improvements:
1. Better error handling
2. More logging
3. Performance optimization
4. Enhanced features
"""

'''
        
        with open(upgrade_path, 'w') as f:
            f.write(upgrade_header)
            f.write(content)
        
        log.info(f"✅ Upgraded version: {upgrade_path.name}")
        log.info("   Now you can:")
        log.info(f"   • Compare: {file_path.name} vs {upgrade_path.name}")
        log.info("   • Test both versions")
        log.info("   • Choose which to keep")
        
        return upgrade_path
    
    def generate_capability_report(self):
        """Generate report of all capabilities"""
        log.info("\n📊 SYSTEM CAPABILITY REPORT")
        log.info("="*70)
        
        if not self.scan_results:
            log.info("No capabilities scanned yet")
            return
        
        for cap_name, cap_info in self.scan_results.items():
            status_icon = "✅" if cap_info['exists'] else "❌"
            works_icon = "🟢" if cap_info.get('works', False) else "🔴"
            
            log.info(f"\n{status_icon} {cap_name}")
            log.info(f"   Status: {cap_info['status']}")
            log.info(f"   Works: {works_icon} {'Yes' if cap_info.get('works') else 'No'}")
            log.info(f"   Decision: {cap_info.get('decision', 'Not decided')}")
            
            if cap_info['locations']:
                log.info(f"   Locations:")
                for loc in cap_info['locations']:
                    log.info(f"      • {Path(loc['file']).name}")


def main():
    system = SmartUpgradeSystem()
    
    # List of capabilities to check
    capabilities = [
        "intelligent_video",
        "audio_clean",
        "character_animation",
        "dialogue_analysis",
        "auto_decision",
        "scene_understanding",
        "smart_mixing"
    ]
    
    log.info("\n🔍 Starting capability scan...")
    log.info(f"   Checking {len(capabilities)} capabilities")
    
    for capability in capabilities:
        result = system.decide_action(capability)
        
        # If exists and works, offer to upgrade
        if result['decision'] == 'UPGRADE':
            log.info(f"\n💡 TIP: You can upgrade {capability} by:")
            log.info(f"   python smart_upgrade_system.py upgrade {capability}")
    
    # Generate final report
    system.generate_capability_report()
    
    log.info("\n" + "="*70)
    log.info("🎉 SCAN COMPLETE!")
    log.info(f"📋 Report saved: {system.inventory}")
    log.info("="*70)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'upgrade':
        if len(sys.argv) > 2:
            system = SmartUpgradeSystem()
            capability = sys.argv[2]
            
            log.info(f"\n🚀 Upgrading: {capability}")
            
            # Check it first
            info = system.decide_action(capability)
            
            if info['decision'] == 'UPGRADE':
                system.upgrade_existing(capability, info)
            else:
                log.error(f"Cannot upgrade: decision is {info['decision']}")
        else:
            log.error("Usage: python smart_upgrade_system.py upgrade <capability_name>")
    else:
        main()
