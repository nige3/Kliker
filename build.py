#!/usr/bin/env python3
"""
Build script for Kliker - Auto Clicker Application
Creates a standalone executable using PyInstaller
"""

import os
import sys
import subprocess
import platform

def build_executable():
    """Build standalone executable for current platform"""

    print("Building Kliker executable...")

    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",           # Single executable file
        "--windowed",          # No console window
        "--name=Kliker",       # Output name
        "--clean",             # Clean cache
        "--noconfirm",         # Overwrite without asking
        "kliker.py"
    ]

    # Platform-specific options
    system = platform.system()
    if system == "Windows":
        cmd.append("--icon=icon.ico")  # Add icon if available
    elif system == "Darwin":  # macOS
        cmd.append("--icon=icon.icns")

    try:
        subprocess.check_call(cmd)
        print("Build completed successfully!")

        # Show output location
        dist_dir = os.path.join(os.getcwd(), "dist")
        exe_name = "Kliker.exe" if system == "Windows" else "Kliker"
        exe_path = os.path.join(dist_dir, exe_name)

        print(f"Executable created: {exe_path}")

    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()