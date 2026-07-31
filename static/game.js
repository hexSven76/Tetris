// Must match constants.py (COLS, ROWS) and PREVIEW_BOX_SIZE.
const COLS = 10;
const ROWS = 20;
const CELL = 30;
const PREVIEW_SIZE = 5;
const PREVIEW_CELL = 24;

const EMPTY_COLOR = "#17171f";

let THEMES = {}; // Populated from /api/themes on load
let SOUNDS = {}; // Populated from /api/sounds on load
let currentTheme = localStorage.getItem("tetris_theme") || "classic";
let currentLevel = parseInt(localStorage.getItem("tetris_level"), 10);
if (!Number.isInteger(currentLevel) || currentLevel < 1 || currentLevel > 9) currentLevel = 1;

const menuScreen = document.getElementById("menu-screen");
const gameScreen = document.getElementById("game-screen");
const menuHighScoreEl = document.getElementById("menu-high-score");
const levelPicker = document.getElementById("level-picker");
const themePicker = document.getElementById("theme-picker");
const startButton = document.getElementById("start-button");

const boardCanvas = document.getElementById("board");
const boardCtx = boardCanvas.getContext("2d");
const nextCanvas = document.getElementById("next");
const nextCtx = nextCanvas.getContext("2d");
const holdCanvas = document.getElementById("hold");
const holdCtx = holdCanvas.getContext("2d");

const scoreEl = document.getElementById("score");
const highScoreEl = document.getElementById("high-score");
const levelEl = document.getElementById("level");
const linesEl = document.getElementById("lines");
const timeEl = document.getElementById("time");

const overlay = document.getElementById("overlay");
const overlayText = document.getElementById("overlay-text");
const resumeButton = document.getElementById("resume-button");
const menuButton = document.getElementById("menu-button");
const continueButton = document.getElementById("continue-button");

let lastLines = 0;
let isGameOver = false;
let isPaused = false;
let phase = "menu";

// ---------- Theme loading ----------

function hexToRgba(hex, alpha) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r},${g},${b},${alpha})`;
}

async function loadThemes() {
  const res = await fetch("/api/themes");
  THEMES = await res.json();
  if (!THEMES[currentTheme]) {
    currentTheme = Object.keys(THEMES)[0] || "classic";
  }
  buildThemePicker();
}

async function loadSounds() {
  try {
    const res = await fetch("/api/sounds");
    if (!res.ok) {
      console.error("GET /api/sounds failed:", res.status, await res.text());
      return;
    }
    const map = await res.json();
    console.log("Loaded sound map from /api/sounds:", map);
    if (Object.keys(map).length === 0) {
      console.warn("assets/sounds appears empty (or the folder wasn't found) - all sounds will fall back to the beep.");
    }
    for (const [name, url] of Object.entries(map)) {
      SOUNDS[name] = new Audio(url);
      SOUNDS[name].addEventListener("error", () => {
        console.error(`Failed to load sound file: ${url}`);
      });
    }
  } catch (e) {
    console.error("loadSounds() failed:", e);
  }
}

// ---------- Menu setup ----------

function buildLevelPicker() {
  levelPicker.innerHTML = "";
  for (let lvl = 1; lvl <= 9; lvl++) {
    const btn = document.createElement("button");
    btn.textContent = lvl;
    btn.className = lvl === currentLevel ? "selected" : "";
    btn.addEventListener("click", () => {
      currentLevel = lvl;
      localStorage.setItem("tetris_level", String(lvl));
      buildLevelPicker();
    });
    levelPicker.appendChild(btn);
  }
}

function buildThemePicker() {
  themePicker.innerHTML = "";
  for (const name of Object.keys(THEMES)) {
    const swatch = document.createElement("div");
    swatch.className = "theme-swatch" + (name === currentTheme ? " selected" : "");

    const row = document.createElement("div");
    row.className = "swatch-row";
    ["1", "3", "5", "7"].forEach((id) => {
      const dot = document.createElement("span");
      dot.style.background = THEMES[name][id] || "#888";
      row.appendChild(dot);
    });

    const label = document.createElement("div");
    label.className = "swatch-name";
    label.textContent = name;

    swatch.appendChild(row);
    swatch.appendChild(label);
    swatch.addEventListener("click", () => {
      currentTheme = name;
      localStorage.setItem("tetris_theme", name);
      buildThemePicker();
    });
    themePicker.appendChild(swatch);
  }
}

buildLevelPicker();
loadThemes();
loadSounds();

startButton.addEventListener("click", () => {
  sendMessage({ type: "start", level: currentLevel });
});

// ---------- Rendering ----------

function drawCell(ctx, x, y, size, color) {
  ctx.fillStyle = color;
  ctx.fillRect(x, y, size, size);
}

function drawBoard(state) {
  const palette = THEMES[currentTheme];
  boardCtx.clearRect(0, 0, boardCanvas.width, boardCanvas.height);

  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const val = state.grid[r][c];
      const color = val === 0 ? EMPTY_COLOR : palette[val];
      drawCell(boardCtx, c * CELL, r * CELL, CELL, color);
    }
  }

  const ghostColor = hexToRgba(palette.ghost, 0.35);
  for (const [r, c] of state.ghost.cells) {
    if (r >= 0 && r < ROWS && c >= 0 && c < COLS) {
      drawCell(boardCtx, c * CELL, r * CELL, CELL, ghostColor);
    }
  }

  const activeColor = palette[state.current.color];
  for (const [r, c] of state.current.cells) {
    if (r >= 0 && r < ROWS && c >= 0 && c < COLS) {
      drawCell(boardCtx, c * CELL, r * CELL, CELL, activeColor);
    }
  }
}

function drawPreview(ctx, canvas, piece) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  if (!piece) return;

  const palette = THEMES[currentTheme];
  const shape = piece.shape;
  const shapeH = shape.length;
  const shapeW = shape[0].length;
  const topPad = Math.floor((PREVIEW_SIZE - shapeH) / 2);
  const leftPad = Math.floor((PREVIEW_SIZE - shapeW) / 2);
  const color = palette[piece.color];

  for (let r = 0; r < shapeH; r++) {
    for (let c = 0; c < shapeW; c++) {
      if (shape[r][c] === 1) {
        const x = (c + leftPad) * PREVIEW_CELL;
        const y = (r + topPad) * PREVIEW_CELL;
        drawCell(ctx, x, y, PREVIEW_CELL, color);
      }
    }
  }
}

function formatTime(totalSeconds) {
  const m = Math.floor(totalSeconds / 60);
  const s = totalSeconds % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

function playBeepFallback(reason) {
  console.warn(`playBeepFallback() firing - ${reason}`);
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.frequency.value = 660;
    gain.gain.setValueAtTime(0.15, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.2);
    osc.connect(gain).connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.2);
  } catch (e) {
    // ignore - audio not essential
  }
  return null;
}

// Plays a sound by name so callers that need to stop a sound later
// (like gameover) can hold onto the right instance
function playSound(name) {
  const audio = SOUNDS[name];
  if (!audio) {
    return playBeepFallback(`no sound loaded for "${name}" (check /api/sounds output and your filenames)`);
  }
  // cloneNode lets overlapping plays (like rapid line clears)
  const instance = audio.cloneNode();
  instance.play().catch((err) => console.warn(`Playback blocked for "${name}":`, err));
  return instance;
}

let gameOverAudio = null;

function stopGameOverSound() {
  if (gameOverAudio) {
    gameOverAudio.pause();
    gameOverAudio.currentTime = 0;
    gameOverAudio = null;
  }
}

function render(state) {
  phase = state.phase;

  if (phase === "menu") {
    menuScreen.classList.remove("hidden");
    gameScreen.classList.add("hidden");
    menuHighScoreEl.textContent = state.high_score;
    lastLines = 0;
    isGameOver = false;
    isPaused = false;
    return;
  }

  menuScreen.classList.add("hidden");
  gameScreen.classList.remove("hidden");

  if (Object.keys(THEMES).length === 0) return; // themes still loading

  drawBoard(state);
  drawPreview(nextCtx, nextCanvas, state.next);
  drawPreview(holdCtx, holdCanvas, state.hold);

  scoreEl.textContent = state.score;
  highScoreEl.textContent = state.high_score;
  levelEl.textContent = state.level;
  linesEl.textContent = state.lines;
  timeEl.textContent = formatTime(state.time);

  if (state.lines > lastLines) {
    const clearedThisEvent = state.lines - lastLines;
    playSound(clearedThisEvent >= 4 ? "4_lines" : "1_line");
  }
  lastLines = state.lines;

  const wasPaused = isPaused;
  const wasGameOver = isGameOver;
  isGameOver = state.game_over;
  isPaused = state.paused;

  if (isGameOver && !wasGameOver) {
    gameOverAudio = playSound("gameover");
  } else if (!isGameOver && wasGameOver) {
    stopGameOverSound();
  }

  if (isGameOver) {
    overlayText.textContent = "GAME OVER";
    resumeButton.classList.add("hidden");
    menuButton.classList.add("hidden");
    continueButton.classList.remove("hidden");
    overlay.classList.remove("hidden");
  } else if (isPaused) {
    overlayText.textContent = "PAUSED";
    resumeButton.classList.remove("hidden");
    menuButton.classList.remove("hidden");
    continueButton.classList.add("hidden");
    overlay.classList.remove("hidden");
    if (!wasPaused) {
      // Resume is default keyboard focus
      resumeButton.focus();
    }
  } else {
    overlay.classList.add("hidden");
  }
}

function backToMenu() {
  stopGameOverSound();
  sendMessage({ type: "menu" });
}

resumeButton.addEventListener("click", () => sendAction("pause"));
menuButton.addEventListener("click", () => backToMenu());
continueButton.addEventListener("click", () => backToMenu());

// ---------- WebSocket transport ----------
// A single persistent connection carries input events (browser -> server)
// state pushes (server -> browser)
// plus a separate SSE stream. Auto-reconnects if the connection drops.

let ws = null;

function connectWS() {
  const protocol = location.protocol === "https:" ? "wss:" : "ws:";
  ws = new WebSocket(`${protocol}//${location.host}/ws`);

  ws.onmessage = (e) => {
    const state = JSON.parse(e.data);
    render(state);
  };

  ws.onclose = () => {
    setTimeout(connectWS, 500);
  };
}

function sendMessage(obj) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(obj));
  }
}

function sendAction(action) {
  sendMessage({ action });
}

connectWS();

// ---------- Keyboard input ----------

const KEY_MAP = {
  ArrowLeft: { down: "left_down", up: "left_up" },
  ArrowRight: { down: "right_down", up: "right_up" },
  ArrowDown: { down: "down_down", up: "down_up" },
  Space: { down: "hard_drop" },
  KeyZ: { down: "rotate_ccw" },
  KeyX: { down: "rotate_cw" },
  KeyC: { down: "hold" },
  KeyP: { down: "pause" },
};

window.addEventListener("keydown", (e) => {
  if (phase !== "playing") return; // menu is mouse-driven

  if (isGameOver) {
    if (e.code === "Enter" || e.code === "Space") {
      e.preventDefault();
      backToMenu();
    }
    return;
  }

  if (isPaused) {
    // Let Enter/Space activate whichever overlay button is focused
    if (e.code === "KeyP") {
      e.preventDefault();
      sendAction("pause");
    }
    return;
  }

  const mapping = KEY_MAP[e.code];
  if (!mapping) return;
  e.preventDefault();
  if (e.repeat) return; // server owns DAS/ARR; ignore browser auto-repeat
  sendAction(mapping.down);
});

window.addEventListener("keyup", (e) => {
  if (phase !== "playing") return;
  const mapping = KEY_MAP[e.code];
  if (!mapping || !mapping.up) return;
  e.preventDefault();
  sendAction(mapping.up);
});

// Release held movement keys if the tab loses focus
window.addEventListener("blur", () => {
  if (phase !== "playing") return;
  sendAction("left_up");
  sendAction("right_up");
  sendAction("down_up");
});
