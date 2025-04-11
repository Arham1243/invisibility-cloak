import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

time.sleep(2)
background = 0


for i in range(30):
    ret, background = cap.read()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    
    frame = cv2.flip(frame, 1)

    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    red_mask = mask1 + mask2

    
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations=2)
    red_mask = cv2.dilate(red_mask, np.ones((3,3), np.uint8), iterations=1)

    
    mask_inv = cv2.bitwise_not(red_mask)

    
    res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)

    
    res2 = cv2.bitwise_and(background, background, mask=red_mask)

    
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow("Invisibility Cloak", final_output)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
