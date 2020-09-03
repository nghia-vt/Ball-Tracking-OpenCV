# USAGE:
# detail: python3 ball_tracking.py --help
# python3 ball_tracking.py --video object_tracking_example.mp4
# python3 ball_tracking.py --camera 0 --color green
# press the 'q' key to stop

# import the necessary packages
import argparse
import imutils
import cv2
from collections import deque
import numpy as np
import time
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "path to the video file")
ap.add_argument("-cam", "--camera", type = int, default = 0, help = "index of camera")
ap.add_argument("-cl", "--color", type = str, default = 'green', help = "select ball color (green or blue)")
args = vars(ap.parse_args())
 
# if a video path was not supplied, grab the reference to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(args["camera"])
 
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# define the color ranges
colorList = [ ((29, 86, 6), (64, 255, 255), "green"),
				((57, 68, 0), (151, 255, 255), "blue")]
if args.get("color") == "green":
	colorRange = colorList[0]
elif args.get("color") == "blue":
	colorRange = colorList[1]

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
bufferSize = 32
pts = deque(maxlen=bufferSize)
(dX, dY) = (0, 0)
direction = ""

# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:

	startTime = time.time()

	# grab the current frame
	(grabbed, frame) = camera.read()
 
	# if we are viewing a video and we did not grab a frame, then we have
	# reached the end of the video
	if args.get("video") and not grabbed or frame is None:
		break
 
	# resize the frame, blur it, and convert it to the HSV color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the colors in the current HSV range, then
	# perform a series of dilations and erosions to remove any small
	# blobs left in the mask
	(lower, upper, colorName) = colorRange;
	mask = cv2.inRange(hsv, lower, upper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use it to compute
		# the minimum enclosing circle and centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only draw the enclosing circle, centroid and text if the radious meets
		# a minimum size
		# then update the list of tracked points
		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			cv2.putText(frame, "x={}, y={}".format(cX, cY), (cX + 10, cY), 
				cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1, lineType=cv2.LINE_AA)
			cv2.putText(frame, "r=" + str(np.round(radius, 2)), (cX + 10, cY + 15), 
				cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1, lineType=cv2.LINE_AA)

			pts.appendleft(center)

	# loop over the set of tracked points
	for i in np.arange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# check to see if enough points have been accumulated in
		# the buffer
		if len(pts) >= 10 and i == 1 and pts[-10] is not None:
			# compute the difference between the x and y
			# coordinates and re-initialize the direction
			# text variables
			dX = pts[-10][0] - pts[i][0]
			dY = pts[-10][1] - pts[i][1]
			(dirX, dirY) = ("", "")

			# ensure there is significant movement in the
			# x-direction
			if np.abs(dX) > 20:
				dirX = "East" if np.sign(dX) == 1 else "West"

			# ensure there is significant movement in the
			# y-direction
			if np.abs(dY) > 20:
				dirY = "North" if np.sign(dY) == 1 else "South"

			# handle when both directions are non-empty
			if dirX != "" and dirY != "":
				direction = "{}-{}".format(dirY, dirX)

			# otherwise, only one direction is non-empty
			else:
				direction = dirX if dirX != "" else dirY

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(bufferSize / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show the movement deltas and the direction of movement on
	# the frame
	cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, lineType=cv2.LINE_AA)
	cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY), (10, frame.shape[0] - 10), 
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, lineType=cv2.LINE_AA)
	cv2.putText(frame, 'fps:' + str(np.round(1/(time.time()-startTime))), (10, frame.shape[0] - 30), 
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 50, 150), 1, lineType=cv2.LINE_AA)

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()