# Kliker 2.0 - Quick Start Guide

## Installation & Setup

### Requirements
- Python 3.8 or higher
- tkinter (included with Python)
- Dependencies from `requirements.txt`

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python kliker.py
```

---

## First-Time Setup

1. **Launch the Application**
   ```bash
   python kliker.py
   ```

2. **Configure Basic Settings**
   - Interval: Time between clicks (ms) - Default: 100ms
   - Count: Number of clicks (0 = infinite) - Default: 0
   - Button: Left, Right, or Middle mouse button - Default: Left
   - Hotkey: Global start/stop shortcut - Default: f6

3. **Choose Your Mode**
   - **🎯 Realtime Clicking** - Click at current cursor position
   - **📋 Sequence Playback** - Record and replay specific positions

4. **Save Configuration**
   - Click "💾 Save Config" to create `kliker_config.json`
   - Settings auto-load on next startup

---

## Usage Modes

### Realtime Clicking
Perfect for continuous clicking at the current mouse position.

**Steps:**
1. Select "🎯 Realtime Clicking" mode
2. Set interval and button preferences
3. Position your mouse where you want clicks
4. Click "▶ Start" or press your hotkey
5. Click "⏹ Stop" or press ESC to stop

**Example:** Clicking buttons in a game 100 times at 100ms intervals
```
Interval: 100ms
Count: 100
Button: Left
Pattern: Linear
```

### Sequence Playback
Record specific positions and play them back automatically.

**Steps:**
1. Select "📋 Sequence Playback" mode
2. Click "⏺ Record" to start recording
3. Click the positions you want to automate
4. Click "⏹ Stop Recording" when done
5. Click "▶ Start" to play back the sequence
6. Adjust interval/count to control playback speed

**Example:** Submitting a form by clicking multiple fields
```
1. Click username field
2. (Type username - recorded positions)
3. Click password field
4. (Type password - recorded positions)
5. Click submit button
Playback starts from position 1 of the recorded positions
```

---

## Advanced Features

### Click Patterns
Adjust timing to avoid detection patterns:

- **Linear** - Consistent spacing (default)
- **Random** - Random variation each click
- **Sine** - Smooth wave pattern
- **Exponential** - Starts fast, slows down

### Randomization
Add timing variation to appear more natural:

- Range: 0-50% of base interval
- Useful for anti-detection
- Example: 100ms ± 10ms = 90-110ms clicks

### Theme Support
- **Light Theme** - Standard appearance
- **Dark Theme** - Easier on the eyes
- Auto-applies to all UI elements

### Quick Presets
One-click configurations:
- ⚡ **Rapid** - 50ms interval (fast)
- 🎯 **Single** - 1 click, 1000ms
- ⚪ **Double** - 100ms, 2 clicks
- 🐌 **Slow** - 2000ms interval (slow)
- 🎮 **Gaming** - 150ms (typical game)
- 📝 **Typing** - 300ms (text-like)

---

## Configuration File

Auto-created as `kliker_config.json`:

```json
{
  "interval": 100,
  "count": 0,
  "button": "left",
  "hotkey": "f6",
  "randomization": 10,
  "pattern": "linear",
  "sound_enabled": true,
  "theme": "light"
}
```

**To load a saved config:**
1. Click "📁 Load Config"
2. Select your JSON file
3. Settings apply immediately

---

## Hotkey Usage

### Default Hotkey: F6
- **Press F6** - Start/stop toggle
- **Press ESC** - Emergency stop (always works)

### Customize Hotkey
1. Go to "Basic Settings" tab
2. Change "Hotkey" field (examples: `f1`, `a`, `space`)
3. Click "💾 Save Config"

**Valid hotkeys:** f1-f12, a-z, 0-9

**In Sequence Mode:**
- While recording, press hotkey to start/stop
- Recording accepts mouse clicks, not keyboard

---

## Statistics & Monitoring

**Live Display Shows:**
- **Status** - Idle, Running, or Paused
- **Clicks** - Total clicks in session
- **CPM** - Clicks Per Minute rate

**To Reset Statistics:**
1. Click "🔄 Reset Stats"
2. Confirms session stats are cleared
3. Useful between test runs

---

## Safety Features

### Emergency Stop
- **Press ESC anytime** - Terminates clicking immediately
- Works even if application is minimized
- Press ESC again to resume pattern (if paused)

### Input Validation
- Invalid intervals rejected with error message
- Click count must be non-negative
- Randomization 0-50%
- Prevents invalid configurations

### Resource Cleanup
- Automatic listener shutdown on exit
- No orphaned threads left running
- Config auto-saves before closing

---

## Troubleshooting

### "No imported module named 'pynput'"
```bash
pip install pynput
```

### "tkinter not found"
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk

# Windows - Already included with Python
```

### Hotkey doesn't work
- Check hotkey format (f6, not F6)
- Ensure not conflicting with system shortcuts
- Close and restart application
- Try a different hotkey

### Clicking not starting
- Check if count is not zero and reached
- Verify interval is between 10-10000ms
- Look for error message dialog
- Try clicking "▶ Start" again

### Configuration not saving
- Check disk space available
- Verify directory is writable
- Check file permissions
- Try "💾 Save Config" manually

---

## Best Practices

### For Reliability
1. Test with small click counts first
2. Use "⏸ Pause" to test timing
3. Save multiple configurations
4. Keep randomization moderate (10-20%)

### For Anti-Detection
1. Use 10-30% randomization
2. Alternate patterns (random + sine)
3. Vary intervals between sessions
4. Add delays between sequences

### For Accuracy
1. Record sequences on target resolution
2. Use realtime for single positions
3. Test on target application
4. Verify with small count first

---

## Common Use Cases

### Use Case: Auto-Clicker for Games
```
Mode: Realtime
Interval: 150ms
Count: 0 (infinite)
Pattern: Random
Randomization: 15%
Hotkey: f6
```

### Use Case: Automated Form Filling
```
Mode: Sequence
Record all form field positions
Interval: 300ms
Count: 0 (infinite)
Pattern: Linear
```

### Use Case: Rapid Testing
```
Mode: Realtime
Interval: 50ms
Count: 1000
Pattern: Linear
Randomization: 0%
```

### Use Case: Soft, Natural Clicking
```
Mode: Realtime
Interval: 500ms
Count: 100
Pattern: Sine
Randomization: 25%
```

---

## Tips and Tricks

### Pause Between Clicks
- Increase interval value
- Use a slower preset
- Randomization adds natural variation

### Record Better Sequences
- Move cursor away before recording
- Click slowly for better timing
- Review/edit sequence in text view
- Start recording after positioning

### Find Your Intervals
- Use "Single" preset for 1 click
- Add ⏸ Pause button to test timing
- Adjust until feels natural
- Save as custom preset

### Avoid Detection
- Mix randomization patterns
- Vary intervals (sine pattern)
- Add longer pauses between sequences
- Use natural timings (150-500ms)

---

## Keyboard Shortcut Summary

| Key | Action |
|-----|--------|
| F6 | Start/Stop (default hotkey) |
| ESC | Emergency Stop (always) |
| Tab | Navigate between fields |
| Enter | Active button action |

---

## Getting Help

### Built-in Help
- Click "❓ Help" button for detailed guide
- Hover over fields for tooltips
- Check status messages for errors

### Configuration Issues
1. Delete `kliker_config.json` for fresh start
2. Restart application
3. Reconfigure settings
4. Click "💾 Save Config"

### Feature Requests
- Document desired feature
- Check REFACTORING_REPORT.md for future enhancements
- File GitHub issue with use case

---

## Advanced Configuration

### Manual JSON Editing
Edit `kliker_config.json` directly for:
- Custom patterns
- Server defaults for deployment
- Team configurations

**Example:**
```json
{
  "interval": 100,
  "count": 25,
  "button": "right",
  "hotkey": "f8",
  "randomization": 20,
  "pattern": "sine",
  "sound_enabled": false,
  "theme": "dark"
}
```

### Loading From Command Line
```bash
python kliker.py
# Then use "📁 Load Config" button
```

---

## Performance Notes

- **Minimum Interval:** 10ms (CPU intensive)
- **Recommended:** 50-500ms
- **System Impact:** Low (<1% per click thread)
- **Memory Usage:** ~50-100MB
- **Network:** No network access required

---

## Support Matrix

| Feature | Status | Notes |
|---------|--------|-------|
| Windows | ✅ | Full support |
| macOS | ✅ | Full support |
| Linux | ✅ | Requires X11/Wayland |
| Python 3.8 | ✅ | Minimum version |
| Python 3.11+ | ✅ | Recommended |
| threading | ✅ | Multi-threaded safe |
| Dark Mode | ✅ | Full support |

---

## License

Kliker is provided as-is for educational and authorized use only.
See LICENSE file for details.

---

**Version:** 2.0  
**Last Updated:** 2024  
**Status:** Production-Ready  

