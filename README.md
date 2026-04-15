# 🖱️ Kliker

A modern, production-ready auto-clicker built with Python.  
Designed for speed, precision, and ease of use, this tool provides powerful mouse automation with a clean GUI and global hotkey control.

Works out-of-the-box with zero configuration.

---

## ⚡ Features

- Left, right, and middle mouse click support  
- Adjustable click interval (milliseconds precision)  
- Configurable click count (or infinite loop)  
- Global hotkeys (works in background)  
- Start / Stop / Toggle controls  
- Emergency stop (ESC key)  
- Real-time status indicator (Idle / Running)  
- Multithreaded (no UI freezing)  
- Lightweight and fast  

---

## 🔁 Modes

### 1. Realtime Clicking Mode
- Clicks at current cursor position  
- Ideal for games, repetitive tasks  

### 2. Sequence Playback Mode
- Record click positions  
- Replay them in exact order  
- Useful for automation workflows and testing  

---

## 🎯 Use Cases

- Game automation (idle games, farming)  
- UI / UX testing  
- Data entry automation  
- Repetitive workflows  

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python kliker.py
```

### Test Installation
```bash
python test.py
```

Or run the validation script:
```bash
python validate.py
```

### Expected Results
- **With Display (GUI environment)**: All tests pass ✅
- **Headless environment**: pynput shows warning ⚠️ (normal - requires X11)
- **Core functionality**: Always works ✅

That's it! The application will launch with a clean GUI ready to use.

---

## 📖 Usage Guide

### Basic Operation
1. **Select Mode**: Choose between "Realtime Clicking" or "Sequence Playback"
2. **Configure Settings**:
   - **Interval**: Time between clicks in milliseconds (minimum 10ms)
   - **Click Count**: Number of clicks (0 = infinite until stopped)
   - **Mouse Button**: Left, right, or middle click
   - **Hotkey**: Key to start/stop (default: F6, restart required to change)
3. **Start Clicking**: Click "▶ Start" or press your hotkey
4. **Stop**: Click "⏹ Stop", press hotkey again, or press ESC for emergency stop

### Realtime Mode
- Clicks repeatedly at your current mouse cursor position
- Perfect for games or repetitive clicking tasks

### Sequence Mode
1. **Record**: Click "⏺ Record" then click positions on screen
2. **Stop Recording**: Click "⏹ Stop Recording" when done
3. **Playback**: Click "▶ Start" to replay the sequence
4. **Clear**: Use "🗑 Clear" to reset recorded positions

### Presets
- **Single Click**: 1000ms interval, 1 click
- **Double Click**: 100ms interval, 2 clicks  
- **Rapid Fire**: 50ms interval, infinite clicks

### Safety Features
- **ESC Key**: Emergency stop at any time
- **Visual Indicator**: Red background when running
- **Status Display**: Shows current state clearly

---

## 🏗️ Building Standalone Executable

Kliker can be compiled into a standalone executable that runs without Python installed.

### Using PyInstaller

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Create Executable**:
   ```bash
   pyinstaller --onefile --windowed --name=Kliker kliker.py
   ```

3. **Find the Executable**:
   - Windows: `dist/Kliker.exe`
   - macOS: `dist/Kliker.app`
   - Linux: `dist/Kliker`

### Alternative: cx_Freeze

1. **Install cx_Freeze**:
   ```bash
   pip install cx-Freeze
   ```

2. **Create setup.py**:
   ```python
   from cx_Freeze import setup, Executable

   setup(
       name="Kliker",
       version="1.0",
       description="Auto Clicker Application",
       executables=[Executable("kliker.py")],
   )
   ```

3. **Build**:
   ```bash
   python setup.py build
   ```

---

## 🔧 Technical Details

### Libraries Used
- **pynput**: Low-level mouse and keyboard control
- **tkinter**: GUI framework (built-in Python)
- **threading**: Multithreaded operation for responsive UI

### Architecture
- **Main Thread**: GUI and user interaction
- **Click Thread**: Mouse automation (separate to prevent UI freezing)
- **Hotkey Thread**: Global keyboard listening
- **Record Thread**: Mouse position recording

### Permissions
The application requires system permissions for mouse/keyboard control. On some systems, you may need to:
- Run as administrator (Windows)
- Grant accessibility permissions (macOS)
- Allow input monitoring (Linux)

### Error Handling
- Invalid input validation
- Permission error messages
- Graceful shutdown on errors

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

Use this tool responsibly. Automated clicking may violate terms of service for some applications or games. The authors are not responsible for any misuse or consequences.

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/autoclicker-pro.git
cd autoclicker-pro
pip install -r requirements.txt
````

---

## ▶️ Run

```bash
python main.py
```

---

## 🧩 Controls

| Action     | Default |
| ---------- | ------- |
| Start/Stop | F6      |
| Force Stop | ESC     |

---

## ⚙️ Configuration

* **Interval** → Delay between clicks (seconds)
* **Click Count** → Number of clicks (0 = infinite)
* **Mouse Button** → Left / Right / Middle
* **Mode** → Realtime or Sequence

---

## 📁 Project Structure

```
Kliker/
│
├── main.py
├── core/
├── gui/
├── utils/
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🔐 Permissions

Some systems require elevated permissions:

* Windows → Run as Administrator
* macOS → Enable Accessibility access

Required for global input control.

---

## 🧪 Build Executable

### Install PyInstaller

```bash
pip install pyinstaller
```

### Build

```bash
pyinstaller --onefile --noconsole main.py
```

Output:

```
dist/main.exe
```

---

## 📦 Optional: Custom Build (Spec File)

```bash
pyinstaller build.spec
```

---

## 🚀 Future Improvements

* Macro scripting
* Save/load click profiles
* Dark mode
* Drag-based sequence editor

---

## 📜 License

MIT License

---

## 🤝 Contributing

Pull requests are welcome.
For major changes, open an issue first.

---

## ⭐ Credits

Inspired by Blur AutoClicker.

- https://github.com/Blur009/Blur-AutoClicker/releases/tag/v3.3.0