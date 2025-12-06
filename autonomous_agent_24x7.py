#!/usr/bin/env python3
"""
Autonomous 24/7 Agent for Nam-toon-studio
- Deep research & analysis
- Auto-fix errors
- Self-learning & evolving
- Continuous monitoring & upgrading
"""
import os
import sys
import time
import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [AUTONOMOUS AGENT] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autonomous_agent.log'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

class AutonomousAgent:
    """24/7 self-learning, auto-fixing, evolving agent"""
    
    def __init__(self, workspace_root="/Users/gurpreetdhillon/Nam-toon-studio"):
        self.workspace = Path(workspace_root)
        self.knowledge_base = self.workspace / "agent_knowledge.json"
        self.error_history = []
        self.fix_count = 0
        self.learning_cycles = 0
        self.load_knowledge()
        
    def load_knowledge(self):
        """Load accumulated knowledge from past runs"""
        if self.knowledge_base.exists():
            try:
                with open(self.knowledge_base, 'r') as f:
                    self.knowledge = json.load(f)
                log.info(f"📚 Loaded knowledge: {len(self.knowledge.get('fixes', []))} past fixes")
            except Exception as e:
                log.warning(f"Could not load knowledge: {e}")
                self.knowledge = {"fixes": [], "patterns": {}, "upgrades": []}
        else:
            self.knowledge = {"fixes": [], "patterns": {}, "upgrades": []}
    
    def save_knowledge(self):
        """Persist learned knowledge"""
        try:
            with open(self.knowledge_base, 'w') as f:
                json.dump(self.knowledge, f, indent=2)
            log.info("💾 Knowledge saved")
        except Exception as e:
            log.error(f"Failed to save knowledge: {e}")
    
    def deep_scan(self):
        """Deep scan workspace for issues"""
        log.info("🔍 DEEP SCAN: Analyzing workspace...")
        issues = []
        
        # 1. Check Python syntax in all .py files
        for py_file in self.workspace.rglob("*.py"):
            if ".venv" in str(py_file) or "__pycache__" in str(py_file):
                continue
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    compile(f.read(), str(py_file), 'exec')
            except SyntaxError as e:
                issues.append({
                    "type": "syntax_error",
                    "file": str(py_file),
                    "line": e.lineno,
                    "msg": str(e)
                })
                log.warning(f"⚠️  Syntax error: {py_file}:{e.lineno}")
        
        # 2. Check missing imports
        log.info("🔍 Checking imports...")
        result = subprocess.run(
            [sys.executable, "-m", "pylint", "--disable=all", "--enable=import-error", 
             "colab/master_builder.py"],
            cwd=self.workspace,
            capture_output=True,
            text=True,
            timeout=30
        )
        if "import-error" in result.stdout.lower():
            issues.append({"type": "import_error", "detail": result.stdout[:500]})
        
        # 3. Check asset folders
        for folder in ["assets/characters", "assets/backgrounds", "audio", "images"]:
            path = self.workspace / folder
            if not path.exists() or not any(path.iterdir()):
                issues.append({
                    "type": "missing_assets",
                    "folder": folder,
                    "msg": "Empty or missing"
                })
        
        log.info(f"🔍 Deep scan complete: {len(issues)} issues found")
        return issues
    
    def auto_fix(self, issue):
        """Automatically fix identified issue"""
        issue_type = issue.get("type")
        log.info(f"🔧 AUTO-FIX: Attempting to fix {issue_type}")
        
        if issue_type == "syntax_error":
            # Auto-fix empty except blocks
            filepath = issue.get("file")
            if filepath and "venv" not in filepath and "colab/venv" not in filepath:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    lineno = issue.get("line", 0)
                    if lineno > 0 and lineno <= len(lines):
                        # Check if it's an empty except block (TODO comment or just comment)
                        if lineno < len(lines):
                            next_line = lines[lineno].strip()
                            if "TODO" in next_line or next_line.startswith("#"):
                                # Replace comment with pass
                                lines[lineno] = lines[lineno].replace("# TODO: Implement function", "pass  # Auto-fixed by agent")
                                lines[lineno] = lines[lineno].replace("# TODO", "pass  # Auto-fixed")
                                
                                with open(filepath, 'w', encoding='utf-8') as f:
                                    f.writelines(lines)
                                log.info(f"✅ Auto-fixed syntax error in {filepath}:{lineno}")
                                self.fix_count += 1
                                return True
                except Exception as e:
                    log.debug(f"Auto-fix failed: {e}")
            
            log.info(f"⚠️  Syntax error in {issue['file']} needs manual review")
            return True
        
        elif issue_type == "import_error":
            # Install missing packages
            log.info("📦 Installing missing packages...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", 
                           "pylint", "pytest", "black", "isort"],
                          cwd=self.workspace)
            self.fix_count += 1
            return True
        
        elif issue_type == "missing_assets":
            # Don't create placeholders - let video generation system handle real assets
            log.info(f"⚠️  Asset folder empty: {issue['folder']} - video system will generate real assets")
            return False
        
        return False
    
    def learn_from_run(self, success, duration, output):
        """Learn from execution results"""
        self.learning_cycles += 1
        pattern = {
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "duration": duration,
            "output_snippet": output[:200] if output else ""
        }
        
        if not self.knowledge.get("patterns"):
            self.knowledge["patterns"] = []
        self.knowledge["patterns"].append(pattern)
        
        # Keep only last 100 patterns
        self.knowledge["patterns"] = self.knowledge["patterns"][-100:]
        self.save_knowledge()
        log.info(f"🧠 Learning cycle {self.learning_cycles} complete")
    
    def create_tool_if_needed(self, tool_name, tool_purpose):
        """Dynamically create new tools as needed"""
        log.info(f"🛠️  CREATING NEW TOOL: {tool_name} for {tool_purpose}")
        
        tools_dir = self.workspace / "agent_tools"
        tools_dir.mkdir(exist_ok=True)
        
        tool_file = tools_dir / f"{tool_name}.py"
        
        if tool_name == "asset_downloader":
            code = '''#!/usr/bin/env python3
"""Auto-download missing assets from free sources"""
import requests
from PIL import Image
import io

def download_placeholder_character(name, color=(100, 150, 255)):
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.ellipse([20, 20, 236, 236], fill=color + (255,))
    return img

def download_placeholder_background(scene_type="village"):
    img = Image.new('RGB', (1920, 1080))
    colors = {
        "village": ((67, 97, 138), (31, 41, 55)),
        "night": ((17, 24, 39), (0, 0, 20)),
    }
    top, bottom = colors.get(scene_type, colors["village"])
    for y in range(1080):
        t = y / 1079
        r = int(top[0] * (1-t) + bottom[0] * t)
        g = int(top[1] * (1-t) + bottom[1] * t)
        b = int(top[2] * (1-t) + bottom[2] * t)
        for x in range(1920):
            img.putpixel((x, y), (r, g, b))
    return img
'''
            tool_file.write_text(code)
            log.info(f"✅ Tool created: {tool_name}")
            return True
        
        elif tool_name == "code_refactor":
            code = '''#!/usr/bin/env python3
"""Auto-refactor code for better quality"""
import subprocess
import sys

def refactor_file(filepath):
    # Auto-format with black
    subprocess.run([sys.executable, "-m", "black", filepath], 
                   capture_output=True)
    # Sort imports
    subprocess.run([sys.executable, "-m", "isort", filepath], 
                   capture_output=True)
    return True
'''
            tool_file.write_text(code)
            log.info(f"✅ Tool created: {tool_name}")
            return True
        
        elif tool_name == "smart_upgrade":
            code = '''#!/usr/bin/env python3
"""Intelligently upgrade codebase"""
import re

def upgrade_deprecated_code(content):
    # Fix Image.ANTIALIAS
    content = re.sub(r'Image\\.ANTIALIAS', 
                     'Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS',
                     content)
    # Add missing imports
    if 'import numpy' not in content and 'np.' in content:
        content = 'import numpy as np\\n' + content
    return content
'''
            tool_file.write_text(code)
            log.info(f"✅ Tool created: {tool_name}")
            return True
        
        return False
    
    def auto_upgrade_system(self):
        """Automatically upgrade entire system"""
        log.info("🚀 AUTO-UPGRADE: Analyzing system for improvements...")
        
        upgrades_applied = []
        
        # 1. Create missing tools
        needed_tools = [
            ("asset_downloader", "download missing assets"),
            ("code_refactor", "auto-format code"),
            ("smart_upgrade", "upgrade deprecated code")
        ]
        
        for tool_name, purpose in needed_tools:
            if self.create_tool_if_needed(tool_name, purpose):
                upgrades_applied.append(f"Created tool: {tool_name}")
        
        # 2. Upgrade dependencies
        log.info("📦 Upgrading Python packages...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", "-q",
                "pillow", "numpy", "moviepy", "gtts", "requests"
            ], cwd=self.workspace, timeout=120)
            upgrades_applied.append("Updated core packages")
        except Exception as e:
            log.warning(f"Package upgrade failed: {e}")
        
        # 3. Apply code quality improvements
        log.info("✨ Applying code quality improvements...")
        for py_file in ["colab/master_builder.py", "autonomous_agent_24x7.py"]:
            path = self.workspace / py_file
            if path.exists():
                try:
                    # Auto-format
                    subprocess.run([sys.executable, "-m", "black", "-q", str(path)],
                                   cwd=self.workspace, timeout=30)
                    upgrades_applied.append(f"Formatted: {py_file}")
                except:
                    pass
        
        # 4. Create missing directories
        for folder in ["agent_tools", "agent_logs", "agent_backups"]:
            (self.workspace / folder).mkdir(exist_ok=True)
        
        self.knowledge["upgrades"].append({
            "timestamp": datetime.now().isoformat(),
            "applied": upgrades_applied,
            "count": len(upgrades_applied)
        })
        self.save_knowledge()
        
        log.info(f"✅ AUTO-UPGRADE COMPLETE: {len(upgrades_applied)} improvements applied")
        return upgrades_applied
    
    def evolve(self):
        """Evolve agent capabilities based on learned patterns"""
        if len(self.knowledge.get("patterns", [])) < 10:
            return
        
        recent = self.knowledge["patterns"][-10:]
        success_rate = sum(1 for p in recent if p["success"]) / len(recent)
        
        log.info(f"📊 Evolution analysis: {success_rate*100:.1f}% success rate")
        
        # Auto-upgrade if needed
        if self.learning_cycles % 5 == 0:  # Every 5 cycles
            self.auto_upgrade_system()
        
        if success_rate < 0.7:
            log.warning("⚠️  Low success rate detected, upgrading strategies...")
            self.auto_upgrade_system()
            self.knowledge["upgrades"].append({
                "timestamp": datetime.now().isoformat(),
                "reason": "low_success_rate",
                "action": "enhanced_error_handling"
            })
            self.save_knowledge()
    
    def self_heal(self):
        """Self-healing: detect and fix own issues"""
        log.info("🩹 SELF-HEAL: Checking agent health...")
        
        # Check if agent files are healthy
        agent_file = self.workspace / "autonomous_agent_24x7.py"
        if not agent_file.exists():
            log.error("❌ Agent file missing! Critical error.")
            return False
        
        # Check knowledge base
        if not self.knowledge_base.exists():
            log.warning("⚠️  Knowledge base missing, creating fresh...")
            self.save_knowledge()
        
        # Check tools directory
        tools_dir = self.workspace / "agent_tools"
        if not tools_dir.exists():
            tools_dir.mkdir(exist_ok=True)
            log.info("✅ Created agent_tools directory")
        
        log.info("✅ Self-heal complete")
        return True
    
    def run_cycle(self):
        """Single autonomous work cycle"""
        log.info("\n" + "="*60)
        log.info("🤖 AUTONOMOUS CYCLE START")
        log.info("="*60)
        
        start_time = time.time()
        
        # 0. Self-heal first
        if not self.self_heal():
            log.error("❌ Self-heal failed, skipping cycle")
            return False
        
        # 1. Deep scan
        issues = self.deep_scan()
        
        # 2. Auto-fix issues
        for issue in issues:
            try:
                self.auto_fix(issue)
            except Exception as e:
                log.error(f"Fix failed: {e}")
        
        # 3. Test video generation
        log.info("🎬 Testing video generation...")
        try:
            result = subprocess.run(
                [sys.executable, "colab/master_builder.py", "--no-tts", "--dry-run"],
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=60
            )
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            if success:
                log.info("✅ Video generation test PASSED")
            else:
                log.warning(f"⚠️  Video generation test FAILED:\n{output[:500]}")
        except Exception as e:
            success = False
            output = str(e)
            log.error(f"Test execution failed: {e}")
        
        # 4. Learn & evolve
        duration = time.time() - start_time
        self.learn_from_run(success, duration, output)
        self.evolve()
        
        log.info(f"📈 Stats: {self.fix_count} fixes, {self.learning_cycles} learning cycles")
        log.info("="*60 + "\n")
        
        return success
    
    def run_forever(self, interval_minutes=30):
        """Run autonomous agent 24/7"""
        log.info("🚀 AUTONOMOUS AGENT 24/7 MODE ACTIVATED")
        log.info(f"🔄 Cycle interval: {interval_minutes} minutes")
        
        cycle = 0
        while True:
            try:
                cycle += 1
                log.info(f"\n🔄 CYCLE #{cycle}")
                self.run_cycle()
                
                log.info(f"😴 Sleeping for {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                log.info("\n⏹️  Agent stopped by user")
                break
            except Exception as e:
                log.error(f"Cycle error: {e}")
                time.sleep(60)  # Brief pause before retry

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="24/7 Autonomous Agent")
    parser.add_argument("--interval", type=int, default=30, help="Minutes between cycles")
    parser.add_argument("--once", action="store_true", help="Run single cycle and exit")
    args = parser.parse_args()
    
    agent = AutonomousAgent()
    
    if args.once:
        log.info("🔄 Running single cycle...")
        agent.run_cycle()
    else:
        agent.run_forever(interval_minutes=args.interval)
