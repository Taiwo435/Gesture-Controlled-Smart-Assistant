import pyautogui
import keyboard
import datetime
import time
import ctypes
import webbrowser

VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xB3


def press_key(hexKeyCode):
    try:
        ctypes.windll.user32.keybd_event(hexKeyCode, 0, 0, 0)
        time.sleep(0.01)
        ctypes.windll.user32.keybd_event(hexKeyCode, 0, 2, 0)
    except Exception as e:
        print(f"Error pressing key {hexKeyCode}:", e)


def mute_volume():
    try:
        keyboard.press_and_release("volume mute")
    except Exception as e:
        print(f"Error sending keyboard command to mute:", e)


def take_screenshot():
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        pyautogui.screenshot(filename)
        print(f"Screenshot saved as {filename}")
    except Exception as e:
        print("Error taking screenshot:", e)


def next_track():
    press_key(VK_MEDIA_NEXT_TRACK)


def previous_track():
    press_key(VK_MEDIA_PREV_TRACK)


def open_chrome():
    try:
        url = "https://www.google.com"
        chrome_path = '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" %s'
        webbrowser.register(
            'chrome', None, webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open_new_tab(url)
        print("Chrome successfully opened.")
    except Exception as e:
        print(f"Failed to open Chrome: {e}")


def play_pause_media():
    press_key(VK_MEDIA_PLAY_PAUSE)


# Optional: if you want a built-in function map
action_map = {
    "mute_volume": mute_volume,
    "take_screenshot": take_screenshot,
    "next_track": next_track,
    "previous_track": previous_track,
    "open_chrome": open_chrome,
    "play_pause_media": play_pause_media
}
