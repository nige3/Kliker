# 🖱️ Kliker - Auto Clicker

A fast, precise auto-clicker with global hotkey support and modern GUI. No configuration needed.

## ⚡ Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python kliker.py

# Test
python test.py
```

## 🎯 Features

- **Realtime Mode**: Click at current position (games, automation)
- **Sequence Mode**: Record and replay click positions
- **Global Hotkey**: Control from any window (F6 = default start/stop)
- **Multiple Buttons**: Left, right, middle click support
- **Advanced Settings**: Patterns, randomization, custom intervals
- **Thread-Safe**: No UI freezing during clicking
- **Emergency Stop**: Press ESC anytime

## 📖 Usage

### Realtime Clicking
1. Set interval (ms) and click count (0 = infinite)
2. Position your mouse
3. Press F6 to start / stop

### Sequence Playback
1. Click "Record"
2. Click positions on screen
3. Click "Stop Recording"
4. Press F6 to playback

## ⚙️ Configuration

Settings auto-save to `kliker_config.json`. Edit manually for custom configs.

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

## 🏗️ Build Standalone Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed kliker.py
```

Output: `dist/kliker.exe` (Windows) or `dist/kliker` (Linux/macOS)

## 🛠️ Technical Stack

- **GUI**: tkinter (built-in)
- **Automation**: pynput
- **Threading**: Multithreaded (responsive UI)
- **Type Hints**: 100% covered, IDE-friendly
- **Documentation**: In-code + QUICKSTART.md + ARCHITECTURE.md

## 📚 Documentation

- **QUICKSTART.md** - Full user guide with examples
- **ARCHITECTURE.md** - Technical design and extension points
- **LICENSE** - MIT license

## 🔒 Safety

- Thread-safe state management
- Input validation on all settings
- Emergency stop (ESC) always works
- Clean resource shutdown

## 📄 License

MIT - See LICENSE file


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