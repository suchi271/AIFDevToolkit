#!/usr/bin/env python3
"""
Clean Cache Script
==================
Removes Python cache files and temporary directories from the project.
Run this script to clean up __pycache__ directories and .pyc files.
"""

import os
import shutil
import glob

def clean_cache():
    """Remove Python cache files and directories."""
    print("🧹 Cleaning Python cache files...")
    
    # Find and remove __pycache__ directories
    cache_dirs = []
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_path = os.path.join(root, '__pycache__')
            cache_dirs.append(cache_path)
    
    for cache_dir in cache_dirs:
        try:
            shutil.rmtree(cache_dir)
            print(f"✓ Removed: {cache_dir}")
        except Exception as e:
            print(f"✗ Failed to remove {cache_dir}: {e}")
    
    # Find and remove .pyc files
    pyc_files = glob.glob('**/*.pyc', recursive=True)
    for pyc_file in pyc_files:
        try:
            os.remove(pyc_file)
            print(f"✓ Removed: {pyc_file}")
        except Exception as e:
            print(f"✗ Failed to remove {pyc_file}: {e}")
    
    # Find and remove .pyo files
    pyo_files = glob.glob('**/*.pyo', recursive=True)
    for pyo_file in pyo_files:
        try:
            os.remove(pyo_file)
            print(f"✓ Removed: {pyo_file}")
        except Exception as e:
            print(f"✗ Failed to remove {pyo_file}: {e}")
    
    print(f"🎉 Cache cleanup complete!")
    print(f"   Removed {len(cache_dirs)} cache directories")
    print(f"   Removed {len(pyc_files)} .pyc files")
    print(f"   Removed {len(pyo_files)} .pyo files")

if __name__ == "__main__":
    clean_cache()
