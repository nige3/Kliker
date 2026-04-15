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


class KlikerApp:
    """Main application class for the Kliker auto-clicker GUI.
    
    Responsibilities:
    - GUI management and user interaction
    - Configuration persistence
    - Coordination between state and clicking logic
    """

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
        self.state.reset_session()

        # Initialize controllers
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()

        # Load configuration
        self.config = self._load_config()

        # UI variables
        self.status_var: Optional[tk.StringVar] = None
        self.stats_var: Optional[tk.StringVar] = None
        self.mode_var: Optional[tk.StringVar] = None
        self.theme_var: Optional[tk.StringVar] = None
        self.interval_var: Optional[tk.StringVar] = None
        self.count_var: Optional[tk.StringVar] = None
        self.button_var: Optional[tk.StringVar] = None
        self.hotkey_var: Optional[tk.StringVar] = None
        self.random_var: Optional[tk.StringVar] = None
        self.pattern_var: Optional[tk.StringVar] = None
        self.sound_var: Optional[tk.BooleanVar] = None

        # Button references
        self.start_btn: Optional[ttk.Button] = None
        self.stop_btn: Optional[ttk.Button] = None
        self.pause_btn: Optional[ttk.Button] = None
        self.record_btn: Optional[ttk.Button] = None
        self.clear_btn: Optional[ttk.Button] = None
        self.theme_btn: Optional[ttk.Button] = None

        # Widget references
        self.sequence_text: Optional[scrolledtext.ScrolledText] = None
        self.sequence_frame: Optional[ttk.LabelFrame] = None

        # Setup UI
        self.apply_theme()
        self._create_widgets()
        self._setup_hotkeys()
        self._schedule_stats_update()

        # Auto-save config on exit
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    # ========== Configuration Management ==========

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
            print(f"Warning: Failed to load config: {e}")
        return DEFAULT_CONFIG.copy()

    def _save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            messagebox.showerror("Config Error", f"Failed to save config: {e}")

    # ========== Theme Management ==========

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
        self.root.configure(bg='#2b2b2b')
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLabel', background='#2b2b2b', foreground='#ffffff',
                       font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6)
        style.configure('TEntry', font=('Segoe UI', 10),
                       fieldbackground='#404040', foreground='#ffffff')
        style.configure('TCombobox', font=('Segoe UI', 10),
                       fieldbackground='#404040', foreground='#ffffff')
        style.configure('TLabelframe', background='#2b2b2b', foreground='#ffffff')
        style.configure('TLabelframe.Label', background='#2b2b2b', foreground='#ffffff')

    def _apply_light_theme(self, style: ttk.Style) -> None:
        """Apply light theme colors."""
        self.root.configure(bg='#f8f9fa')
        style.configure('TFrame', background='#f8f9fa')
        style.configure('TLabel', background='#f8f9fa', foreground='#212529',
                       font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6)
        style.configure('TEntry', font=('Segoe UI', 10))
        style.configure('TCombobox', font=('Segoe UI', 10))
        style.configure('TLabelframe', background='#f8f9fa', foreground='#212529')
        style.configure('TLabelframe.Label', background='#f8f9fa', foreground='#212529')

    def toggle_theme(self) -> None:
        """Toggle between light and dark themes."""
        current_theme = self.config.get('theme', 'light')
        new_theme = 'dark' if current_theme == 'light' else 'light'
        self.config['theme'] = new_theme
        if self.theme_var:
            self.theme_var.set(new_theme)
        self.apply_theme()
        self._save_config()

    # ========== UI Creation ==========

    def _create_widgets(self) -> None:
        """Create and layout all GUI widgets using helper methods."""
        # Create main scrollable container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Setup scrolling
        canvas = tk.Canvas(main_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        canvas.bind_all("<MouseWheel>", 
                       lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Main frame
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create UI components
        self._create_header(main_frame)
        self._create_status_frame(main_frame)
        self._create_mode_selection(main_frame)
        self._create_settings_tabs(main_frame)
        self._create_sequence_frame(main_frame)
        self._create_control_buttons(main_frame)
        self._create_preset_buttons(main_frame)
        self._create_footer(main_frame)

        # Apply mode
        self.switch_mode()

        # Configure button styles
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'), relief='raised')

    def _create_header(self, parent: ttk.Frame) -> None:
        """Create header with title and theme toggle."""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(header_frame, text="🖱️ Kliker", 
                 font=('Segoe UI', 18, 'bold')).pack(side=tk.LEFT)

        self.theme_var = tk.StringVar(value=self.config.get('theme', 'light'))
        self.theme_btn = ttk.Button(header_frame, text="🌙 Dark", command=self.toggle_theme)
        self.theme_btn.pack(side=tk.RIGHT)

    def _create_status_frame(self, parent: ttk.Frame) -> None:
        """Create status indicator and statistics display."""
        status_frame = ttk.LabelFrame(parent, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 15))

        self.status_var = tk.StringVar(value="Status: Idle")
        ttk.Label(status_frame, textvariable=self.status_var,
                 font=('Segoe UI', 12, 'bold'),
                 foreground='green').pack(side=tk.LEFT)

        self.stats_var = tk.StringVar(value="Clicks: 0 | CPM: 0")
        ttk.Label(status_frame, textvariable=self.stats_var,
                 font=('Segoe UI', 10)).pack(side=tk.RIGHT)

    def _create_mode_selection(self, parent: ttk.Frame) -> None:
        """Create mode selection radio buttons."""
        mode_frame = ttk.LabelFrame(parent, text="Operating Mode", padding="10")
        mode_frame.pack(fill=tk.X, pady=(0, 15))

        self.mode_var = tk.StringVar(value="realtime")
        ttk.Radiobutton(mode_frame, text="🎯 Realtime Clicking",
                       variable=self.mode_var, value="realtime",
                       command=self.switch_mode).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(mode_frame, text="📋 Sequence Playback",
                       variable=self.mode_var, value="sequence",
                       command=self.switch_mode).pack(side=tk.LEFT)

    def _create_settings_tabs(self, parent: ttk.Frame) -> None:
        """Create tabbed settings interface."""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.X, pady=(0, 15))

        # Basic settings tab
        basic_tab = ttk.Frame(notebook, padding="10")
        notebook.add(basic_tab, text="Basic Settings")
        self._create_basic_settings(basic_tab)

        # Advanced settings tab
        advanced_tab = ttk.Frame(notebook, padding="10")
        notebook.add(advanced_tab, text="Advanced")
        self._create_advanced_settings(advanced_tab)

    def _create_basic_settings(self, parent: ttk.Frame) -> None:
        """Create basic settings controls."""
        # Interval
        ttk.Label(parent, text="Interval (ms):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.interval_var = tk.StringVar(value=str(self.config.get('interval', 100)))
        interval_entry = ttk.Entry(parent, textvariable=self.interval_var, width=12)
        interval_entry.grid(row=0, column=1, sticky=tk.W, pady=2)
        self._create_tooltip(interval_entry, "Time between clicks (10-10000ms)")

        # Count
        ttk.Label(parent, text="Click Count (0=infinite):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.count_var = tk.StringVar(value=str(self.config.get('count', 0)))
        count_entry = ttk.Entry(parent, textvariable=self.count_var, width=12)
        count_entry.grid(row=1, column=1, sticky=tk.W, pady=2)
        self._create_tooltip(count_entry, "Number of clicks (0 = infinite)")

        # Button
        ttk.Label(parent, text="Mouse Button:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.button_var = tk.StringVar(value=self.config.get('button', 'left'))
        button_combo = ttk.Combobox(parent, textvariable=self.button_var,
                                   values=VALID_BUTTONS, state="readonly", width=10)
        button_combo.grid(row=2, column=1, sticky=tk.W, pady=2)

        # Hotkey
        ttk.Label(parent, text="Hotkey:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.hotkey_var = tk.StringVar(value=self.config.get('hotkey', 'f6'))
        hotkey_entry = ttk.Entry(parent, textvariable=self.hotkey_var, width=12)
        hotkey_entry.grid(row=3, column=1, sticky=tk.W, pady=2)
        self._create_tooltip(hotkey_entry, "Global hotkey (f1-f12, a-z, 0-9)")

    def _create_advanced_settings(self, parent: ttk.Frame) -> None:
        """Create advanced settings controls."""
        # Randomization
        ttk.Label(parent, text="Randomization (%):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.random_var = tk.StringVar(value=str(self.config.get('randomization', 10)))
        random_entry = ttk.Entry(parent, textvariable=self.random_var, width=12)
        random_entry.grid(row=0, column=1, sticky=tk.W, pady=2)
        self._create_tooltip(random_entry, "Timing variation for anti-detection (0-50%)")

        # Pattern
        ttk.Label(parent, text="Click Pattern:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.pattern_var = tk.StringVar(value=self.config.get('pattern', 'linear'))
        pattern_combo = ttk.Combobox(parent, textvariable=self.pattern_var,
                                    values=VALID_PATTERNS, state="readonly", width=12)
        pattern_combo.grid(row=1, column=1, sticky=tk.W, pady=2)
        self._create_tooltip(pattern_combo, "Click timing pattern")

        # Sound
        ttk.Label(parent, text="Sound Notifications:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.sound_var = tk.BooleanVar(value=self.config.get('sound_enabled', True))
        ttk.Checkbutton(parent, text="Enable", variable=self.sound_var).grid(
            row=2, column=1, sticky=tk.W, pady=2)

    def _create_sequence_frame(self, parent: ttk.Frame) -> None:
        """Create sequence recording display frame."""
        self.sequence_frame = ttk.LabelFrame(parent, text="Sequence Recording", padding="10")

        ttk.Label(self.sequence_frame, text="Recorded Positions:").pack(anchor=tk.W)
        self.sequence_text = scrolledtext.ScrolledText(
            self.sequence_frame, height=6, width=60, font=('Consolas', 9))
        self.sequence_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        self.sequence_text.config(state=tk.DISABLED)

    def _create_control_buttons(self, parent: ttk.Frame) -> None:
        """Create main control buttons."""
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.pack(fill=tk.X, pady=(15, 0))

        # Main controls
        main_controls = ttk.Frame(control_frame)
        main_controls.pack(fill=tk.X, pady=(0, 10))

        self.start_btn = ttk.Button(main_controls, text="▶ Start",
                                   command=self.start_clicking, style='Accent.TButton')
        self.start_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.stop_btn = ttk.Button(main_controls, text="⏹ Stop",
                                  command=self.stop_clicking, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.pause_btn = ttk.Button(main_controls, text="⏸ Pause",
                                   command=self.pause_clicking, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.record_btn = ttk.Button(main_controls, text="⏺ Record",
                                    command=self.start_recording)
        self.record_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.clear_btn = ttk.Button(main_controls, text="🗑 Clear",
                                   command=self.clear_sequence)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Utility controls
        utility_controls = ttk.Frame(control_frame)
        utility_controls.pack(fill=tk.X)

        ttk.Button(utility_controls, text="💾 Save Config",
                  command=self.save_current_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(utility_controls, text="📁 Load Config",
                  command=self.load_config_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(utility_controls, text="🔄 Reset Stats",
                  command=self.reset_session_stats).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(utility_controls, text="❓ Help",
                  command=self.show_help).pack(side=tk.RIGHT)

    def _create_preset_buttons(self, parent: ttk.Frame) -> None:
        """Create quick preset buttons."""
        preset_frame = ttk.LabelFrame(parent, text="Quick Presets", padding="10")
        preset_frame.pack(fill=tk.X, pady=(15, 0))

        presets = [
            ("⚡ Rapid", 50, 0),
            ("🎯 Single", 1000, 1),
            ("⚪ Double", 100, 2),
            ("🐌 Slow", 2000, 0),
            ("🎮 Gaming", 150, 0),
            ("📝 Typing", 300, 0)
        ]

        for i, (label, interval, count) in enumerate(presets):
            row, col = i // 3, i % 3
            ttk.Button(preset_frame, text=label,
                      command=lambda intv=interval, cnt=count: self.set_preset(intv, cnt)
                      ).grid(row=row, column=col, padx=5, pady=2, sticky=tk.W+tk.E)

    def _create_footer(self, parent: ttk.Frame) -> None:
        """Create footer with usage information."""
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(fill=tk.X, pady=(20, 0))

        info_text = "ESC: Emergency Stop | Hotkey works globally | Session auto-saves"
        ttk.Label(footer_frame, text=info_text, font=('Segoe UI', 8),
                 foreground='gray').pack()

    def _create_tooltip(self, widget: tk.Widget, text: str) -> None:
        """Create a tooltip for a widget.
        
        Args:
            widget: The widget to attach the tooltip to
            text: The tooltip text
        """
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

            label = tk.Label(tooltip, text=text, background="#ffffe0",
                           relief="solid", borderwidth=1,
                           font=('Segoe UI', 8), padx=5, pady=3)
            label.pack()

            def hide_tooltip():
                try:
                    tooltip.destroy()
                except:
                    pass

            widget.bind('<Leave>', lambda e: hide_tooltip())
            tooltip.bind('<Leave>', lambda e: hide_tooltip())

        widget.bind('<Enter>', show_tooltip)

    # ========== Settings Management ==========

    def switch_mode(self) -> None:
        """Switch between realtime and sequence modes."""
        if not self.mode_var or not self.sequence_frame:
            return

        mode = self.mode_var.get()
        self.state.current_mode = mode

        if mode == "sequence":
            self.sequence_frame.pack(fill=tk.X, pady=(15, 0), before=self.sequence_frame)
            if self.record_btn and self.clear_btn:
                self.record_btn.config(state=tk.NORMAL)
                self.clear_btn.config(state=tk.NORMAL)
        else:
            self.sequence_frame.pack_forget()
            if self.record_btn and self.clear_btn:
                self.record_btn.config(state=tk.DISABLED)
                self.clear_btn.config(state=tk.DISABLED)

    def set_preset(self, interval: int, count: int) -> None:
        """Set preset configuration.
        
        Args:
            interval: Click interval in milliseconds
            count: Number of clicks
        """
        if self.interval_var and self.count_var:
            self.interval_var.set(str(interval))
            self.count_var.set(str(count))
        self._play_sound('preset')

    def save_current_config(self) -> None:
        """Save current settings to config file."""
        try:
            if not all([self.interval_var, self.count_var, self.button_var,
                       self.hotkey_var, self.random_var, self.pattern_var,
                       self.sound_var]):
                raise ValueError("UI variables not initialized")

            self.config.update({
                'interval': int(self.interval_var.get()),
                'count': int(self.count_var.get()),
                'button': self.button_var.get(),
                'hotkey': self.hotkey_var.get().lower(),
                'randomization': int(self.random_var.get()),
                'pattern': self.pattern_var.get(),
                'sound_enabled': self.sound_var.get(),
                'theme': self.theme_var.get() if self.theme_var else 'light'
            })
            self._save_config()
            self._play_sound('success')
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

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
                self._play_sound('success')
                messagebox.showinfo("Success", "Configuration loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {e}")

    def _apply_loaded_config(self) -> None:
        """Apply loaded configuration to UI variables."""
        if all([self.interval_var, self.count_var, self.button_var,
               self.hotkey_var, self.random_var, self.pattern_var,
               self.sound_var, self.theme_var]):
            self.interval_var.set(str(self.config.get('interval', 100)))
            self.count_var.set(str(self.config.get('count', 0)))
            self.button_var.set(self.config.get('button', 'left'))
            self.hotkey_var.set(self.config.get('hotkey', 'f6'))
            self.random_var.set(str(self.config.get('randomization', 10)))
            self.pattern_var.set(self.config.get('pattern', 'linear'))
            self.sound_var.set(self.config.get('sound_enabled', True))
            self.theme_var.set(self.config.get('theme', 'light'))
            self.apply_theme()

    def reset_session_stats(self) -> None:
        """Reset session statistics."""
        self.state.reset_session()
        self._update_stats_display()

    # ========== Stats Management ==========

    def _schedule_stats_update(self) -> None:
        """Schedule periodic statistics updates."""
        self._update_stats_display()

    def _update_stats_display(self) -> None:
        """Update statistics display."""
        if not self.stats_var:
            return

        stats = self.state.get_stats_snapshot()
        clicks = stats['total_clicks']
        cpm = stats['clicks_per_minute']

        self.stats_var.set(f"Clicks: {clicks} | CPM: {cpm:.1f}")

        # Schedule next update
        if self.root:
            self.root.after(1000, self._update_stats_display)

    # ========== Clicking Logic ==========

    def _validate_input(self) -> Tuple[bool, Optional[str]]:
        """Validate user input before clicking.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            if not all([self.interval_var, self.count_var, self.random_var]):
                return False, "UI variables not initialized"

            interval = int(self.interval_var.get())
            count = int(self.count_var.get())
            randomization = int(self.random_var.get())

            if interval < MIN_INTERVAL or interval > MAX_INTERVAL:
                return False, f"Interval must be {MIN_INTERVAL}-{MAX_INTERVAL}ms"
            if count < 0:
                return False, "Click count cannot be negative"
            if randomization < 0 or randomization > MAX_RANDOMIZATION:
                return False, f"Randomization must be 0-{MAX_RANDOMIZATION}%"

            return True, None
        except ValueError as e:
            return False, f"Invalid numeric input: {e}"

    def start_clicking(self) -> None:
        """Start clicking with current configuration."""
        if self.state.get_running():
            return

        is_valid, error = self._validate_input()
        if not is_valid:
            messagebox.showerror("Error", error or "Unknown error")
            return

        try:
            interval = int(self.interval_var.get())  # type: ignore
            count = int(self.count_var.get())  # type: ignore
            button = self.button_var.get()  # type: ignore
            randomization = int(self.random_var.get())  # type: ignore
            pattern = self.pattern_var.get()  # type: ignore
            mode = self.state.current_mode

            # Check mode-specific requirements
            if mode == "sequence" and self.state.get_positions_count() == 0:
                messagebox.showerror("Error", "No recorded positions to play back")
                return

            # Start clicking
            self.state.set_running(True)
            if self.status_var:
                self.status_var.set("Status: Running")
            if self.start_btn:
                self.start_btn.config(state=tk.DISABLED, text="▶ Running")
            if self.stop_btn:
                self.stop_btn.config(state=tk.NORMAL)
            if self.pause_btn:
                self.pause_btn.config(state=tk.NORMAL)

            # Update UI background
            bg_color = '#ffe6e6' if self.config.get('theme') == 'light' else '#4a2c2c'
            self.root.configure(bg=bg_color)

            # Create and start click thread
            if mode == "realtime":
                thread = threading.Thread(
                    target=self._click_loop,
                    args=(interval, count, button, randomization, pattern),
                    daemon=True
                )
            else:
                thread = threading.Thread(
                    target=self._playback_loop,
                    args=(interval, count, button, randomization, pattern),
                    daemon=True
                )

            self.state.set_click_thread(thread)
            thread.start()
            self._play_sound('start')

        except Exception as e:
            self.state.set_running(False)
            messagebox.showerror("Error", f"Failed to start clicking: {e}")

    def pause_clicking(self) -> None:
        """Pause or resume clicking."""
        if not self.pause_btn or not self.status_var or not self.start_btn:
            return

        if self.state.get_running():
            self.state.set_running(False)
            self.status_var.set("Status: Paused")
            self.start_btn.config(text="▶ Resume")
            self.pause_btn.config(text="⏯ Resume")
            self._play_sound('pause')
        else:
            self.state.set_running(True)
            self.status_var.set("Status: Running")
            self.start_btn.config(text="▶ Running")
            self.pause_btn.config(text="⏸ Pause")
            self._play_sound('resume')

    def stop_clicking(self) -> None:
        """Stop clicking."""
        self.state.set_running(False)

        if self.status_var:
            self.status_var.set("Status: Idle")
        if self.start_btn:
            self.start_btn.config(state=tk.NORMAL, text="▶ Start")
        if self.stop_btn:
            self.stop_btn.config(state=tk.DISABLED)
        if self.pause_btn:
            self.pause_btn.config(state=tk.DISABLED, text="⏸ Pause")

        bg_color = '#f8f9fa' if self.config.get('theme') == 'light' else '#2b2b2b'
        self.root.configure(bg=bg_color)

        self._play_sound('stop')

    def _get_next_interval(self, base: int, randomization: int, pattern: str,
                          click_num: int = 0) -> float:
        """Calculate next click interval based on pattern and randomization.
        
        Args:
            base: Base interval in milliseconds
            randomization: Randomization percentage
            pattern: Pattern type (linear, random, sine, exponential)
            click_num: Current click number
            
        Returns:
            Next interval in milliseconds
        """
        # Apply randomization
        if randomization > 0:
            variation = base * (randomization / 100.0)
            random_factor = random.uniform(-variation, variation)
            interval = base + random_factor
        else:
            interval = base

        # Apply pattern
        if pattern == "sine":
            wave = math.sin(click_num * 0.1) * 0.5 + 0.5
            interval = base * (0.5 + wave * 0.5)
        elif pattern == "exponential":
            decay = math.exp(-click_num * 0.01)
            interval = base / max(decay, 0.1)

        return max(MIN_INTERVAL, interval)

    def _click_loop(self, interval: int, count: int, button: str,
                   randomization: int, pattern: str) -> None:
        """Perform clicking loop in realtime mode.
        
        Args:
            interval: Click interval in milliseconds
            count: Number of clicks (0 = infinite)
            button: Mouse button
            randomization: Randomization percentage
            pattern: Click pattern
        """
        button_map = {
            "left": Button.left,
            "right": Button.right,
            "middle": Button.middle
        }
        btn = button_map[button]

        clicks_done = 0
        try:
            while self.state.get_running() and (count == 0 or clicks_done < count):
                self.mouse_controller.click(btn)
                self.state.increment_clicks()
                clicks_done += 1

                next_interval = self._get_next_interval(interval, randomization, pattern, clicks_done)
                time.sleep(next_interval / 1000.0)
        except Exception as e:
            print(f"Error in click loop: {e}")
        finally:
            self.stop_clicking()

    def _playback_loop(self, interval: int, count: int, button: str,
                      randomization: int, pattern: str) -> None:
        """Perform sequence playback.
        
        Args:
            interval: Click interval in milliseconds
            count: Number of playback cycles
            button: Mouse button
            randomization: Randomization percentage
            pattern: Click pattern
        """
        button_map = {
            "left": Button.left,
            "right": Button.right,
            "middle": Button.middle
        }
        btn = button_map[button]

        playback_count = 0
        positions = self.state.get_positions()

        try:
            while self.state.get_running():
                for pos in positions:
                    if not self.state.get_running():
                        break

                    self.mouse_controller.position = pos
                    time.sleep(0.01)
                    self.mouse_controller.click(btn)
                    self.state.increment_clicks()

                    next_interval = self._get_next_interval(
                        interval, randomization, pattern,
                        playback_count * len(positions) + positions.index(pos)
                    )
                    time.sleep(next_interval / 1000.0)

                playback_count += 1
                if count > 0 and playback_count >= count:
                    break
        except Exception as e:
            print(f"Error in playback loop: {e}")
        finally:
            self.stop_clicking()

    # ========== Recording Logic ==========

    def start_recording(self) -> None:
        """Start recording click positions."""
        self.state.clear_positions()
        self.state.set_record_mode(True)

        if self.record_btn:
            self.record_btn.config(text="⏹ Stop Recording")

        # Create mouse listener
        def on_click(x, y, button, pressed):
            if pressed and button == Button.left and self.state.get_record_mode():
                self.state.add_position(x, y)
                self._update_sequence_display()

        listener = mouse.Listener(on_click=on_click)
        self.state.set_record_listener(listener)
        listener.start()

    def stop_recording(self) -> None:
        """Stop recording click positions."""
        self.state.set_record_mode(False)

        listener = self.state.get_record_listener()
        if listener:
            listener.stop()
            self.state.set_record_listener(None)

        if self.record_btn:
            self.record_btn.config(text="⏺ Record")

        self._update_sequence_display()

    def clear_sequence(self) -> None:
        """Clear recorded positions."""
        if messagebox.askyesno("Confirm", "Clear all recorded positions?"):
            self.state.clear_positions()
            self._update_sequence_display()

    def _update_sequence_display(self) -> None:
        """Update sequence display with recorded positions."""
        if not self.sequence_text:
            return

        self.sequence_text.config(state=tk.NORMAL)
        self.sequence_text.delete(1.0, tk.END)

        positions = self.state.get_positions()
        for i, (x, y) in enumerate(positions, 1):
            self.sequence_text.insert(tk.END, f"{i}. ({x}, {y})\n")

        self.sequence_text.config(state=tk.DISABLED)

    # ========== Hotkey Management ==========

    def _setup_hotkeys(self) -> None:
        """Setup global hotkey listener."""
        def on_press(key):
            self._handle_hotkey(key)

        listener = keyboard.Listener(on_press=on_press)
        self.state.set_hotkey_listener(listener)
        listener.start()

    def _handle_hotkey(self, key) -> None:
        """Handle hotkey press.
        
        Args:
            key: The pressed key
        """
        try:
            if not self.hotkey_var:
                return

            hotkey = self.hotkey_var.get().lower()

            # Check if hotkey was pressed
            key_matches = False
            if hasattr(key, 'char') and key.char and key.char.lower() == hotkey:
                key_matches = True
            elif hasattr(key, 'name') and key.name == hotkey:
                key_matches = True
            elif hotkey.startswith('f') and hotkey[1:].isdigit():
                # Handle function keys
                f_num = int(hotkey[1:])
                if 1 <= f_num <= 12:
                    f_keys = [Key.f1, Key.f2, Key.f3, Key.f4, Key.f5, Key.f6,
                             Key.f7, Key.f8, Key.f9, Key.f10, Key.f11, Key.f12]
                    if key == f_keys[f_num - 1]:
                        key_matches = True

            # Toggle clicking
            if key_matches:
                if self.state.get_running():
                    self.stop_clicking()
                else:
                    self.start_clicking()

            # Emergency stop
            elif key == Key.esc:
                self.stop_clicking()

        except (AttributeError, ValueError, IndexError) as e:
            print(f"Hotkey error: {e}")

    # ========== UI Utilities ==========

    def _play_sound(self, sound_type: str) -> None:
        """Play notification sound.
        
        Args:
            sound_type: Type of sound to play
        """
        if not self.config.get('sound_enabled', True):
            return

        try:
            self.root.bell()
        except:
            pass  # Ignore if bell not available

    def show_help(self) -> None:
        """Show help dialog."""
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
• Randomization: Timing variation (anti-detection)
• Pattern: Click timing pattern
• Sound: Enable/disable notifications

CONTROLS:
• ESC: Emergency stop (always works)
• Hotkey: Start/stop toggle
• Presets: Quick configurations

SAFETY:
• Use responsibly
• Test before using in important tasks
• ESC always stops clicking
• Session saved automatically

RECORDING:
1. Select "Sequence Playback" mode
2. Click "Record"
3. Click positions on screen
4. Click "Stop Recording"
5. Click "Start" to playback
"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Kliker Help")
        help_window.geometry("500x600")

        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)

        ttk.Button(help_window, text="Close", command=help_window.destroy).pack(pady=10)

    def _on_closing(self) -> None:
        """Handle window closing."""
        try:
            self.stop_clicking()

            # Stop listeners
            hotkey_listener = self.state.get_hotkey_listener()
            if hotkey_listener:
                hotkey_listener.stop()

            record_listener = self.state.get_record_listener()
            if record_listener:
                record_listener.stop()

            # Save config
            self._save_config()
        except Exception as e:
            print(f"Error on closing: {e}")
        finally:
            self.root.destroy()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = KlikerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
