#!/usr/bin/env python3
"""
🚑 NUMPY FIXER
Fixing the 'binary incompatibility' error.

Problem: Numpy 2.0.2 is too new for some libraries.
Solution: Downgrade to Numpy 1.26.4 (stable).
"""

import subprocess
import sys

def fix_numpy():
    print("🚑 FIXING NUMPY VERSION...")
    print("=========================")
    
    try:
        # Uninstall current numpy
        print("🗑️  Uninstalling current numpy...")
        subprocess.call([sys.executable, "-m", "pip", "uninstall", "-y", "numpy"])
        
        # Install compatible version
        print("⬇️  Installing numpy<2.0.0...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy<2.0.0"])
        
        print("✅ Numpy fixed!")
        
        # Verify import
        import numpy
        print(f"   Current version: {numpy.__version__}")
        
    except Exception as e:
        print(f"❌ Fix failed: {e}")

if __name__ == "__main__":
    fix_numpy()
