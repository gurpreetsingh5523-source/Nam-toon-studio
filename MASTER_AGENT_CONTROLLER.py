#!/usr/bin/env python3
"""
🤖 MASTER AGENT CONTROLLER
ਸਾਰੇ agents ਨੂੰ auto mode ਤੇ ਚਲਾਉਣ ਵਾਲਾ master system

Responsibilities:
1. Auto-detect all agents
2. Auto-fix errors
3. Auto-update/upgrade
4. Auto-evolution
5. Fit agents in right places
6. Run 24/7 monitoring
"""

import os
import sys
import time
import json
import logging
import importlib.util
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

logging.basicConfig(
    level=logging.INFO,
    format='🤖 [MASTER] %(message)s',
    handlers=[
        logging.FileHandler('master_agent_controller.log'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)


class MasterAgentController:
    """Master controller for all agents - ਸਾਰੇ agents ਦਾ ਮਾਲਕ"""
    
    def __init__(self, workspace="/Users/gurpreetdhillon/Nam-toon-studio"):
        self.workspace = Path(workspace)
        self.agents = {}
        self.agent_status = {}
        self.auto_mode = True
        self.evolution_enabled = True
        
        log.info("="*70)
        log.info("🤖 MASTER AGENT CONTROLLER STARTING")
        log.info("   ਸਾਰੇ agents ਨੂੰ auto mode ਤੇ ਲਗਾ ਰਿਹਾਂ...")
        log.info("="*70)
        
        self.discover_agents()
        self.configure_agents()
    
    def discover_agents(self):
        """Auto-discover all agent files"""
        log.info("\n🔍 DISCOVERING AGENTS...")
        log.info("-" * 70)
        
        agent_files = list(self.workspace.glob("*agent*.py"))
        
        for agent_file in agent_files:
            if agent_file.name == 'MASTER_AGENT_CONTROLLER.py':
                continue
            
            try:
                # Load module
                spec = importlib.util.spec_from_file_location(
                    agent_file.stem, 
                    agent_file
                )
                if not spec or not spec.loader:
                    continue
                
                module = importlib.util.module_from_spec(spec)
                sys.modules[agent_file.stem] = module
                spec.loader.exec_module(module)
                
                # Find agent classes
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and 'Agent' in attr_name:
                        self.agents[attr_name] = {
                            'class': attr,
                            'module': module,
                            'file': agent_file,
                            'instance': None
                        }
                        log.info(f"   ✅ Found: {attr_name} in {agent_file.name}")
            
            except Exception as e:
                log.warning(f"   ⚠️  Could not load {agent_file.name}: {e}")
        
        log.info(f"\n📊 Total agents discovered: {len(self.agents)}")
    
    def configure_agents(self):
        """Configure each agent for auto-mode"""
        log.info("\n⚙️  CONFIGURING AGENTS FOR AUTO-MODE...")
        log.info("-" * 70)
        
        for agent_name, agent_info in self.agents.items():
            try:
                # Create instance
                agent_class = agent_info['class']
                
                # Try different initialization patterns
                try:
                    instance = agent_class(workspace=str(self.workspace))
                except TypeError:
                    try:
                        instance = agent_class(str(self.workspace))
                    except TypeError:
                        instance = agent_class()
                
                agent_info['instance'] = instance
                
                # Set auto-mode if possible
                if hasattr(instance, 'auto_mode'):
                    instance.auto_mode = True
                
                if hasattr(instance, 'continuous_mode'):
                    instance.continuous_mode = True
                
                self.agent_status[agent_name] = {
                    'enabled': True,
                    'auto_fix': True,
                    'auto_update': True,
                    'evolution': True,
                    'last_run': None,
                    'run_count': 0,
                    'errors_fixed': 0,
                    'upgrades': 0
                }
                
                log.info(f"   ✅ {agent_name} configured")
                log.info(f"      → Auto-fix: ON")
                log.info(f"      → Auto-update: ON")
                log.info(f"      → Evolution: ON")
            
            except Exception as e:
                log.error(f"   ❌ Failed to configure {agent_name}: {e}")
                self.agent_status[agent_name] = {
                    'enabled': False,
                    'error': str(e)
                }
    
    def fit_agent_to_role(self, agent_name):
        """Fit agent to specific role based on its capabilities"""
        
        roles = {
            'AutonomousAgent': {
                'role': 'System Monitor & Auto-Fixer',
                'tasks': ['deep_scan', 'auto_fix', 'self_heal', 'evolution'],
                'priority': 1,
                'run_interval': 300  # 5 minutes
            },
            'StudioAgent': {
                'role': 'File Scanner & Error Detector',
                'tasks': ['scan_files', 'check_errors', 'auto_fix'],
                'priority': 2,
                'run_interval': 600  # 10 minutes
            },
            'StudioAgentCodegen': {
                'role': 'Code Upgrade & Optimization',
                'tasks': ['scan_for_upgrades', 'apply_upgrade'],
                'priority': 3,
                'run_interval': 1800  # 30 minutes
            },
            'StudioAgentSecurity': {
                'role': 'Security Scanner',
                'tasks': ['security_scan', 'vulnerability_check'],
                'priority': 2,
                'run_interval': 3600  # 1 hour
            }
        }
        
        return roles.get(agent_name, {
            'role': 'General Agent',
            'tasks': [],
            'priority': 5,
            'run_interval': 3600
        })
    
    def run_agent_cycle(self, agent_name):
        """Run one cycle of agent work"""
        
        if agent_name not in self.agents:
            return
        
        agent_info = self.agents[agent_name]
        instance = agent_info['instance']
        
        if not instance:
            return
        
        role_info = self.fit_agent_to_role(agent_name)
        
        log.info(f"\n🔧 Running: {agent_name}")
        log.info(f"   Role: {role_info['role']}")
        log.info(f"   Tasks: {', '.join(role_info['tasks'])}")
        
        try:
            # Execute agent tasks
            for task in role_info['tasks']:
                if hasattr(instance, task):
                    method = getattr(instance, task)
                    result = method()
                    
                    # Track results
                    if 'fix' in task.lower():
                        self.agent_status[agent_name]['errors_fixed'] += 1
                    if 'upgrade' in task.lower():
                        self.agent_status[agent_name]['upgrades'] += 1
            
            self.agent_status[agent_name]['last_run'] = datetime.now().isoformat()
            self.agent_status[agent_name]['run_count'] += 1
            
            log.info(f"   ✅ Cycle complete")
        
        except Exception as e:
            log.error(f"   ❌ Error in {agent_name}: {e}")
    
    def auto_evolution(self):
        """Evolve agents based on performance"""
        log.info("\n🧬 EVOLUTION CYCLE...")
        log.info("-" * 70)
        
        for agent_name, status in self.agent_status.items():
            if not status.get('enabled', False):
                continue
            
            run_count = status.get('run_count', 0)
            errors_fixed = status.get('errors_fixed', 0)
            
            # Evolution logic
            if run_count > 10 and errors_fixed > 5:
                log.info(f"   🌟 {agent_name} is performing well!")
                log.info(f"      → Runs: {run_count}, Fixes: {errors_fixed}")
                log.info(f"      → Evolution: Increasing priority")
                
                # Increase priority
                role_info = self.fit_agent_to_role(agent_name)
                if role_info['priority'] > 1:
                    role_info['priority'] -= 1
            
            elif run_count > 10 and errors_fixed == 0:
                log.info(f"   💤 {agent_name} found no work")
                log.info(f"      → Evolution: Reducing frequency")
                
                # Reduce frequency
                role_info = self.fit_agent_to_role(agent_name)
                role_info['run_interval'] *= 2
    
    def run_continuous(self, duration_minutes=None):
        """Run all agents continuously"""
        
        log.info("\n🚀 STARTING CONTINUOUS MODE")
        log.info("="*70)
        log.info("   All agents on AUTO mode")
        log.info("   Auto-fix: ENABLED")
        log.info("   Auto-update: ENABLED")
        log.info("   Evolution: ENABLED")
        log.info("="*70)
        
        start_time = time.time()
        cycle_count = 0
        
        try:
            while True:
                cycle_count += 1
                log.info(f"\n{'='*70}")
                log.info(f"🔄 CYCLE #{cycle_count} - {datetime.now().strftime('%H:%M:%S')}")
                log.info(f"{'='*70}")
                
                # Run each agent by priority
                agents_by_priority = sorted(
                    self.agents.items(),
                    key=lambda x: self.fit_agent_to_role(x[0])['priority']
                )
                
                for agent_name, _ in agents_by_priority:
                    if not self.agent_status.get(agent_name, {}).get('enabled', False):
                        continue
                    
                    role_info = self.fit_agent_to_role(agent_name)
                    last_run = self.agent_status[agent_name].get('last_run')
                    
                    # Check if it's time to run
                    should_run = False
                    if not last_run:
                        should_run = True
                    else:
                        last_run_time = datetime.fromisoformat(last_run)
                        elapsed = (datetime.now() - last_run_time).total_seconds()
                        if elapsed >= role_info['run_interval']:
                            should_run = True
                    
                    if should_run:
                        self.run_agent_cycle(agent_name)
                
                # Evolution every 10 cycles
                if cycle_count % 10 == 0 and self.evolution_enabled:
                    self.auto_evolution()
                
                # Status report
                self.print_status_report()
                
                # Check duration
                if duration_minutes:
                    elapsed_minutes = (time.time() - start_time) / 60
                    if elapsed_minutes >= duration_minutes:
                        log.info(f"\n✅ Completed {duration_minutes} minute run")
                        break
                
                # Sleep before next cycle
                log.info("\n💤 Sleeping 60 seconds...")
                time.sleep(60)
        
        except KeyboardInterrupt:
            log.info("\n\n⏹️  STOPPED by user")
            self.print_status_report()
    
    def print_status_report(self):
        """Print status of all agents"""
        log.info("\n" + "="*70)
        log.info("📊 AGENT STATUS REPORT")
        log.info("="*70)
        
        for agent_name, status in self.agent_status.items():
            if not status.get('enabled', False):
                continue
            
            role_info = self.fit_agent_to_role(agent_name)
            
            log.info(f"\n🤖 {agent_name}")
            log.info(f"   Role: {role_info['role']}")
            log.info(f"   Status: {'🟢 ACTIVE' if status['enabled'] else '🔴 DISABLED'}")
            log.info(f"   Runs: {status.get('run_count', 0)}")
            log.info(f"   Errors Fixed: {status.get('errors_fixed', 0)}")
            log.info(f"   Upgrades: {status.get('upgrades', 0)}")
            
            last_run = status.get('last_run')
            if last_run:
                log.info(f"   Last Run: {datetime.fromisoformat(last_run).strftime('%H:%M:%S')}")
        
        log.info("="*70)
    
    def save_state(self):
        """Save agent states"""
        state_file = self.workspace / "agent_states.json"
        
        state_data = {
            'agents': list(self.agents.keys()),
            'status': self.agent_status,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(state_file, 'w') as f:
            json.dump(state_data, f, indent=2)
        
        log.info(f"\n💾 State saved: {state_file}")


def main():
    """Main entry point"""
    
    log.info("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║           🤖 MASTER AGENT CONTROLLER                              ║
║           ਸਾਰੇ Agents ਨੂੰ Auto Mode ਤੇ ਲਗਾਉਣਾ                    ║
║                                                                   ║
║   • Auto-Fix: ON                                                  ║
║   • Auto-Update: ON                                               ║
║   • Evolution: ON                                                 ║
║   • 24/7 Monitoring: ON                                           ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    controller = MasterAgentController()
    
    # Print discovered agents
    log.info("\n🎯 AGENT DEPLOYMENT:")
    for agent_name in controller.agents.keys():
        role_info = controller.fit_agent_to_role(agent_name)
        log.info(f"   • {agent_name} → {role_info['role']}")
    
    # Ask user
    log.info("\n" + "="*70)
    mode = input("🚀 Run mode? [1] Test (5 min), [2] Continuous 24/7: ").strip()
    
    if mode == '1':
        controller.run_continuous(duration_minutes=5)
    else:
        controller.run_continuous()
    
    controller.save_state()


if __name__ == "__main__":
    main()
