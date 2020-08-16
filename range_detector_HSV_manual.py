import cv2
import numpy as np
import imutils

def nothing(x):
    pass

cv2.namedWindow("HSV Range Dectector")
cv2.createTrackbar("H_min", "HSV Range Dectector", 0, 255, nothing)
cv2.createTrackbar("H_max", "HSV Range Dectector", 255, 255, nothing)
cv2.createTrackbar("S_min", "HSV Range Dectector", 0, 255, nothing)
cv2.createTrackbar("S_max", "HSV Range Dectector", 255, 255, nothing)
cv2.createTrackbar("V_min", "HSV Range Dectector", 0, 255, nothing)
cv2.createTrackbar("V_max", "HSV Range Dectector", 255, 255, nothing)

while True:
    frame = cv2.imread('test_lab_environment.PNG')

    frame = imutils.resize(frame, width=600)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("H_min", "HSV Range Dectector")
    l_s = cv2.getTrackbarPos("S_min", "HSV Range Dectector")
    l_v = cv2.getTrackbarPos("V_min", "HSV Range Dectector")

    u_h = cv2.getTrackbarPos("H_max", "HSV Range Dectector")
    u_s = cv2.getTrackbarPos("S_max", "HSV Range Dectector")
    u_v = cv2.getTrackbarPos("V_max", "HSV Range Dectector")

    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, l_b, u_b)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("frame", frame)
    # cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
