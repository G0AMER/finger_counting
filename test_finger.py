import time

import cv2
import mediapipe as mp
import requests


mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
tipIds = [4, 8, 12, 16, 20]
response = requests.get(f"http://192.168.4.1/start?signal={'wait'}")
while response.text != "go":
    response = requests.get(f"http://192.168.4.1/start?signal={'wait'}")
    print(response.text)
    time.sleep(1)
print(response.text)
video = cv2.VideoCapture("http://192.168.4.1/stream")
total = 0
t = time.time()
with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while total == 0 or time.time() - t < 3:
        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList = []
        if results.multi_hand_landmarks:
            for hand_index, hand_landmark in enumerate(results.multi_hand_landmarks):
                myHands = results.multi_hand_landmarks[hand_index]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
                fingers = []
                if len(lmList) != 0:
                    if hand_index == 0:  # Right hand
                        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                        for id in range(1, 5):
                            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                                fingers.append(1)
                            else:
                                fingers.append(0)
                    elif hand_index == 1:  # Left hand
                        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                        for id in range(1, 5):
                            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                                fingers.append(1)
                            else:
                                fingers.append(0)
                    total = fingers.count(1)

                    print(total)
        # Send HTTP GET request to ESP32-CAM with number offingers detected
        # response = requests.get(f"http://192.168.4.1/fingers?num={total}")
        # print(response.text)
        cv2.imshow("Frame", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

t = time.time()
list1 = []
with mp_hand.Hands(min_detection_confidence=0.4, min_tracking_confidence=0.4) as hands:
    while time.time() - t < 2:
        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList = []
        if results.multi_hand_landmarks:
            for hand_index, hand_landmark in enumerate(results.multi_hand_landmarks):
                myHands = results.multi_hand_landmarks[hand_index]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
                fingers = []
                if len(lmList) != 0:
                    if hand_index == 0:  # Right hand
                        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                        for id in range(1, 5):
                            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                                fingers.append(1)
                            else:
                                fingers.append(0)
                    elif hand_index == 1:  # Left hand
                        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                        for id in range(1, 5):
                            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                                fingers.append(1)
                            else:
                                fingers.append(0)
                    list1.append(fingers.count(1))
                    list1.append(fingers.count(1))
                    total = fingers.count(1)
                    print(total)

        # Send HTTP GET request to ESP32-CAM with number offingers detected
        # response = requests.get(f"http://192.168.4.1/fingers?num={total}")
        # print(response.text)
        cv2.imshow("Frame", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
video.release()
cv2.destroyAllWindows()
time.sleep(0.5)
print(list1)
res1 = list1.count(1)
res2 = list1.count(2)
mx = max(res1, res2)
res = 0
if mx == res2:
    res = 2
else:
    res = 1
print("resultat:", res)
response = requests.get(f"http://192.168.4.1/fingers?num={res}")
print(response.text)
video = cv2.VideoCapture("http://192.168.4.1/stream")
with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow("Frame", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
video.release()
cv2.destroyAllWindows()
