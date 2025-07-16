from GestureActions import action_map
import pyautogui
import cv2
import time
import os
import HandTrackingModule as htm
import pyautogui as pag
import keyboard
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import numpy as np
import ctypes
import datetime
from collections import deque
import json


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)


GESTURE_FILE = "gesture_config.json"
ENABLED_FILE = "enabled_gestures.json"


# print(gesture_config_path)
# print(enabled_gestures_path)
with open(GESTURE_FILE, "r") as f:
    gesture_config = json.load(f)
print("gesture_config loaded")

with open(ENABLED_FILE, "r") as f:
    enabled_gestures = json.load(f)

# print("enabled_gestures loaded")

# print("Starting camera loop...")
pTime = 0


detector = htm.handDetector(detectionConf=0.8)

try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volRange = volume.GetVolumeRange()
    minVol = volRange[0]
    maxVol = volRange[1]
except Exception as e:
    print("Error initializing audio device:", e)
    volume = None

lastVolumeChangeTime = 0


tipIds = [4, 8, 12, 16, 20]

prevAction = None
actionCooldown = 1  # seconds
last_trigger_time = 0

prevFingerCount = -1
stableStartTime = 0
gestureHoldDuration = 0.5  # seconds gesture must be stable


def hand_volume_control(lmList, img):
    global lastVolumeChangeTime

    x1, y1 = lmList[4][1], lmList[4][2]
    x2, y2 = lmList[8][1], lmList[8][2]
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    length = math.hypot(x2 - x1, y2 - y1)

    vol = np.interp(length, [60, 179], [minVol, maxVol])

    currentVolumeTime = time.time()
    volumeChangeThreshold = 1.5

    if currentVolumeTime - lastVolumeChangeTime > volumeChangeThreshold:
        if volume:
            volume.SetMasterVolumeLevel(vol, None)
            lastVolumeChangeTime = currentVolumeTime

    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

    if length < 15:
        cv2.circle(img, ((x1 + x2) // 2, (y1 + y2) // 2),
                   6, (0, 255, 0), cv2.FILLED)

    cv2.putText(img, f'Volume: {int(np.interp(length, [60, 179], [0, 100]))} %',
                (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)


def trigger_action(fingerCount):
    global prevAction, last_trigger_time

    currentTime = time.time()
    if currentTime - last_trigger_time < actionCooldown:
        return  # Prevent repeated triggers

    gestureKey = str(fingerCount)
    actionName = gesture_config.get(gestureKey)

    # checking if gesture is enabled
    if not enabled_gestures.get(gestureKey, True):
        print(f"Gesture {gestureKey} is disabled.")
        return

    if actionName in action_map:
        # print(f"Action triggered: {actions[fingerCount]}")
        action_map[actionName]()
        last_trigger_time = currentTime
    else:
        print(f"No action mapped for {gestureKey} fingers.")


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1] + 20:
            fingers.append(1)
        else:
            fingers.append(0)

        # The four other fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        # print(f"DEBUG: Detected fingers = {fingers}")

        totalFingers = fingers.count(1)

        # labels = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        # for i in range(5):
        #     print(f"{labels[i]}: {'Up' if fingers[i] else 'Down'}")

        # If only thumb + index are up → adjust volume by distance
        if fingers == [1, 1, 0, 0, 0]:
            hand_volume_control(lmList, img)
        else:
            # Stable gesture detection
            if totalFingers != prevFingerCount:
                stableStartTime = time.time()  # Gesture changed, reset timer
                prevFingerCount = totalFingers
            else:
                if totalFingers in [1, 2] and (fingers[0] == 1 or fingers[1] == 1):
                    if time.time() - stableStartTime < 0.4:
                        continue

                if time.time() - stableStartTime > gestureHoldDuration:
                    print(f"Confirmed gesture: {totalFingers} fingers")
                    trigger_action(totalFingers)
                    prevFingerCount = -1  # Reset so the same gesture doesn't retrigger
                    stableStartTime = 0

        cv2.putText(img, f'Fingers: {totalFingers}', (50, 400),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 40),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow("Gesture Assistant", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break
