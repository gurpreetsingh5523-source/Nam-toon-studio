#!/usr/bin/env python3
"""
🚑 SYSTEM REPAIR DOCTOR
Fixing the AI Brain (Libraries)

Problem: 'transformers' and 'diffusers' are broken.
Solution: Re-install compatible versions.
"""

import subprocess
import sys

def install_package(package):
    print(f"🔧 Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--upgrade"])
        print(f"✅ {package} installed!")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")

def run_repairs():
    print("🚑 STARTING SYSTEM REPAIR...")
    print("===========================")
    
    # 1. Fix Transformers/Diffusers mismatch
    # These versions are known to work well together
    packages = [
        "transformers>=4.30.0",
        "diffusers>=0.19.0",
        "accelerate>=0.21.0",
        "torch", 
        "safetensors",
        "sentencepiece"
    ]
    
    for pkg in packages:
        install_package(pkg)
        
    print("\n🔄 Verifying imports...")
    try:
        from diffusers import StableDiffusionPipeline
        import torch
        print("✅ Stable Diffusion is READY!")
        print(f"   Torch version: {torch.__version__}")
    except ImportError as e:
        print(f"❌ Still failing: {e}")

if __name__ == "__main__":
    run_repairs()
