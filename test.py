#!/usr/bin/env python3
"""Test script for Kliker - checks dependencies and basic functionality"""

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import tkinter
        from pynput import mouse, keyboard
        import threading, time
        print("✓ All imports OK")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_state_module():
    """Test ClickerState functionality"""
    try:
        from clicker_state import ClickerState
        state = ClickerState()
        
        # Test click counting
        state.increment_clicks()
        assert state.get_click_count() == 1, "Click count failed"
        
        # Test position recording
        state.add_position(100, 200)
        assert state.get_positions_count() == 1, "Position recording failed"
        
        # Test stats
        stats = state.get_stats_snapshot()
        assert 'total_clicks' in stats, "Stats snapshot failed"
        
        print("✓ State module OK")
        return True
    except Exception as e:
        print(f"✗ State module failed: {e}")
        return False

def main():
    print("Testing Kliker...\n")
    
    if not test_imports():
        print("\nFix: pip install -r requirements.txt")
        return False
    
    if not test_state_module():
        return False
    
    print("\n✅ All tests passed!")
    print("Run: python kliker.py")
    return True

if __name__ == "__main__":
    exit(0 if main() else 1)