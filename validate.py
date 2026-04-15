#!/usr/bin/env python3
"""Quick validation script for Kliker"""

def main():
    print("🔍 Kliker Validation\n")
    
    # Test core imports
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox, scrolledtext
        import threading, time, sys, os, json
        print("✅ Core imports OK")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test pynput
    pynput_ok = False
    try:
        from pynput import mouse, keyboard
        from pynput.mouse import Button
        from pynput.keyboard import Key
        mouse.Controller()
        keyboard.Controller()
        print("✅ pynput OK")
        pynput_ok = True
    except ImportError:
        print("⚠️  pynput unavailable (headless environment)")
    except Exception as e:
        print(f"⚠️  pynput display failed: {type(e).__name__}")
    
    # Test syntax
    try:
        with open('kliker.py', 'r') as f:
            compile(f.read(), 'kliker.py', 'exec')
        print("✅ Syntax OK")
    except Exception as e:
        print(f"❌ Syntax error: {e}")
        return False
    
    # Test state module
    try:
        from clicker_state import ClickerState
        state = ClickerState()
        state.increment_clicks()
        assert state.get_click_count() == 1
        print("✅ State module OK")
    except Exception as e:
        print(f"❌ State module failed: {e}")
        return False
    
    status = "READY" if pynput_ok else "READY (GUI environment required)"
    print(f"\n✅ Validation complete: {status}")
    return True

if __name__ == "__main__":
    exit(0 if main() else 1)