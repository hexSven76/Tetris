# Tetris

A modern **Tetris** clone written in **Python**, featuring both a **browser-based graphical interface** and **terminal version**.

The game implements modern Tetris mechanics including the **Super Rotation System (SRS)**, **Ghost Piece**, **Hold Piece**, configurable **DAS/ARR**, sound effects, and a modular object-oriented architecture.

### Terminal Version Showcase:

<p align="center">
  <img width="1186" height="1032" alt="Terminal Version" src="https://github.com/user-attachments/assets/15215420-4c6d-4683-af84-3acb2a9b1bc9" />
</p>

---

## ✨ Features

- Browser-based graphical interface
- Terminal version
- Classic Tetris gameplay
- Super Rotation System (SRS) wall kicks
- Ghost Piece
- Hold Piece
- Next Piece Preview
- Hard Drop & Soft Drop
- 7-Bag randomizer
- Progressive gravity & level system
- Multiple color themes
- Sound effects

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| ← | Move Left |
| → | Move Right |
| ↓ | Soft Drop |
| Space | Hard Drop |
| Z | Rotate Counter-Clockwise |
| X | Rotate Clockwise |
| C | Hold Piece |
| P | Pause |

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/hexSven76/Tetris.git
cd .\Tetris\
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶ Browser Version

Start the server:

```bash
python web_main.py
```

Open your browser:

```
http://localhost:5000
```

---

## ▶ Terminal Version

```bash
python main.py
```

---

## 🛠 Technical Highlights

This project was built with an emphasis on clean architecture and recreating the mechanics of modern Tetris.

Highlights include:

- Official Super Rotation System (SRS) implementation
- Wall kick support for all tetrominoes
- Configurable DAS (Delayed Auto Shift)
- Configurable ARR (Auto Repeat Rate)
- Dynamic level progression with increasing gravity
- Ghost piece projection
- Hold piece system
- High Score persistence
- Line clear animation
- Modular game engine
- Browser frontend using HTML, CSS and JavaScript
- Python backend communicating through WebSockets

---

## 🏗 Architecture

```
Browser (HTML/CSS/JavaScript)
            │
       WebSocket
            │
     Flask-SocketIO
            │
      Python Game Engine
            │
 ┌──────────┴──────────┐
 │                     │
Browser Frontend   Terminal Frontend
```

The game logic is shared between both frontends.

---

## 📂 Project Structure

```text
.
├── game.py              # Core game engine
├── board.py             # Board logic
├── piece.py             # Tetromino logic
├── renderer.py          # Terminal renderer
├── input.py             # Terminal input
├── audio.py             # Terminal audio processing
├── themes.py            # List of color themes
├── highscore.py         # Store/Load highscore
├── constants.py         # Constant values
├── main.py              # Terminal version's gameloop
├── pieces_data.py       # List of Tetrominos and attributes
├── srs.py               # SRS tables
├── web_input.py         # GUI version input
├── web_main.py          # GUI version's gameloop
├── web_themes.py        # themes' data translation for GUI
│
├── static/              # GUI rendering files
│   ├── index.html
│   ├── game.js
│   └── style.css
│
└── assets/              # Sound effects
    └── sounds/
```

---

## 📜 License

This project is licensed under the MIT License.
