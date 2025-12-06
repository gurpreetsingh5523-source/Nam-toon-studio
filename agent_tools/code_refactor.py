#!/usr/bin/env python3
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
