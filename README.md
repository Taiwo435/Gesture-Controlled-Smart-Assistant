# Gesture-Controlled Smart Assistant

Control your system with simple hand gestures using your webcam!  
This Python project lets you adjust volume, skip tracks, open Chrome, and more — all hands-free.

---

## Demo

![Demo GIF](https://user-images.githubusercontent.com/your-demo-link-here.gif)  
* To do: Add a short screen recording or animated GIF showing you using gestures with action feedback on screen.*

---

## Features

- Real-time hand gesture recognition using MediaPipe
- Volume control via finger distance
- Media control (Play/Pause, Next, Previous)
- Launch Google Chrome
- Instant screenshot capture
- Easily customizable actions via `gesture_config.json`
- GUI toggle panel to enable or disable gestures (`GestureToggleGUI.py`)

---

## Project Structure

```
GestureAssistant/
│
├── main.py                  # Main script (Gesture Control System)
├── GestureActions.py       # Modular system actions (volume, browser, media, etc.)
├── gesture_config.json     # Maps finger counts to actions
├── HandTrackingModule.py   # Custom hand detection wrapper using MediaPipe
├── GestureToggleGUI.py     # GUI to toggle gestures on/off
├── enabled_gestures.json   # Stores which gestures are enabled
└── README.md               # You are here
```

---

## Gesture-to-Action Mapping

Modify `gesture_config.json` to map number of raised fingers (0–5) to any supported action:

```json
{
  "0": "mute_volume",
  "1": "take_screenshot",
  "2": "next_track",
  "3": "previous_track",
  "4": "open_chrome",
  "5": "play_pause_media"
}
```

You can easily add more actions by editing `GestureActions.py` and referencing them by name here.

---

## GUI: Enable or Disable Gestures Easily

Want more control over which gestures are active?  
Use the built-in graphical interface to turn gestures on or off in seconds.

---

### How It Works

### Run the GUI:

```bash
python GestureToggleGUI.py
```

- A window opens showing checkboxes for each gesture (0–5 fingers).

- Checked box = Gesture is enabled

- Unchecked box = Gesture is disabled

- Click "Save & Close" to save changes to enabled_gestures.json.

---

## Setup & Installation

### Requirements

- Python 3.7+
- Webcam
- Windows OS (due to system-level volume/media control)

### Install Dependencies

```bash
pip install opencv-python mediapipe pyautogui pycaw screen_brightness_control keyboard comtypes
```

### Run the App

```bash
python main.py
```

Make sure your webcam is connected. A window will open displaying your hand with gesture feedback.

---

## How It Works

- Uses **MediaPipe** to detect hand landmarks in real time.
- Counts raised fingers using landmark positions.
- If the thumb + index are up (`[1,1,0,0,0]`), it activates **volume control** based on finger distance.
- For other finger counts (e.g., 1, 2, 3...), it triggers corresponding actions **only after a short confirmation hold** (debounce).
- Actions are handled modularly through `GestureActions.py`.

---

## Examples

| Gesture            | Action              |
|--------------------|---------------------|
| 0 fingers - a fist  | Mute system volume  |
| 1 finger           | Take a screenshot   |
| 2 fingers          | Next media track    |
| 3 fingers          | Previous track      |
| 4 fingers          | Open Google Chrome  |
| 5 fingers          | Play/Pause media    |
| Thumb + Index only | Adjust volume based on distance |

---

## Error Handling & Stability

- Gesture must be **held steadily** for 0.5s before triggering (prevents false triggers).
- Includes `try/except` around system actions to handle unsupported platforms or missing applications.
- Prevents rapid re-triggering with a 1-second cooldown.

---

## Ideas for Extension

- Gesture training/learning interface
- Profile switching for different users
- Integration with smart home APIs (lights, fans, etc.)

---

## Author

**Muzzamil Jolaade**  
Aspiring software engineer passionate about computer vision, automation, and system-level development.  
[LinkedIn](https://www.linkedin.com/in/muzzamil-jolaade/)• [Email](mailto:mtjolaade@gmail.com)

---

## License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute it with proper credit.
