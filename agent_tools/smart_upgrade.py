#!/usr/bin/env python3
"""Intelligently upgrade codebase"""
import re

def upgrade_deprecated_code(content):
    # Fix Image.ANTIALIAS
    content = re.sub(r'Image\.ANTIALIAS', 
                     'Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS',
                     content)
    # Add missing imports
    if 'import numpy' not in content and 'np.' in content:
        content = 'import numpy as np\n' + content
    return content
