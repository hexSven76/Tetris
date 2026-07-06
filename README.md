# Tetris

A modern terminal-based **Tetris** clone written in **Python**, featuring **Super Rotation System (SRS)**, **Hold Piece**, **Ghost Piece**, configurable **DAS/ARR**, smooth ANSI terminal rendering, and a modular object-oriented architecture.

<img width="1280" height="720" alt="vc_0002147-1" src="https://github.com/user-attachments/assets/bd7a21f9-8dea-4169-93ca-af201031c889" />

---

## ✨ Features

* Classic Tetris gameplay
* Super Rotation System (SRS) wall kicks
* Ghost Piece
* Hold Piece
* Next Piece Preview
* Hard Drop and Soft Drop
* Progressive gravity and level system
* Animated line clearing
* ANSI-colored terminal rendering

---

## 🎮 Controls

| Key   | Action                   |
| ----- | ------------------------ |
| ←     | Move Left                |
| →     | Move Right               |
| ↓     | Soft Drop                |
| Space | Hard Drop                |
| Z     | Rotate Counter-Clockwise |
| X     | Rotate Clockwise         |
| C     | Hold Piece               |

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/hexSven76/Tetris.git
cd .\Tetris\
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the game:

```bash
python main.py
```

---

## 🛠️ Technical Highlights

This project was built with an emphasis on clean architecture and recreating the mechanics of modern Tetris.

Highlights include:

* Official Super Rotation System (SRS) implementation
* Wall kick support for all tetrominoes
* Configurable DAS (Delayed Auto Shift)
* Configurable ARR (Auto Repeat Rate)
* Dynamic level progression with increasing gravity
* Ghost piece projection
* Hold piece system
* Line clear animation
* ANSI escape sequence rendering
* Alternate screen buffer for flicker-free rendering
* Modular codebase with separated responsibilities

---

## 📂 Project Structure

```text
.
├── main.py            # Main game loop
├── game.py            # General game logics
├── board.py           # Board logic and line clearing
├── piece.py           # Tetromino definitions and rotations
├── pieces_data.py    
├── srs.py             # SRS tables
├── renderer.py        # Terminal rendering
├── input.py           # Keyboard input handling
├── constants.py       # Shared constants
└── requirements.txt
```

---

## 📜 License

This project is licensed under the MIT License.

