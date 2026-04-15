#!/usr/bin/env python3
"""
Test script for Kliker
Checks if all dependencies are installed and basic functionality works
"""

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import tkinter
        print("✓ tkinter imported successfully")
    except ImportError:
        print("✗ tkinter not available")
        return False

    try:
        from pynput import mouse, keyboard
        print("✓ pynput imported successfully")
    except ImportError:
        print("✗ pynput not available")
        return False

    try:
        import threading
        import time
        print("✓ Standard library modules imported successfully")
    except ImportError:
        print("✗ Standard library modules not available")
        return False

    return True

def test_basic_functionality():
    """Test basic functionality without GUI"""
    try:
        from pynput import mouse, keyboard
        from pynput.mouse import Button

        # Test mouse controller
        mouse_ctrl = mouse.Controller()
        print("✓ Mouse controller created")

        # Test keyboard controller
        kb_ctrl = keyboard.Controller()
        print("✓ Keyboard controller created")

        # Test button mapping
        button_map = {"left": Button.left, "right": Button.right, "middle": Button.middle}
        print("✓ Button mapping works")

        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def main():
    print("Testing Kliker dependencies and basic functionality...\n")

    imports_ok = test_imports()
    if not imports_ok:
        print("\n❌ Import tests failed. Please install requirements:")
        print("pip install -r requirements.txt")
        return

    print()
    func_ok = test_basic_functionality()
    if not func_ok:
        print("\n❌ Functionality tests failed.")
        return

    print("\n✅ All tests passed! Kliker should work correctly.")
    print("Note: GUI will require display server (X11 on Linux, etc.)")

if __name__ == "__main__":
    main()