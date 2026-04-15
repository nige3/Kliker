#!/usr/bin/env python3
"""
Kliker - A Modern Auto-Clicker Application
==========================================

A production-quality auto-clicker with GUI, inspired by Blur AutoClicker.
Supports mouse clicking automation and keyboard hotkeys with global control.

Features:
- Mouse clicking (left/right/middle)
- Keyboard hotkey automation
- Clean, modern GUI with tkinter
- Start/stop/toggle with visual feedback
- Global hotkey detection
- Configurable intervals and counts
- Safety features (ESC to stop)
- Two modes: Realtime clicking and Sequence playback

Author: GitHub Copilot
License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import sys
import os
from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode
import json

# Global variables
is_running = False
click_thread = None
hotkey_listener = None
mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()
recorded_positions = []
current_mode = "realtime"  # "realtime" or "sequence"
record_mode = False
record_listener = None

# Default settings
DEFAULT_INTERVAL = 100  # ms
DEFAULT_COUNT = 0  # 0 = infinite
DEFAULT_BUTTON = "left"
DEFAULT_HOTKEY = "f6"

class KlikerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kliker - Auto Clicker")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # Set modern theme
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors
        self.root.configure(bg='#f0f0f0')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=5)
        style.configure('TEntry', font=('Arial', 10))
        style.configure('TCombobox', font=('Arial', 10))

        self.create_widgets()
        self.setup_hotkeys()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="🖱️ Kliker", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))

        # Status indicator
        self.status_var = tk.StringVar(value="Status: Idle")
        status_label = ttk.Label(main_frame, textvariable=self.status_var,
                                font=('Arial', 12, 'bold'), foreground='green')
        status_label.pack(pady=(0, 20))

        # Mode selection
        mode_frame = ttk.LabelFrame(main_frame, text="Mode", padding="10")
        mode_frame.pack(fill=tk.X, pady=(0, 10))

        self.mode_var = tk.StringVar(value="realtime")
        ttk.Radiobutton(mode_frame, text="Realtime Clicking", variable=self.mode_var,
                       value="realtime", command=self.switch_mode).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(mode_frame, text="Sequence Playback", variable=self.mode_var,
                       value="sequence", command=self.switch_mode).pack(side=tk.LEFT)

        # Settings frame
        self.settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        self.settings_frame.pack(fill=tk.X, pady=(0, 10))

        # Click interval
        ttk.Label(self.settings_frame, text="Interval (ms):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.interval_var = tk.StringVar(value=str(DEFAULT_INTERVAL))
        ttk.Entry(self.settings_frame, textvariable=self.interval_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=2)

        # Click count
        ttk.Label(self.settings_frame, text="Click Count (0=infinite):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.count_var = tk.StringVar(value=str(DEFAULT_COUNT))
        ttk.Entry(self.settings_frame, textvariable=self.count_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=2)

        # Mouse button
        ttk.Label(self.settings_frame, text="Mouse Button:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.button_var = tk.StringVar(value=DEFAULT_BUTTON)
        button_combo = ttk.Combobox(self.settings_frame, textvariable=self.button_var,
                                   values=["left", "right", "middle"], state="readonly", width=8)
        button_combo.grid(row=2, column=1, sticky=tk.W, pady=2)

        # Hotkey
        ttk.Label(self.settings_frame, text="Hotkey:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.hotkey_var = tk.StringVar(value=DEFAULT_HOTKEY)
        ttk.Entry(self.settings_frame, textvariable=self.hotkey_var, width=10).grid(row=3, column=1, sticky=tk.W, pady=2)

        # Sequence frame (initially hidden)
        self.sequence_frame = ttk.LabelFrame(main_frame, text="Sequence", padding="10")

        ttk.Label(self.sequence_frame, text="Recorded Positions:").pack(anchor=tk.W)
        self.sequence_text = scrolledtext.ScrolledText(self.sequence_frame, height=8, width=50, state=tk.DISABLED)
        self.sequence_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        self.start_btn = ttk.Button(button_frame, text="▶ Start", command=self.start_clicking)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.stop_btn = ttk.Button(button_frame, text="⏹ Stop", command=self.stop_clicking, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.record_btn = ttk.Button(button_frame, text="⏺ Record", command=self.start_recording)
        self.record_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.clear_btn = ttk.Button(button_frame, text="🗑 Clear", command=self.clear_sequence)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Preset buttons
        preset_frame = ttk.LabelFrame(main_frame, text="Presets", padding="10")
        preset_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(preset_frame, text="Single Click", command=lambda: self.set_preset(1000, 1)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(preset_frame, text="Double Click", command=lambda: self.set_preset(100, 2)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(preset_frame, text="Rapid Fire", command=lambda: self.set_preset(50, 0)).pack(side=tk.LEFT, padx=(0, 5))

        # Info label
        info_label = ttk.Label(main_frame, text="Press ESC to emergency stop. Hotkey works globally.",
                              font=('Arial', 8), foreground='gray')
        info_label.pack(pady=(10, 0))

    def switch_mode(self):
        global current_mode
        current_mode = self.mode_var.get()
        if current_mode == "sequence":
            self.sequence_frame.pack(fill=tk.X, pady=(0, 10), after=self.settings_frame)
            self.record_btn.config(state=tk.NORMAL)
            self.clear_btn.config(state=tk.NORMAL)
        else:
            self.sequence_frame.pack_forget()
            self.record_btn.config(state=tk.DISABLED)
            self.clear_btn.config(state=tk.DISABLED)

    def set_preset(self, interval, count):
        self.interval_var.set(str(interval))
        self.count_var.set(str(count))

    def start_clicking(self):
        global is_running, click_thread
        if is_running:
            return

        try:
            interval = int(self.interval_var.get())
            count = int(self.count_var.get())
            button = self.button_var.get()
            hotkey = self.hotkey_var.get().lower()

            if interval < 10:
                messagebox.showerror("Error", "Interval must be at least 10ms")
                return
            if count < 0:
                messagebox.showerror("Error", "Click count cannot be negative")
                return

        except ValueError:
            messagebox.showerror("Error", "Invalid numeric input")
            return

        is_running = True
        self.status_var.set("Status: Running")
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.root.configure(bg='#ffe6e6')  # Light red background when running

        if current_mode == "realtime":
            click_thread = threading.Thread(target=self.click_loop, args=(interval, count, button))
        else:
            if not recorded_positions:
                messagebox.showerror("Error", "No recorded positions to play back")
                self.stop_clicking()
                return
            click_thread = threading.Thread(target=self.playback_loop, args=(interval, count, button))

        click_thread.daemon = True
        click_thread.start()

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