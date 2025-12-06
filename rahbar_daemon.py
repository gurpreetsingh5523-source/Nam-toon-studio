#!/usr/bin/env python3
"""
👑 Rahbar Daemon - Background Runner
Runs Rahbar Supreme without terminal attachment issues
"""

import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(__file__).parent

def run_cycle():
    """Run one Rahbar cycle"""
    print(f"\n{'='*70}")
    print(f"🔄 Starting Rahbar cycle at {datetime.now().strftime('%I:%M %p')}")
    print(f"{'='*70}\n")
    
    try:
        # Run with stdout/stderr redirected to devnull to avoid TTY issues
        result = subprocess.run(
            [sys.executable, str(WORKSPACE / "rahbar_supreme_controller.py")],
            cwd=WORKSPACE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=600  # 10 minutes max
        )
        
        if result.returncode == 0:
            print("✅ Cycle completed successfully")
            return True
        else:
            print(f"⚠️ Cycle failed with code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Cycle timeout (10 minutes)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run multiple cycles"""
    print("\n" + "="*70)
    print("👑 RAHBAR DAEMON STARTING")
    print("   Running in background - no terminal attachment")
    print("   ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ")
    print("="*70)
    
    cycles = 8
    successful = 0
    
    for i in range(1, cycles + 1):
        print(f"\n📍 Cycle {i}/{cycles}")
        
        if run_cycle():
            successful += 1
        
        # Check logs after each cycle
        log_file = WORKSPACE / "rahbar_supreme_log.json"
        if log_file.exists():
            size_kb = log_file.stat().st_size / 1024
            print(f"   📄 Log size: {size_kb:.1f} KB")
        
        # Count videos
        videos = list(WORKSPACE.glob("training_*.mp4"))
        recent = [v for v in videos if (time.time() - v.stat().st_mtime) < 3600]
        print(f"   🎬 Videos: {len(videos)} total, {len(recent)} recent")
        
        # Sleep before next cycle
        if i < cycles:
            print(f"   😴 Sleeping 1 hour...")
            time.sleep(3600)
    
    print(f"\n{'='*70}")
    print(f"✅ DAEMON COMPLETE")
    print(f"   Successful cycles: {successful}/{cycles}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
