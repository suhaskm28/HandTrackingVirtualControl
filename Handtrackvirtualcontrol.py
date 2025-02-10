import cv2
import time
import os
import pyautogui
import HandTrackingModule as htm
import numpy as np

# Initialize camera settings
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Load overlay images for finger counting
folderPath = "D:/CGI_PROJECT/AIVirtualMouse/Fingers"
overlayList = [cv2.imread(os.path.join(folderPath, imPath))
               for imPath in os.listdir(folderPath)]

detector = htm.handDetector(detectionCon=0.7, maxHands=1)
tipIds = [4, 8, 12, 16, 20]

pTime = 0
currentMode = "Finger Counting"
lastPlayPauseTime = 0
cooldown = 2
volumeLevel = 50  # Start at a mid-level
showPlayPause = False
playPauseCooldown = 2

# Mouse control variables
lastClickTime = 0
clickCooldown = 1  # Cooldown period to prevent accidental clicks
clickThreshold = 20
smoothening = 7  # The higher the value, the smoother the cursor
plocX, plocY = 0, 0
screenWidth, screenHeight = pyautogui.size()

while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.findHands(img, draw=True)
    lmlist, _ = detector.findPosition(img, draw=False)

    # Check key presses for mode switching
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('1'):
        currentMode = "Finger Counting"
    elif key == ord('2'):
        currentMode = "Volume Control"
    elif key == ord('3'):
        currentMode = "Mouse Control"

    if len(lmlist) != 0:
        fingers = []
        wrist_x = lmlist[0][1]
        thumb_tip_x = lmlist[tipIds[0]][1]

        # Determine if hand is left or right
        is_left_hand = wrist_x < thumb_tip_x

        # Thumb logic: Count as 1 if thumb is extended
        fingers.append(
            1 if abs(lmlist[tipIds[0]][1] - lmlist[13][1]) > 50 else 0)

        # Other fingers logic
        for id in range(1, 5):
            fingers.append(1 if lmlist[tipIds[id]][2]
                           < lmlist[tipIds[id] - 2][2] else 0)

        totalFingers = fingers.count(1)
        img[0:overlayList[totalFingers].shape[0],
            0:overlayList[totalFingers].shape[1]] = overlayList[totalFingers]

        if currentMode == "Volume Control":
            currentTime = time.time()
            if totalFingers == 1:
                pyautogui.press("volumeup")
                volumeLevel = min(volumeLevel + 5, 100)
            elif totalFingers == 2:
                pyautogui.press("volumedown")
                volumeLevel = max(volumeLevel - 5, 0)
            elif totalFingers == 5 and currentTime - lastPlayPauseTime > cooldown:
                pyautogui.press("playpause")
                showPlayPause = not showPlayPause
                lastPlayPauseTime = currentTime

            # Display volume level as a filled cylinder
            cylinderHeight = 200
            cylinderWidth = 50
            cylinderX = 10
            cylinderY = 200
            volumeHeight = int((volumeLevel / 100) * cylinderHeight)
            cv2.rectangle(img, (cylinderX, cylinderY), (cylinderX +
                          cylinderWidth, cylinderY + cylinderHeight), (255, 0, 0), 2)
            cv2.rectangle(img, (cylinderX, cylinderY + (cylinderHeight - volumeHeight)),
                          (cylinderX + cylinderWidth, cylinderY + cylinderHeight), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, f'Volume: {volumeLevel}%', (
                cylinderX, cylinderY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # Display play/pause button
            if showPlayPause:
                if currentTime - lastPlayPauseTime < playPauseCooldown:
                    playX, playY = 300, 150
                    if showPlayPause:
                        points = np.array(
                            [[playX, playY], [playX, playY + 50], [playX + 50, playY + 25]], np.int32)
                        cv2.fillPoly(img, [points], (0, 255, 0))
                    else:
                        cv2.rectangle(
                            img, (playX, playY), (playX + 20, playY + 50), (0, 255, 0), cv2.FILLED)
                        cv2.rectangle(
                            img, (playX + 30, playY), (playX + 50, playY + 50), (0, 255, 0), cv2.FILLED)

        elif currentMode == "Mouse Control":
            x1, y1 = lmlist[8][1], lmlist[8][2]  # Index finger tip
            x2, y2 = lmlist[4][1], lmlist[4][2]  # Thumb tip

            # Convert coordinates
            x3 = np.interp(x1, (0, wCam), (0, screenWidth))
            y3 = np.interp(y1, (0, hCam), (0, screenHeight))

            # Smooth the cursor movement
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # Move mouse
            pyautogui.moveTo(screenWidth - clocX, clocY)
            plocX, plocY = clocX, clocY

            # Left-click detection
            if abs(lmlist[8][1] - lmlist[4][1]) < clickThreshold and abs(lmlist[8][2] - lmlist[4][2]) < clickThreshold:
                currentTime = time.time()
                if currentTime - lastClickTime > clickCooldown:
                    pyautogui.click()
                    lastClickTime = currentTime

            # Right-click detection
            if abs(lmlist[12][1] - lmlist[4][1]) < clickThreshold and abs(lmlist[12][2] - lmlist[4][2]) < clickThreshold:
                currentTime = time.time()
                if currentTime - lastClickTime > clickCooldown:
                    pyautogui.rightClick()
                    lastClickTime = currentTime

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # FPS
    cv2.putText(img, f'FPS: {int(fps)}', (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
