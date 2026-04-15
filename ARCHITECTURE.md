# Kliker 2.0 - Architecture & Developer Guide

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Module Overview](#module-overview)
3. [Class Design](#class-design)
4. [Thread Safety](#thread-safety)
5. [Configuration System](#configuration-system)
6. [Extension Points](#extension-points)
7. [Design Patterns](#design-patterns)
8. [Best Practices](#best-practices)

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│                    (Tkinter GUI)                         │
│         ┌──────────────────────────────────┐             │
│         │      KlikerApp (Main Class)      │             │
│         │   - GUI Components                │             │
│         │   - Event Handling                │             │
│         │   - Settings Management           │             │
│         └──────────────────────────────────┘             │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│             State Management Layer                       │
│         ┌──────────────────────────────────┐             │
│         │      ClickerState (Thread-Safe)   │             │
│         │  - Running state                  │             │
│         │  - Click counting                 │             │
│         │  - Position recording             │             │
│         │  - Statistics                     │             │
│         │  - Thread synchronization         │             │
│         └──────────────────────────────────┘             │
└────────────────────────┬────────────────────────────────┘
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
      ┌─────────┐  ┌──────────┐  ┌─────────┐
      │  Click  │  │ Keyboard │  │  Mouse  │
      │  Loop   │  │ Listener │  │Listener │
      │(Thread) │  │(Thread)  │  │(Thread) │
      └─────────┘  └──────────┘  └─────────┘
            │            │            │
            └────────────┼────────────┘
                         ▼
                    ┌──────────┐
                    │ pynput   │
                    │ Library  │
                    └──────────┘
```

### Data Flow

```
User Input → KlikerApp → ClickerState → Click Logic
     ↓           ↓            ↓              ↓
  Events    Validation   Safe Access    Threading
             & Updates
```

---

## Module Overview

### kliker.py (Main Module)
**Responsibility:** User interface and application coordination  
**Size:** ~950 lines  
**Dependencies:** tkinter, pynput, json, threading, etc.

**Main Class:** `KlikerApp`
- Manages GUI components
- Handles user interactions
- Coordinates with ClickerState
- Manages configuration
- Implements click logic

**Key Sections:**
1. Configuration Management (load/save JSON)
2. Theme Management (light/dark)
3. UI Creation (tabbed interface)
4. Settings Management (validation, presets)
5. Statistics (display, auto-update)
6. Clicking Logic (realtime and playback modes)
7. Recording Logic (sequence capture)
8. Hotkey Management (global shortcuts)
9. UI Utilities (sounds, help, tooltips)

### clicker_state.py (State Module)
**Responsibility:** Thread-safe state container  
**Size:** ~180 lines  
**Dependencies:** threading, datetime

**Main Class:** `ClickerState`
- Encapsulates all shared state
- Provides thread-safe access via RLock
- Manages click statistics
- Handles position recording
- Manages listener references

**Key Methods:**
- Running state: `get_running()`, `set_running()`
- Click tracking: `increment_clicks()`, `get_click_count()`
- Recording: `add_position()`, `get_positions()`, `clear_positions()`
- Statistics: `get_stats_snapshot()`, `reset_session()`
- Thread refs: `set_click_thread()`, `get_click_thread()`
- Listeners: `set_hotkey_listener()`, `get_hotkey_listener()`

---

## Class Design

### KlikerApp Class Structure

```python
class KlikerApp:
    
    # ========== Initialization ==========
    def __init__(self, root: tk.Tk) -> None
    
    # ========== Configuration Management ==========
    def _load_config(self) -> Dict[str, Any]
    def _save_config(self) -> None
    def save_current_config(self) -> None
    def load_config_file(self) -> None
    def _apply_loaded_config(self) -> None
    
    # ========== Theme Management ==========
    def apply_theme(self) -> None
    def _apply_dark_theme(self, style: ttk.Style) -> None
    def _apply_light_theme(self, style: ttk.Style) -> None
    def toggle_theme(self) -> None
    
    # ========== UI Creation ==========
    def _create_widgets(self) -> None
    def _create_header(self, parent: ttk.Frame) -> None
    def _create_status_frame(self, parent: ttk.Frame) -> None
    def _create_mode_selection(self, parent: ttk.Frame) -> None
    def _create_settings_tabs(self, parent: ttk.Frame) -> None
    def _create_basic_settings(self, parent: ttk.Frame) -> None
    def _create_advanced_settings(self, parent: ttk.Frame) -> None
    def _create_sequence_frame(self, parent: ttk.Frame) -> None
    def _create_control_buttons(self, parent: ttk.Frame) -> None
    def _create_preset_buttons(self, parent: ttk.Frame) -> None
    def _create_footer(self, parent: ttk.Frame) -> None
    def _create_tooltip(self, widget: tk.Widget, text: str) -> None
    
    # ========== Settings Management ==========
    def switch_mode(self) -> None
    def set_preset(self, interval: int, count: int) -> None
    def reset_session_stats(self) -> None
    
    # ========== Stats Management ==========
    def _schedule_stats_update(self) -> None
    def _update_stats_display(self) -> None
    
    # ========== Input Validation ==========
    def _validate_input(self) -> Tuple[bool, Optional[str]]
    
    # ========== Clicking Logic ==========
    def start_clicking(self) -> None
    def pause_clicking(self) -> None
    def stop_clicking(self) -> None
    def _get_next_interval(self, ...) -> float
    def _click_loop(self, ...) -> None
    def _playback_loop(self, ...) -> None
    
    # ========== Recording Logic ==========
    def start_recording(self) -> None
    def stop_recording(self) -> None
    def clear_sequence(self) -> None
    def _update_sequence_display(self) -> None
    
    # ========== Hotkey Management ==========
    def _setup_hotkeys(self) -> None
    def _handle_hotkey(self, key) -> None
    
    # ========== UI Utilities ==========
    def _play_sound(self, sound_type: str) -> None
    def show_help(self) -> None
    def _on_closing(self) -> None
```

### ClickerState Class Structure

```python
class ClickerState:
    
    # ========== Initialization ==========
    def __init__(self) -> None
    
    # ========== Running State ==========
    def get_running(self) -> bool
    def set_running(self, value: bool) -> None
    def get_paused(self) -> bool
    def set_paused(self, value: bool) -> None
    
    # ========== Click Counting ==========
    def increment_clicks(self) -> None
    def get_click_count(self) -> int
    def reset_session(self) -> None
    
    # ========== Statistics ==========
    def get_stats_snapshot(self) -> Dict[str, Any]
    
    # ========== Position Recording ==========
    def add_position(self, x: int, y: int) -> None
    def get_positions(self) -> List[Tuple[int, int]]
    def get_positions_count(self) -> int
    def clear_positions(self) -> None
    
    # ========== Recording Mode ==========
    def get_record_mode(self) -> bool
    def set_record_mode(self, value: bool) -> None
    def get_record_listener(self) -> Optional[mouse.Listener]
    def set_record_listener(self, listener: Optional[mouse.Listener]) -> None
    
    # ========== Thread Management ==========
    def get_click_thread(self) -> Optional[threading.Thread]
    def set_click_thread(self, thread: Optional[threading.Thread]) -> None
    def get_hotkey_listener(self) -> Optional[keyboard.Listener]
    def set_hotkey_listener(self, listener: Optional[keyboard.Listener]) -> None
```

---

## Thread Safety

### The Problem
Multiple threads access shared state:
- GUI thread reads/writes UI variables
- Click thread updates click count
- Hotkey thread handles keyboard input
- Recording thread captures positions

### The Solution: RLock

```python
class ClickerState:
    def __init__(self):
        self._lock = threading.RLock()  # Reentrant lock
        self._total_clicks = 0
    
    def increment_clicks(self) -> None:
        with self._lock:  # Acquire lock
            self._total_clicks += 1  # Protected
        # Lock automatically released
```

### Protected Operations
Every state modification is wrapped:

| Method | Protected | Lock | Duration |
|--------|-----------|------|----------|
| `increment_clicks()` | ✅ | RLock | ~1µs |
| `get_running()` | ✅ | RLock | <1µs |
| `add_position()` | ✅ | RLock | ~1µs |
| `get_stats_snapshot()` | ✅ | RLock | ~10µs |

### Race Condition Prevention

**Before (Unsafe):**
```python
# Thread 1                    # Thread 2
self.total_clicks += 1       # Read: total_clicks = 0
                             # Increment = 1
                             # Write: total_clicks = 1
# Read: total_clicks = 0     
# Increment = 1              
# Write: total_clicks = 1    
# Result: Lost increment!    
```

**After (Safe):**
```python
# Thread 1                    # Thread 2
with self._lock:             # Blocked - waiting for lock
    self.total_clicks += 1   # 
                             # Acquired lock
                             # with self._lock:
                             #     self.total_clicks += 1
                             # Result: Correct!
```

---

## Configuration System

### Configuration File: `kliker_config.json`

```json
{
  "interval": 100,           // Click interval in milliseconds
  "count": 0,                // Number of clicks (0 = infinite)
  "button": "left",          // Mouse button (left/right/middle)
  "hotkey": "f6",            // Global hotkey
  "randomization": 10,       // Timing variation percentage
  "pattern": "linear",       // Click pattern type
  "sound_enabled": true,     // Enable notification sounds
  "theme": "light"           // UI theme (light/dark)
}
```

### Default Configuration

In `kliker.py`:

```python
DEFAULT_CONFIG = {
    'interval': 100,
    'count': 0,
    'button': 'left',
    'hotkey': 'f6',
    'randomization': 10,
    'pattern': 'linear',
    'sound_enabled': True,
    'theme': 'light'
}
```

### Configuration Lifecycle

```
┌──────────────┐
│   Program    │
│   Startup    │
└──────┬───────┘
       ▼
┌──────────────────────────────┐
│  Check for kliker_config.json│
└──────┬───────────────────────┘
       │
       ├─→ Exists → Load JSON
       │               ↓
       │         Merge with defaults
       │               ↓
       │         Apply to UI
       │
       └─→ Not found → Use defaults
                           ↓
                      Initialize UI

When User Clicks "Save Config":
    ↓
Update config dict
    ↓
Write to kliker_config.json
    ↓
Show confirmation
```

### Loading Custom Configurations

```python
def load_config_file(self) -> None:
    """Load configuration from file dialog."""
    file_path = filedialog.askopenfilename(
        title="Load Configuration",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'r') as f:
                loaded_config = json.load(f)
            self.config.update(loaded_config)
            self._apply_loaded_config()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load: {e}")
```

---

## Extension Points

### Adding a New Click Pattern

**1. Update pattern list in constants:**
```python
VALID_PATTERNS = ["linear", "random", "sine", "exponential", "mypattern"]
```

**2. Implement pattern logic:**
```python
def _get_next_interval(self, base: int, randomization: int, 
                      pattern: str, click_num: int = 0) -> float:
    # ... existing code ...
    
    elif pattern == "mypattern":
        # My custom calculation
        interval = base * (1 + math.cos(click_num * 0.05))
    
    return max(MIN_INTERVAL, interval)
```

**3. Update UI combo box:**
```python
pattern_combo = ttk.Combobox(parent, textvariable=self.pattern_var,
                            values=VALID_PATTERNS, state="readonly")
```

### Adding a New Configuration Option

**1. Add to defaults:**
```python
DEFAULT_CONFIG = {
    # ... existing ...
    'my_option': 'default_value'
}
```

**2. Create UI variable:**
```python
self.my_option_var = tk.StringVar(value=self.config.get('my_option', 'default'))
```

**3. Create UI control:**
```python
ttk.Entry(parent, textvariable=self.my_option_var).pack()
```

**4. Save/load in config:**
```python
self.config['my_option'] = self.my_option_var.get()
```

### Adding a New Feature

**1. Create state container:**
```python
# In clicker_state.py
self._my_feature = None

def get_my_feature(self) -> Any:
    with self._lock:
        return self._my_feature

def set_my_feature(self, value: Any) -> None:
    with self._lock:
        self._my_feature = value
```

**2. Create UI controls:**
```python
# In KlikerApp._create_widgets()
def _create_my_feature(self, parent: ttk.Frame) -> None:
    # Create UI elements
    pass

# Call from _create_widgets()
self._create_my_feature(main_frame)
```

**3. Implement logic:**
```python
def my_feature_logic(self) -> None:
    # Access state safely
    value = self.state.get_my_feature()
    # Do something
    pass
```

---

## Design Patterns

### 1. Model-View-Controller (MVC)

- **Model:** `ClickerState` (thread-safe state)
- **View:** Tkinter widgets (UI)
- **Controller:** `KlikerApp` (coordination logic)

```python
                  User Input
                      ↓
            ┌─────────────────────┐
            │     KlikerApp       │
            │    (Controller)     │
            └────────┬──────────┬─────────┐
                     ▼          ▼         ▼
            ┌──────────────┐   ┌────────────────┐
            │   ClickerState│   │  UI Widgets    │
            │   (Model)     │   │   (View)       │
            └──────────────┘   └────────────────┘
```

### 2. Observer Pattern (Stats Update)

```python
def _schedule_stats_update(self) -> None:
    """Schedule periodic updates."""
    self._update_stats_display()

def _update_stats_display(self) -> None:
    """Observer: watches state and updates UI."""
    stats = self.state.get_stats_snapshot()  # Observe
    self.stats_var.set(f"Clicks: {stats['total_clicks']}")  # Update
    self.root.after(1000, self._update_stats_display)  # Reschedule
```

### 3. Strategy Pattern (Click Patterns)

```python
def _get_next_interval(self, base: int, pattern: str, ...) -> float:
    """Strategy: Different timing algorithms."""
    if pattern == "linear":
        return base  # Linear strategy
    elif pattern == "random":
        return base + random.uniform(-variance, variance)  # Random
    elif pattern == "sine":
        return base * math.sin(click_num)  # Sine strategy
```

### 4. Factory Pattern (Button Creation)

```python
button_map = {
    "left": Button.left,
    "right": Button.right,
    "middle": Button.middle
}
btn = button_map[button]  # Create appropriate button
```

### 5. Thread-Safe Singleton (ClickerState)

```python
# Single shared instance
self.state = ClickerState()

# All threads access same instance
# Protected by RLock for safety
```

---

## Best Practices

### 1. Always Lock When Accessing State

```python
# ❌ WRONG - potential race condition
def bad_method(self):
    return self.state._total_clicks  # Unsafe!

# ✅ RIGHT - thread-safe access
def good_method(self):
    return self.state.get_click_count()  # Safe!
```

### 2. Validate Input Early

```python
def start_clicking(self) -> None:
    # Validate before doing anything
    is_valid, error = self._validate_input()
    if not is_valid:
        messagebox.showerror("Error", error)
        return
    
    # Proceed with validated data
    start_clicking_logic()
```

### 3. Use Type Hints

```python
# ❌ WRONG
def process(self, data):
    return data.value

# ✅ RIGHT
def process(self, data: ConfigDict) -> int:
    return data['value']
```

### 4. Document Public APIs

```python
def public_method(self) -> None:
    """Description of what this does.
    
    Args:
        arg1: What arg1 is
        
    Returns:
        What is returned
        
    Raises:
        ExceptionType: When this exception occurs
    """
    pass
```

### 5. Clean Up Resources

```python
def _on_closing(self) -> None:
    """Handle window closing and cleanup."""
    try:
        # Stop clicking
        self.stop_clicking()
        
        # Stop listeners
        hotkey_listener = self.state.get_hotkey_listener()
        if hotkey_listener:
            hotkey_listener.stop()
        
        # Save config
        self._save_config()
    finally:
        self.root.destroy()
```

### 6. Use Context Managers for Locks

```python
# In ClickerState
def increment_clicks(self) -> None:
    with self._lock:  # Automatically released
        self._total_clicks += 1
        self._last_click_time = time.time()
```

### 7. Separate Concerns into Sections

```python
class KlikerApp:
    # ========== Configuration Management ==========
    def _load_config(self): ...
    def _save_config(self): ...
    
    # ========== Theme Management ==========
    def apply_theme(self): ...
    def toggle_theme(self): ...
    
    # ========== Clicking Logic ==========
    def _click_loop(self): ...
    def _playback_loop(self): ...
```

---

## Performance Considerations

### Click Thread Efficiency
- Minimal state access per click cycle
- Click operations < 1ms per iteration
- Randomization calculated once per click
- Pattern calculations O(1) complexity

### Memory Usage
- State object: ~5KB
- Configuration: ~1KB
- Listeners: ~10KB each (2-3 active)
- UI: ~30MB (tkinter baseline)
- **Total:** ~50-100MB

### Optimization Tips
1. Use linear pattern for fastest performance
2. Minimize randomization calculation
3. Avoid frequent config writes
4. Use realistic intervals (50ms+)
5. Close unneeded dialogs

---

## Testing Recommendations

### Unit Tests
```python
def test_clicker_state_thread_safety():
    """Test that state access is thread-safe."""
    state = ClickerState()
    
    def increment_multiple():
        for _ in range(1000):
            state.increment_clicks()
    
    import threading
    threads = [threading.Thread(target=increment_multiple) 
               for _ in range(10)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    assert state.get_click_count() == 10000  # All increments counted
```

### Integration Tests
```python
def test_click_loop_execution():
    """Test that click loop executes correct number of clicks."""
    state = ClickerState()
    state.set_running(True)
    
    # Run click loop
    app._click_loop(interval=10, count=100, button="left", 
                   randomization=0, pattern="linear")
    
    assert state.get_click_count() == 100
    assert not state.get_running()
```

### Manual Testing
1. Test each preset configuration
2. Verify hotkey activation globally
3. Test pause/resume functionality
4. Verify config persistence
5. Test sequence recording and playback

---

## Deployment Notes

### Single-File Distribution
Keep `kliker.py` and `clicker_state.py` together in same directory.

### Requirements
From `requirements.txt`:
- pynput>=1.7
- tkinter (built-in with Python)

###Installation
```bash
pip install -r requirements.txt
python kliker.py
```

### Packaging
For distribution as an executable:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed kliker.py
```

---

## Glossary

- **RLock:** Reentrant Lock - allows same thread to acquire lock multiple times
- **Race Condition:** When output depends on timing of thread execution
- **CPM:** Clicks Per Minute - metric for click rate
- **Hotkey:** Global keyboard shortcut that works across applications
- **Thread-Safe:** Can be safely accessed from multiple threads simultaneously

---

**Version:** 2.0  
**Status:** Production-Ready  
**Last Updated:** 2024  

