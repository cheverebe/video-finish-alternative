import numpy as np
import cv2
from datetime import datetime, timedelta

start = datetime.now()
cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    actual = datetime.now()
    diff = actual - start
    diff_str = str(diff)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(gray, diff_str,(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)
    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
