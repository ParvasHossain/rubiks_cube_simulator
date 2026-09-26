<div align="center">

# 🧩 3D Rubik's Cube Simulator & AI Coach

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame-CE](https://img.shields.io/badge/Pygame--CE-2.5.8+-green?style=for-the-badge&logo=pygame&logoColor=white)](https://pyga.me)
[![OpenGL](https://img.shields.io/badge/PyOpenGL-3.1.10-5580A0?style=for-the-badge&logo=opengl&logoColor=white)](https://www.opengl.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

*An interactive, high-performance 3D Rubik's Cube Simulator powered by OpenGL, featuring an intelligent AI Coach, real-time animation engine, and customizable speed controller.*

[Features](#-key-features) • [Quick Start](#-quick-start) • [Controls](#-controls--keyboard-shortcuts) • [Architecture](#-architecture) • [License](#-license)

---

</div>

## 📌 Features

- **🎮 Interactive 3D Viewport:** Full 360° orbital camera control with drag-to-rotate and scroll-to-zoom capabilities rendered via PyOpenGL.
- **🎓 Real-Time AI Coach:** Provides live feedback and mechanical explanations for every face turn (e.g., Cross creation, F2L slotting, OLL/PLL triggers).
- **⏱️ Speed Controller Slider:** Adjust playback rate dynamically from $1 \text{ move/sec}$ (frame-by-frame learning) up to $20 \text{ moves/sec}$ (high-speed auto-solving).
- **🌀 Fluid 3D Animation Engine:** Queued move pipeline ensuring smooth 90° and 180° rotation sweeps without UI blocking or dropping frame rates.
- **⚡ Zero External Solver Dependencies:** Pure Python matrix tracking system—runs out of the box without requiring C++ compilers or third-party binaries.

---

## 🚀 Quick Start

### Prerequisites
Make sure you have **Python 3.10+** installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/rubiks-cube-ai-coach.git
cd rubiks-cube-ai-coach
```

### 2. Set Up Virtual Environment
```bash
# Create environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on macOS / Linux
source venv/bin/activate
```

### 3. Install Requirements
```bash
pip install pygame-ce PyOpenGL pillow
```

### 4. Launch the App
```bash
python rubiks_cube_app.py
```

---

## ⌨️ Controls & Keyboard Shortcuts

| Input | Action |
| :--- | :--- |
| **Left Click + Drag** | Orbit Camera View |
| **Mouse Wheel Up/Down** | Zoom Viewport In / Out |
| <kbd>U</kbd> / <kbd>Shift</kbd> + <kbd>U</kbd> | Turn **Up** Face (Clockwise / Counter-Clockwise) |
| <kbd>D</kbd> / <kbd>Shift</kbd> + <kbd>D</kbd> | Turn **Down** Face (Clockwise / Counter-Clockwise) |
| <kbd>F</kbd> / <kbd>Shift</kbd> + <kbd>F</kbd> | Turn **Front** Face (Clockwise / Counter-Clockwise) |
| <kbd>B</kbd> / <kbd>Shift</kbd> + <kbd>B</kbd> | Turn **Back** Face (Clockwise / Counter-Clockwise) |
| <kbd>L</kbd> / <kbd>Shift</kbd> + <kbd>L</kbd> | Turn **Left** Face (Clockwise / Counter-Clockwise) |
| <kbd>R</kbd> / <kbd>Shift</kbd> + <kbd>R</kbd> | Turn **Right** Face (Clockwise / Counter-Clockwise) |

---

## 🏗️ Architecture

```
├── rubiks_cube_app.py    # Complete application entry point (UI + OpenGL Engine + State Machine)
├── README.md             # Project documentation
└── requirements.txt      # Dependency manifest
```

- **`RubiksCubeLogic`**: Handles 3D spatial cubie coordinate mappings, state history, and inverse move resolution.
- **`draw_cubie`**: Manages OpenGL quad primitive creation, sticker offsets, and color buffer rendering.
- **`RubiksCubeApp`**: Controls the Tkinter dashboard, speed sliders, thread management, and event loops.

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for details.