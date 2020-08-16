import cv2
import numpy as np

def max_mim_color(img):
	maxhsv1 = np.amax(img[:,:,0])
	maxhsv2 = np.amax(img[:,:,1])
	maxhsv3 = np.amax(img[:,:,2])
	maxcolor = [maxhsv1,maxhsv2,maxhsv3]
	minhsv1 = np.amin(img[:,:,0])
	minhsv2 = np.amin(img[:,:,1])
	minhsv3 = np.amin(img[:,:,2])
	mincolor = [minhsv1,minhsv2,minhsv3]
	return[mincolor,maxcolor]
def detectColor(cam = 0):
	cap = cv2.VideoCapture(cam)
	ret, frame = cap.read()

	# setup initial location of window
	track_window = cv2.selectROI(frame, False)

	# set up the ROI for tracking
	roi_range_BGR = frame[track_window[1]:track_window[1] + track_window[3], track_window[0]:track_window[0] + track_window[2]]
	roi_range_HSV = cv2.cvtColor(roi_range_BGR, cv2.COLOR_BGR2HSV)
	rangecolor_HSV = max_mim_color(roi_range_HSV)
	rangecolor_BGR = max_mim_color(roi_range_BGR)

	print('HSV:')
	print(rangecolor_HSV)

	cv2.destroyWindow('ROI selector')
	return rangecolor_HSV

rangecolor_HSV=detectColor(cam = 0);
cap = cv2.VideoCapture(0)

while(True):

	ret, frame = cap.read()

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	l_b = np.array(rangecolor_HSV[0])
	u_b = np.array(rangecolor_HSV[1])
	mask = cv2.inRange(hsv, l_b, u_b)
	res = cv2.bitwise_and(frame, frame, mask = mask)

	cv2.imshow('Camera video', frame)
	cv2.imshow("mask", mask)

	if cv2.waitKey(1) == 27: #esc
		break

cap.release()
cv2.destroyAllWindows()