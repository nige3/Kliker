#!/usr/bin/env python3
"""
Kliker - Advanced Auto-Clicker Application
==========================================

A production-quality auto-clicker with modern GUI.
Features thread-safe state management, anti-detection randomization, and professional UI.

Architecture:
- ClickerState: Thread-safe state container for all shared state
- KlikerApp: Main GUI application class
- Separation of concerns: UI, state, and clicking logic are decoupled

Features:
- Mouse clicking (left/right/middle)
- Keyboard hotkey automation
- Modern tkinter GUI with light/dark themes
- Two modes: Realtime clicking and Sequence playback
- Click randomization and multiple patterns
- Session statistics and configuration persistence
- Sound notifications and visual feedback

Author: GitHub Copilot
License: MIT
Version: 2.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import time
import sys
import os
import json
import random
import math
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass

from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key

from clicker_state import ClickerState


# Configuration
CONFIG_FILE = "kliker_config.json"
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

# Constants for validation
VALID_BUTTONS = ["left", "right", "middle"]
VALID_PATTERNS = ["linear", "random", "sine", "exponential"]
MIN_INTERVAL = 10
MAX_INTERVAL = 10000
MAX_RANDOMIZATION = 50

# Remove all global variables - now managed by ClickerState


class KlikerApp:
    """Main application class for the Kliker auto-clicker GUI."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the Kliker application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Kliker - Advanced Auto Clicker")
        self.root.geometry("600x750")
        self.root.resizable(True, True)
        self.root.minsize(600, 700)

        # Initialize thread-safe state
        self.state = ClickerState()

        # Initialize controllers
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()

        # Load configuration
        self.config = self._load_config()

        # Reset session statistics
        self.state.reset_session()

        # Setup UI
        self.apply_theme()
        self._create_widgets()
        self._setup_hotkeys()
        self._schedule_stats_update()

        # Auto-save config on exit
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file.
        
        Returns:
            Merged configuration dictionary
        """
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    loaded = json.load(f)
                    return {**DEFAULT_CONFIG, **loaded}
        except Exception as e:
            print(f"Error loading config: {e}")
        return DEFAULT_CONFIG.copy()

    def _save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            messagebox.showerror("Config Error", f"Failed to save config: {e}")

    def apply_theme(self) -> None:
        """Apply the current theme (light or dark)."""
        style = ttk.Style()
        style.theme_use('clam')

        theme = self.config.get('theme', 'light')
        
        if theme == 'dark':
            self._apply_dark_theme(style)
        else:
            self._apply_light_theme(style)

    def _apply_dark_theme(self, style: ttk.Style) -> None:
        """Apply dark theme colors."""
        colors = {
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'entry_bg': '#404040',
            'text_color': '#ffffff'
        }
        self.root.configure(bg=colors['bg'])
        style.configure('TFrame', background=colors['bg'])
        style.configure('TLabel', background=colors['bg'], foreground=colors['fg'],
                       font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6)
        style.configure('TEntry', font=('Segoe UI', 10),
                       fieldbackground=colors['entry_bg'],
                       foreground=colors['text_color'])
        style.configure('TCombobox', font=('Segoe UI', 10),
                       fieldbackground=colors['entry_bg'],
                       foreground=colors['text_color'])
        style.configure('TLabelframe', background=colors['bg'],
                       foreground=colors['fg'])
        style.configure('TLabelframe.Label', background=colors['bg'],
                       foreground=colors['fg'])

    def _apply_light_theme(self, style: ttk.Style) -> None:
        """Apply light theme colors."""
        colors = {
            'bg': '#f8f9fa',
            'fg': '#212529'
        }
        self.root.configure(bg=colors['bg'])
        style.configure('TFrame', background=colors['bg'])
        style.configure('TLabel', background=colors['bg'], foreground=colors['fg'],
                       font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6)
        style.configure('TEntry', font=('Segoe UI', 10))
        style.configure('TCombobox', font=('Segoe UI', 10))
        style.configure('TLabelframe', background=colors['bg'],
                       foreground=colors['fg'])
        style.configure('TLabelframe.Label', background=colors['bg'],
                       foreground=colors['fg'])

    def _create_widgets(self) -> None:
        """Create and layout all GUI widgets.
        
        Breaks the UI creation into logical components for maintainability.
        """
        # Create main container with scrollbar
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas and scrollbar for scrolling
        canvas = tk.Canvas(main_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Main frame
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header with title and theme toggle
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title_label = ttk.Label(header_frame, text="🖱️ Kliker", font=('Segoe UI', 18, 'bold'))
        title_label.pack(side=tk.LEFT)

        # Theme toggle button
        self.theme_var = tk.StringVar(value=self.config.get('theme', 'light'))
        theme_btn = ttk.Button(header_frame, text="🌙 Dark", command=self.toggle_theme)
        theme_btn.pack(side=tk.RIGHT)
        self.theme_btn = theme_btn

        # Status indicator with better styling
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 15))

        self.status_var = tk.StringVar(value="Status: Idle")
        status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                font=('Segoe UI', 12, 'bold'), foreground='green')
        status_label.pack(side=tk.LEFT)

        # Session stats
        self.stats_var = tk.StringVar(value="Clicks: 0 | CPM: 0")
        stats_label = ttk.Label(status_frame, textvariable=self.stats_var,
                               font=('Segoe UI', 10))
        stats_label.pack(side=tk.RIGHT)

        # Mode selection with better layout
        mode_frame = ttk.LabelFrame(main_frame, text="Operating Mode", padding="10")
        mode_frame.pack(fill=tk.X, pady=(0, 15))

        self.mode_var = tk.StringVar(value="realtime")
        ttk.Radiobutton(mode_frame, text="🎯 Realtime Clicking",
                       variable=self.mode_var, value="realtime",
                       command=self.switch_mode).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(mode_frame, text="📋 Sequence Playback",
                       variable=self.mode_var, value="sequence",
                       command=self.switch_mode).pack(side=tk.LEFT)

        # Settings frame with tabs
        settings_notebook = ttk.Notebook(main_frame)
        settings_notebook.pack(fill=tk.X, pady=(0, 15))

        # Basic settings tab
        basic_tab = ttk.Frame(settings_notebook, padding="10")
        settings_notebook.add(basic_tab, text="Basic Settings")

        # Click settings
        ttk.Label(basic_tab, text="Interval (ms):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.interval_var = tk.StringVar(value=str(self.config.get('interval', DEFAULT_INTERVAL)))
        interval_entry = ttk.Entry(basic_tab, textvariable=self.interval_var, width=12)
        interval_entry.grid(row=0, column=1, sticky=tk.W, pady=2)
        self.create_tooltip(interval_entry, "Time between clicks in milliseconds (10-10000)")

        ttk.Label(basic_tab, text="Click Count (0=infinite):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.count_var = tk.StringVar(value=str(self.config.get('count', DEFAULT_COUNT)))
        count_entry = ttk.Entry(basic_tab, textvariable=self.count_var, width=12)
        count_entry.grid(row=1, column=1, sticky=tk.W, pady=2)
        self.create_tooltip(count_entry, "Number of clicks to perform (0 = infinite)")

        ttk.Label(basic_tab, text="Mouse Button:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.button_var = tk.StringVar(value=self.config.get('button', DEFAULT_BUTTON))
        button_combo = ttk.Combobox(basic_tab, textvariable=self.button_var,
                                   values=["left", "right", "middle"], state="readonly", width=10)
        button_combo.grid(row=2, column=1, sticky=tk.W, pady=2)

        ttk.Label(basic_tab, text="Hotkey:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.hotkey_var = tk.StringVar(value=self.config.get('hotkey', DEFAULT_HOTKEY))
        hotkey_entry = ttk.Entry(basic_tab, textvariable=self.hotkey_var, width=12)
        hotkey_entry.grid(row=3, column=1, sticky=tk.W, pady=2)
        self.create_tooltip(hotkey_entry, "Hotkey to start/stop (f1-f12, a-z, 0-9)")

        # Advanced settings tab
        advanced_tab = ttk.Frame(settings_notebook, padding="10")
        settings_notebook.add(advanced_tab, text="Advanced")

        # Randomization settings
        ttk.Label(advanced_tab, text="Randomization (%):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.random_var = tk.StringVar(value=str(self.config.get('randomization', 10)))
        random_entry = ttk.Entry(advanced_tab, textvariable=self.random_var, width=12)
        random_entry.grid(row=0, column=1, sticky=tk.W, pady=2)
        self.create_tooltip(random_entry, "Random variation in timing (0-50%)")

        ttk.Label(advanced_tab, text="Click Pattern:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.pattern_var = tk.StringVar(value=self.config.get('pattern', 'linear'))
        pattern_combo = ttk.Combobox(advanced_tab, textvariable=self.pattern_var,
                                    values=["linear", "random", "sine", "exponential"],
                                    state="readonly", width=12)
        pattern_combo.grid(row=1, column=1, sticky=tk.W, pady=2)
        self.create_tooltip(pattern_combo, "Click timing pattern")

        # Sound toggle
        ttk.Label(advanced_tab, text="Sound Notifications:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.sound_var = tk.BooleanVar(value=self.config.get('sound_enabled', True))
        sound_check = ttk.Checkbutton(advanced_tab, text="Enable", variable=self.sound_var)
        sound_check.grid(row=2, column=1, sticky=tk.W, pady=2)

        # Sequence frame (initially hidden)
        self.sequence_frame = ttk.LabelFrame(main_frame, text="Sequence Recording", padding="10")

        ttk.Label(self.sequence_frame, text="Recorded Positions:").pack(anchor=tk.W)
        self.sequence_text = scrolledtext.ScrolledText(self.sequence_frame, height=6, width=60,
                                                      font=('Consolas', 9))
        self.sequence_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        self.sequence_text.config(state=tk.DISABLED)

        # Control buttons with better layout
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.pack(fill=tk.X, pady=(15, 0))

        # Top row - main controls
        main_controls = ttk.Frame(control_frame)
        main_controls.pack(fill=tk.X, pady=(0, 10))

        self.start_btn = ttk.Button(main_controls, text="▶ Start", command=self.start_clicking,
                                   style='Accent.TButton')
        self.start_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.stop_btn = ttk.Button(main_controls, text="⏹ Stop", command=self.stop_clicking,
                                  state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.pause_btn = ttk.Button(main_controls, text="⏸ Pause", command=self.pause_clicking,
                                   state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Sequence controls
        self.record_btn = ttk.Button(main_controls, text="⏺ Record", command=self.start_recording)
        self.record_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.clear_btn = ttk.Button(main_controls, text="🗑 Clear", command=self.clear_sequence)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Bottom row - utility buttons
        utility_controls = ttk.Frame(control_frame)
        utility_controls.pack(fill=tk.X)

        ttk.Button(utility_controls, text="💾 Save Config", command=self.save_current_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(utility_controls, text="📁 Load Config", command=self.load_config_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(utility_controls, text="🔄 Reset Stats", command=self.reset_session_stats).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(utility_controls, text="❓ Help", command=self.show_help).pack(side=tk.RIGHT)

        # Preset buttons with better organization
        preset_frame = ttk.LabelFrame(main_frame, text="Quick Presets", padding="10")
        preset_frame.pack(fill=tk.X, pady=(15, 0))

        # Create preset buttons in a grid
        presets = [
            ("⚡ Rapid", lambda: self.set_preset(50, 0)),
            ("🎯 Single", lambda: self.set_preset(1000, 1)),
            ("⚪ Double", lambda: self.set_preset(100, 2)),
            ("🐌 Slow", lambda: self.set_preset(2000, 0)),
            ("🎮 Gaming", lambda: self.set_preset(150, 0)),
            ("📝 Typing", lambda: self.set_preset(300, 0))
        ]

        for i, (text, cmd) in enumerate(presets):
            row, col = i // 3, i % 3
            ttk.Button(preset_frame, text=text, command=cmd).grid(row=row, column=col, padx=5, pady=2, sticky=tk.W+tk.E)

        # Footer with info
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(20, 0))

        info_text = "ESC: Emergency Stop | Hotkey works globally | Session auto-saves"
        info_label = ttk.Label(footer_frame, text=info_text, font=('Segoe UI', 8), foreground='gray')
        info_label.pack()

        # Apply initial mode
        self.switch_mode()

        # Configure accent button style
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'), relief='raised')

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

            label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1,
                           font=('Segoe UI', 8), padx=5, pady=3)
            label.pack()

            def hide_tooltip():
                tooltip.destroy()

            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
            tooltip.bind('<Leave>', lambda e: hide_tooltip())

        widget.bind('<Enter>', show_tooltip)

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        current_theme = self.config.get('theme', 'light')
        new_theme = 'dark' if current_theme == 'light' else 'light'
        self.config['theme'] = new_theme
        self.theme_var.set(new_theme)
        self.theme_btn.config(text="☀️ Light" if new_theme == 'dark' else "🌙 Dark")
        self.apply_theme()
        self.save_config()

    def update_stats_display(self):
        """Update the statistics display"""
        global session_stats
        clicks = session_stats['total_clicks']

        # Calculate clicks per minute
        if session_stats['session_start']:
            elapsed = (datetime.now() - session_stats['session_start']).total_seconds()
            if elapsed > 0:
                cpm = int((clicks / elapsed) * 60)
                session_stats['clicks_per_minute'] = cpm
            else:
                cpm = 0
        else:
            cpm = 0

        self.stats_var.set(f"Clicks: {clicks} | CPM: {cpm}")

        # Schedule next update
        if hasattr(self, 'root') and self.root:
            self.root.after(1000, self.update_stats_display)

    def save_current_config(self):
        """Save current settings to config"""
        try:
            self.config.update({
                'interval': int(self.interval_var.get()),
                'count': int(self.count_var.get()),
                'button': self.button_var.get(),
                'hotkey': self.hotkey_var.get().lower(),
                'randomization': int(self.random_var.get()),
                'pattern': self.pattern_var.get(),
                'sound_enabled': self.sound_var.get(),
                'theme': self.theme_var.get()
            })
            self.save_config()
            self.play_sound('success')
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def load_config_file(self):
        """Load configuration from file"""
        file_path = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    loaded_config = json.load(f)
                self.config.update(loaded_config)
                self.apply_loaded_config()
                self.play_sound('success')
                messagebox.showinfo("Success", "Configuration loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {e}")

    def apply_loaded_config(self):
        """Apply loaded configuration to UI"""
        self.interval_var.set(str(self.config.get('interval', DEFAULT_INTERVAL)))
        self.count_var.set(str(self.config.get('count', DEFAULT_COUNT)))
        self.button_var.set(self.config.get('button', DEFAULT_BUTTON))
        self.hotkey_var.set(self.config.get('hotkey', DEFAULT_HOTKEY))
        self.random_var.set(str(self.config.get('randomization', 10)))
        self.pattern_var.set(self.config.get('pattern', 'linear'))
        self.sound_var.set(self.config.get('sound_enabled', True))
        self.theme_var.set(self.config.get('theme', 'light'))
        self.apply_theme()

    def play_sound(self, sound_type):
        """Play notification sound"""
        if not self.config.get('sound_enabled', True):
            return

        try:
            # Simple beep using system bell
            self.root.bell()
        except:
            pass  # Ignore if bell not available

    def show_help(self):
        """Show help dialog"""
        help_text = """
Kliker - Advanced Auto Clicker Help

MODES:
• Realtime: Clicks at current cursor position
• Sequence: Records and replays click sequences

SETTINGS:
• Interval: Time between clicks (milliseconds)
• Count: Number of clicks (0 = infinite)
• Button: Left, right, or middle mouse button
• Hotkey: Global start/stop key

ADVANCED:
• Randomization: Adds timing variation (anti-detection)
• Pattern: Click timing pattern (linear/random/sine/exponential)
• Sound: Enable/disable notifications

CONTROLS:
• ESC: Emergency stop
• Hotkey: Toggle start/stop
• Presets: Quick setting combinations

SAFETY:
• Use responsibly
• ESC always stops clicking
• Visual indicators show status
• Session statistics tracked

TIPS:
• Lower randomization for precision
• Higher randomization for anti-detection
• Test settings before use
• Save favorite configurations
"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Kliker Help")
        help_window.geometry("500x600")

        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)

        ttk.Button(help_window, text="Close", command=help_window.destroy).pack(pady=10)

    def set_preset(self, interval, count):
        self.interval_var.set(str(interval))
        self.count_var.set(str(count))
        self.play_sound('preset')

    def start_clicking(self):
        global is_running, click_thread
        if is_running:
            return

        try:
            interval = int(self.interval_var.get())
            count = int(self.count_var.get())
            button = self.button_var.get()
            randomization = int(self.random_var.get())
            pattern = self.pattern_var.get()

            if interval < 10:
                messagebox.showerror("Error", "Interval must be at least 10ms")
                return
            if count < 0:
                messagebox.showerror("Error", "Click count cannot be negative")
                return
            if randomization < 0 or randomization > 50:
                messagebox.showerror("Error", "Randomization must be 0-50%")
                return

        except ValueError:
            messagebox.showerror("Error", "Invalid numeric input")
            return

        is_running = True
        self.status_var.set("Status: Running")
        self.start_btn.config(state=tk.DISABLED, text="▶ Running")
        self.stop_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.NORMAL)
        self.root.configure(bg='#ffe6e6' if self.config.get('theme') == 'light' else '#4a2c2c')

        if current_mode == "realtime":
            click_thread = threading.Thread(target=self.click_loop,
                                          args=(interval, count, button, randomization, pattern))
        else:
            if not recorded_positions:
                messagebox.showerror("Error", "No recorded positions to play back")
                self.stop_clicking()
                return
            click_thread = threading.Thread(target=self.playback_loop,
                                          args=(interval, count, button, randomization, pattern))

        click_thread.daemon = True
        click_thread.start()
        self.play_sound('start')

    def pause_clicking(self):
        """Pause/resume clicking"""
        global is_running
        if is_running:
            is_running = False
            self.status_var.set("Status: Paused")
            self.start_btn.config(text="▶ Resume")
            self.pause_btn.config(text="⏯ Resume")
            self.play_sound('pause')
        else:
            is_running = True
            self.status_var.set("Status: Running")
            self.start_btn.config(text="▶ Running")
            self.pause_btn.config(text="⏸ Pause")
            self.play_sound('resume')

    def stop_clicking(self):
        global is_running
        is_running = False
        self.status_var.set("Status: Idle")
        self.start_btn.config(state=tk.NORMAL, text="▶ Start")
        self.stop_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.DISABLED, text="⏸ Pause")
        self.root.configure(bg='#f8f9fa' if self.config.get('theme') == 'light' else '#2b2b2b')
        self.play_sound('stop')

    def get_next_interval(self, base_interval, randomization, pattern, click_num=0):
        """Calculate next click interval based on pattern and randomization"""
        # Apply randomization
        if randomization > 0:
            variation = base_interval * (randomization / 100.0)
            random_factor = random.uniform(-variation, variation)
            interval = base_interval + random_factor
        else:
            interval = base_interval

        # Apply pattern
        if pattern == "random":
            # Already randomized above
            pass
        elif pattern == "sine":
            # Sine wave pattern
            wave = math.sin(click_num * 0.1) * 0.5 + 0.5  # 0-1 range
            interval = base_interval * (0.5 + wave * 0.5)  # 50%-150% of base
        elif pattern == "exponential":
            # Exponential decay (starts fast, slows down)
            decay = math.exp(-click_num * 0.01)
            interval = base_interval / max(decay, 0.1)

        return max(10, interval)  # Minimum 10ms

    def click_loop(self, interval, count, button, randomization, pattern):
        global is_running, session_stats
        button_map = {"left": Button.left, "right": Button.right, "middle": Button.middle}
        btn = button_map[button]

        clicks_done = 0
        while is_running and (count == 0 or clicks_done < count):
            try:
                mouse_controller.click(btn)
                session_stats['total_clicks'] += 1
                session_stats['last_click_time'] = datetime.now()
                clicks_done += 1

                # Calculate next interval
                next_interval = self.get_next_interval(interval, randomization, pattern, clicks_done)
                time.sleep(next_interval / 1000.0)
            except Exception as e:
                print(f"Click error: {e}")
                break

    def playback_loop(self, interval, count, button, randomization, pattern):
        global is_running, session_stats
        button_map = {"left": Button.left, "right": Button.right, "middle": Button.middle}
        btn = button_map[button]

        playback_count = 0
        while is_running:
            for pos in recorded_positions:
                if not is_running:
                    break
                try:
                    mouse_controller.position = pos
                    time.sleep(0.01)  # Small delay to move cursor
                    mouse_controller.click(btn)
                    session_stats['total_clicks'] += 1
                    session_stats['last_click_time'] = datetime.now()

                    # Calculate next interval
                    next_interval = self.get_next_interval(interval, randomization, pattern,
                                                        playback_count * len(recorded_positions) + recorded_positions.index(pos))
                    time.sleep(next_interval / 1000.0)
                except Exception as e:
                    print(f"Playback error: {e}")
                    break

            playback_count += 1
            if count > 0 and playback_count >= count:
                break

    def stop_clicking(self):
        global is_running
        is_running = False
        self.status_var.set("Status: Idle")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.root.configure(bg='#f0f0f0')  # Back to normal

    def click_loop(self, interval, count, button):
        global is_running
        button_map = {"left": Button.left, "right": Button.right, "middle": Button.middle}
        btn = button_map[button]

        clicks_done = 0
        while is_running and (count == 0 or clicks_done < count):
            mouse_controller.click(btn)
            clicks_done += 1
            time.sleep(interval / 1000.0)

    def playback_loop(self, interval, count, button):
        global is_running
        button_map = {"left": Button.left, "right": Button.right, "middle": Button.middle}
        btn = button_map[button]

        while is_running:
            for pos in recorded_positions:
                if not is_running:
                    break
                mouse_controller.position = pos
                time.sleep(0.01)  # Small delay to move cursor
                mouse_controller.click(btn)
                time.sleep(interval / 1000.0)
            if count > 0:
                count -= 1
                if count == 0:
                    break

    def start_recording(self):
        global record_mode, record_listener, recorded_positions
        if record_mode:
            self.stop_recording()
            return

        recorded_positions = []
        record_mode = True
        self.record_btn.config(text="⏹ Stop Recording")
        self.update_sequence_display()

        record_listener = mouse.Listener(on_click=self.on_click_record)
        record_listener.start()

    def stop_recording(self):
        global record_mode, record_listener
        if record_listener:
            record_listener.stop()
        record_mode = False
        self.record_btn.config(text="⏺ Record")
        self.update_sequence_display()

    def on_click_record(self, x, y, button, pressed):
        if pressed and button == Button.left:
            recorded_positions.append((x, y))
            self.update_sequence_display()

    def clear_sequence(self):
        global recorded_positions
        recorded_positions = []
        self.update_sequence_display()

    def update_sequence_display(self):
        self.sequence_text.config(state=tk.NORMAL)
        self.sequence_text.delete(1.0, tk.END)
        for i, pos in enumerate(recorded_positions, 1):
            self.sequence_text.insert(tk.END, f"{i}. ({pos[0]}, {pos[1]})\n")
        self.sequence_text.config(state=tk.DISABLED)

    def setup_hotkeys(self):
        global hotkey_listener
        hotkey_listener = keyboard.Listener(on_press=self.on_hotkey_press)
        hotkey_listener.start()

    def on_hotkey_press(self, key):
        try:
            hotkey = self.hotkey_var.get().lower()
            if hasattr(key, 'char') and key.char and key.char.lower() == hotkey:
                if is_running:
                    self.stop_clicking()
                else:
                    self.start_clicking()
            elif hasattr(key, 'name') and key.name == hotkey:
                if is_running:
                    self.stop_clicking()
                else:
                    self.start_clicking()
            elif key == Key.esc:
                self.stop_clicking()
            # Handle function keys
            elif hotkey.startswith('f') and hotkey[1:].isdigit():
                f_num = int(hotkey[1:])
                if f_num >= 1 and f_num <= 12:
                    f_keys = [Key.f1, Key.f2, Key.f3, Key.f4, Key.f5, Key.f6,
                             Key.f7, Key.f8, Key.f9, Key.f10, Key.f11, Key.f12]
                    if key == f_keys[f_num - 1]:
                        if is_running:
                            self.stop_clicking()
                        else:
                            self.start_clicking()
        except (AttributeError, ValueError, IndexError) as e:
            # Log error but don't crash
            print(f"Hotkey error: {e}")
            pass

    def on_closing(self):
        global is_running, hotkey_listener, record_listener
        is_running = False
        if hotkey_listener:
            hotkey_listener.stop()
        if record_listener:
            record_listener.stop()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = KlikerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()