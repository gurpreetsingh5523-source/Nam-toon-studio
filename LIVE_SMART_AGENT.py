#!/usr/bin/env python3
"""
🔴 LIVE CONTINUOUS SMART AGENT
Real-time updates, auto-start, smart upgrading, new logic discovery

Features:
- Live terminal updates (you can see what's happening)
- Auto-start on laptop boot
- Smart upgrading with new logic discovery
- Interactive progress display
"""

import os
import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

WORKSPACE = Path("/Users/gurpreetdhillon/Nam-toon-studio")
sys.path.insert(0, str(WORKSPACE))

# Live console logging
logging.basicConfig(
    level=logging.INFO,
    format='🔴 [%(asctime)s] %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(WORKSPACE / "live_agent.log")
    ]
)
log = logging.getLogger(__name__)


class LiveSmartAgent:
    """Live agent with real-time updates"""
    
    def __init__(self):
        self.workspace = WORKSPACE
        self.running = False
        self.cycle = 0
        
        # Stats
        self.discoveries = []
        self.upgrades = []
        self.fixes = []
        
        self.clear_screen()
        self.print_banner()
    
    def clear_screen(self):
        """Clear terminal"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_banner(self):
        """Print live banner"""
        print("\n" + "="*70)
        print("🔴 LIVE CONTINUOUS SMART AGENT")
        print("   Real-time Updates • Auto-Start • Smart Upgrading")
        print("="*70)
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Workspace: {self.workspace}")
        print("="*70 + "\n")
    
    def print_status(self):
        """Print live status"""
        print(f"\r🔄 Cycle #{self.cycle} | "
              f"🔍 Discoveries: {len(self.discoveries)} | "
              f"⬆️  Upgrades: {len(self.upgrades)} | "
              f"🔧 Fixes: {len(self.fixes)}", end='', flush=True)
    
    def discover_new_logic(self):
        """Discover new logic patterns in code"""
        log.info("\n🔍 DISCOVERING NEW LOGIC...")
        
        # Scan Python files for patterns
        py_files = list(self.workspace.glob("*.py"))
        
        new_patterns = []
        
        for py_file in py_files[:10]:  # Sample
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Look for new patterns
                    if 'class' in content and py_file.stem not in [d['file'] for d in self.discoveries]:
                        classes = content.count('class ')
                        if classes > 0:
                            new_patterns.append({
                                'type': 'class_pattern',
                                'file': py_file.stem,
                                'count': classes,
                                'timestamp': datetime.now().isoformat()
                            })
                            log.info(f"   ✨ Found {classes} classes in {py_file.name}")
            
            except Exception as e:
                pass
        
        self.discoveries.extend(new_patterns)
        log.info(f"   ✅ Discovered {len(new_patterns)} new patterns")
        
        return new_patterns
    
    def smart_upgrade(self):
        """Smart upgrade based on discoveries"""
        log.info("\n⬆️  SMART UPGRADING...")
        
        # Load systems
        try:
            from MASTER_BRAIN_SUPREME import MasterBrainSupreme
            master = MasterBrainSupreme()
            
            # Upgrade
            result = master.execute_command('upgrade_self')
            
            self.upgrades.append({
                'type': 'master_brain',
                'result': str(result),
                'timestamp': datetime.now().isoformat()
            })
            
            log.info(f"   ✅ {result}")
            return True
        
        except Exception as e:
            log.error(f"   ❌ Upgrade failed: {e}")
            return False
    
    def auto_fix(self):
        """Auto-fix issues"""
        log.info("\n🔧 AUTO-FIXING...")
        
        try:
            from MASTER_AGENT_CONTROLLER import MasterAgentController
            controller = MasterAgentController(str(self.workspace))
            
            # Run agents
            fixed = 0
            for agent_name in list(controller.agents.keys())[:2]:  # Run 2 agents
                if controller.agent_status.get(agent_name, {}).get('enabled', False):
                    controller.run_agent_cycle(agent_name)
                    errors_fixed = controller.agent_status[agent_name].get('errors_fixed', 0)
                    if errors_fixed > 0:
                        fixed += errors_fixed
                        log.info(f"   ✅ {agent_name}: {errors_fixed} fixes")
            
            if fixed > 0:
                self.fixes.append({
                    'count': fixed,
                    'timestamp': datetime.now().isoformat()
                })
            
            return fixed
        
        except Exception as e:
            log.error(f"   ❌ Auto-fix failed: {e}")
            return 0
    
    def run_live_cycle(self):
        """Run one live cycle"""
        self.cycle += 1
        
        log.info("\n" + "="*70)
        log.info(f"🔄 CYCLE #{self.cycle}")
        log.info(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
        log.info("="*70)
        
        # Task 1: Discover new logic
        patterns = self.discover_new_logic()
        
        # Task 2: Smart upgrade (every 5 cycles)
        if self.cycle % 5 == 0:
            self.smart_upgrade()
        
        # Task 3: Auto-fix
        fixed = self.auto_fix()
        
        # Update live status
        self.print_status()
        
        # Save progress
        self.save_progress()
        
        log.info("\n" + "="*70)
        log.info(f"✅ CYCLE #{self.cycle} COMPLETE")
        log.info("="*70)
    
    def save_progress(self):
        """Save progress to file"""
        progress = {
            'cycle': self.cycle,
            'discoveries': len(self.discoveries),
            'upgrades': len(self.upgrades),
            'fixes': sum(f['count'] for f in self.fixes),
            'last_update': datetime.now().isoformat()
        }
        
        with open(self.workspace / "live_progress.json", 'w') as f:
            json.dump(progress, f, indent=2)
    
    def start(self):
        """Start live agent"""
        self.running = True
        
        log.info("\n🚀 STARTING LIVE AGENT")
        log.info("   Press Ctrl+C to stop\n")
        
        try:
            while self.running:
                self.run_live_cycle()
                
                # Wait 5 minutes
                log.info("\n💤 Sleeping 5 minutes...\n")
                for i in range(300):  # 5 minutes = 300 seconds
                    time.sleep(1)
                    if i % 30 == 0:  # Update every 30 seconds
                        remaining = (300 - i) // 60
                        print(f"\r⏱️  Next cycle in {remaining}m {(300-i)%60}s   ", end='', flush=True)
        
        except KeyboardInterrupt:
            log.info("\n\n⏹️  Stopped by user")
            self.stop()
    
    def stop(self):
        """Stop agent"""
        self.running = False
        
        log.info("\n" + "="*70)
        log.info("📊 FINAL STATS")
        log.info("="*70)
        log.info(f"🔄 Total Cycles: {self.cycle}")
        log.info(f"🔍 Discoveries: {len(self.discoveries)}")
        log.info(f"⬆️  Upgrades: {len(self.upgrades)}")
        log.info(f"🔧 Total Fixes: {sum(f['count'] for f in self.fixes)}")
        log.info("="*70 + "\n")


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║           🔴 LIVE CONTINUOUS SMART AGENT                          ║
║           ਸਿੱਧੇ ਦਿੱਖਣ ਵਾਲੇ Updates                                ║
║                                                                   ║
║   Features:                                                       ║
║   • Live terminal updates (see what's happening)                  ║
║   • Smart logic discovery                                         ║
║   • Auto-upgrading every 5 cycles                                 ║
║   • Auto-fixing errors                                            ║
║   • Runs every 5 minutes                                          ║
║                                                                   ║
║   Press Ctrl+C to stop                                            ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    agent = LiveSmartAgent()
    agent.start()


if __name__ == "__main__":
    main()
