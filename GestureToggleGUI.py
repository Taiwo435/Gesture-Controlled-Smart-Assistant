import tkinter as tk
import json
import os

GESTURE_FILE = "gesture_config.json"
ENABLED_FILE = "enabled_gestures.json"


def load_config():
    if not os.path.exists(GESTURE_FILE):
        default_config = {
            "0": "mute_volume",
            "1": "take_screenshot",
            "2": "next_track",
            "3": "previous_track",
            "4": "open_chrome",
            "5": "play_pause_media"
        }
        with open(GESTURE_FILE, "w") as f:
            json.dump(default_config, f, indent=2)
    with open(GESTURE_FILE, "r") as f:
        return json.load(f)


def load_enabled():
    if os.path.exists(ENABLED_FILE):
        with open(ENABLED_FILE, "r") as f:
            return json.load(f)
    else:
        return None  # Triggers all-enabled on first run


def save_enabled(enabled_map):
    with open(ENABLED_FILE, "w") as f:
        json.dump(enabled_map, f, indent=2)


def create_gui():
    config = load_config()
    enabled_map = load_enabled()
    if enabled_map is None:
        enabled_map = {str(k): True for k in config}

    root = tk.Tk()
    root.title("Gesture Toggle Panel")
    root.geometry("400x400")
    tk.Label(root, text="Enable or disable gestures:",
             font=("Arial", 14)).pack(pady=10)

    check_vars = {}

    for gesture_num, action in config.items():
        gesture_key = str(gesture_num)
        var = tk.BooleanVar(value=enabled_map.get(gesture_key, True))
        check_vars[gesture_key] = var

        cb = tk.Checkbutton(
            root,
            text=f"{gesture_key} fingers → {action.replace('_', ' ').title()}",
            variable=var,
            font=("Arial", 12),
            anchor="w"
        )
        cb.pack(anchor="w", padx=20)

    def save_and_exit():
        updated = {key: var.get() for key, var in check_vars.items()}
        save_enabled(updated)
        print("Saved gesture states:", updated)
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", save_and_exit)

    tk.Button(root, text="Save & Close", command=save_and_exit,
              font=("Arial", 12)).pack(pady=20)
    root.mainloop()


if __name__ == "__main__":
    create_gui()
