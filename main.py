import numpy as np
import cv2
from datetime import datetime, timedelta
refPt = []
cropping = False

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False


def has_changed(prev_roi, actual_roi):
    diff_a = actual_roi-prev_roi
    print(diff_a.max())
    return diff_a.max() > 20

start = datetime.now()
cap = cv2.VideoCapture(0)
show = True
running = True
started = False
first_roi = True
prev_roi = None
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
while show:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if running:
        actual = datetime.now()
    if started:
        diff = actual - start
    else:
        diff = timedelta()
    diff_str = str(diff)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(gray, diff_str,(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)
    if len(refPt) == 2:
        clone = gray.copy()
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        cv2.rectangle(gray,(refPt[0][0],refPt[0][1]),(refPt[1][0],refPt[1][1]),(0,255,0),1)
        cv2.imshow("ROI", roi)
        if first_roi:
            first_roi = False
        else:
            if has_changed(prev_roi, roi):
                started = True
        prev_roi = roi
        prev_roi = roi

    # Display the resulting frame
    cv2.imshow('image',gray)
    c = cv2.waitKey(80)
    if not (c == -1):
        if c == 27:
            show = False
        else:
            running = False

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
