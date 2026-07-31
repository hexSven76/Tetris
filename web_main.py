"""
Web frontend entry point. Run with:

    python web_main.py

Then open http://127.0.0.1:5000 in a browser.

Input and state share a single WebSocket connection (via flask-sock)
instead of separate POST requests + an SSE stream. This removes the
per-keystroke HTTP request/response overhead.
"""

from flask import Flask, request, send_from_directory, jsonify
from flask_sock import Sock
import threading
import time
import json
import os

from constants import LOCK_DELAY
from game import Game
from web_input import WebInputHandler
from web_themes import serialize_themes
from highscore import load_high_score
from audio import Audio

# Sound is played client-side in the browser instead of server-side
Audio.enabled = False

app = Flask(__name__, static_folder="static", static_url_path="")
sock = Sock(app)

ASSETS_SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "sounds")

state_lock = threading.Lock()
state_condition = threading.Condition()

# "menu" phase : no active game, main menu is visible, nothing ticks
# "playing" phase :  active game running
phase = "menu"
tetris = None
web_input = None
latest_state = None
game_over_saved = False
TICK_INTERVAL = 0.005  # 200Hz tick rate for responsive DAS/ARR


def make_game(start_level):
    '''
    on_frame streams intermediate frames during the line-clear animation
    (the same hook main.py uses for Renderer.draw).
    '''
    return Game(on_frame=lambda g: push_state(), start_level=start_level)


def serialize_state():

    if phase == "menu":
        return {"phase": "menu", "high_score": load_high_score()}

    game = tetris

    def preview(piece):
        if piece is None:
            return None
        return {"shape": piece.get_shape(), "color": piece.color}

    return {
        "phase": "playing",
        "grid": game.board.grid,
        "current": {
            "cells": game.current_piece.get_occupied_cells(),
            "color": game.current_piece.color,
        },
        "ghost": {"cells": game.get_ghost().get_occupied_cells()},
        "next": preview(game.next_piece),
        "hold": preview(game.hold_piece),
        "score": game.score,
        "high_score": game.high_score,
        "level": game.level,
        "lines": game.total_lines,
        "time": game.get_elapsed_time(),
        "paused": game.paused,
        "game_over": game.game_over,
    }


def push_state():
    '''
    Called every tick, and mid-frame during line-clear animation.
    Notifies any waiting WebSocket sender threads immediately instead of
    making them wait out a polling interval - this is what makes state
    (and therefore visual feedback) reach the browser with minimal delay.
    '''

    global latest_state
    with state_condition:
        latest_state = json.dumps(serialize_state())
        state_condition.notify_all()


def handle_ws_message(data):
    """Applies one incoming WebSocket message. Called with state_lock held."""

    global phase, tetris, web_input, game_over_saved

    msg_type = data.get("type")

    if msg_type == "start":
        level = data.get("level", 1)
        try:
            level = int(level)
        except (TypeError, ValueError):
            level = 1
        level = max(1, min(9, level))

        tetris = make_game(start_level=level)
        web_input = WebInputHandler()
        game_over_saved = False
        phase = "playing"
        push_state()

    elif msg_type == "menu":
        phase = "menu"
        push_state()

    else:
        action = data.get("action")
        if action and phase == "playing":
            web_input.apply_event(action)


def tick_loop():

    global game_over_saved
    last_fall_time = time.time()
    push_state()

    while True:

        with state_lock:

            if phase == "playing":

                if not tetris.game_over:

                    web_input.update(tetris)

                    if not tetris.paused:

                        current_time = time.time()
                        if current_time - last_fall_time >= tetris.get_fall_interval():
                            tetris.gravity()
                            last_fall_time = current_time

                        if tetris.lock_timer and current_time - tetris.lock_timer >= LOCK_DELAY:
                            tetris.lock_and_spawn()

                    else:
                        last_fall_time = time.time()

                elif not game_over_saved:
                    tetris.save_score()
                    game_over_saved = True

                push_state()

            else:
                last_fall_time = time.time()

        time.sleep(TICK_INTERVAL)


threading.Thread(target=tick_loop, daemon=True).start()


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/themes")
def api_themes():
    return jsonify(serialize_themes())


@app.route("/api/sounds")
def api_sounds():
    # Lists SFXs in assets/sounds (can play - .wav, .mp3, .ogg, ...)
    # Keyed by filename without extension
    sounds = {}
    if os.path.isdir(ASSETS_SOUNDS_DIR):
        for name in sorted(os.listdir(ASSETS_SOUNDS_DIR)):
            if name.startswith("."):
                continue
            full_path = os.path.join(ASSETS_SOUNDS_DIR, name)
            if os.path.isfile(full_path) and "." in name:
                key = name.rsplit(".", 1)[0]
                sounds[key] = f"/assets/sounds/{name}"
    return jsonify(sounds)


@app.route("/assets/sounds/<path:filename>")
def assets_sound(filename):
    return send_from_directory(ASSETS_SOUNDS_DIR, filename)


@sock.route("/ws")
def ws_endpoint(ws):

    stop_event = threading.Event()

    def sender():
        last_sent = None
        while not stop_event.is_set():
            with state_condition:
                while latest_state == last_sent and not stop_event.is_set():
                    state_condition.wait(timeout=1.0)
                current = latest_state
            if stop_event.is_set():
                break
            try:
                ws.send(current)
                last_sent = current
            except Exception:
                stop_event.set()
                break

    sender_thread = threading.Thread(target=sender, daemon=True)
    sender_thread.start()

    try:
        while True:
            msg = ws.receive()  # blocks until a message arrives or the socket closes
            if msg is None:
                break
            try:
                data = json.loads(msg)
            except (TypeError, ValueError):
                continue
            with state_lock:
                handle_ws_message(data)
    finally:
        stop_event.set()
        with state_condition:
            state_condition.notify_all()  # wake the sender thread so it can exit
        sender_thread.join(timeout=2)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=True, debug=False)
