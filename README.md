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

## 🛠️ Requirements

- Python 3.8+

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

