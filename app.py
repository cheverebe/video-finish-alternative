from datetime import datetime, timedelta
import cv2
from videorecorder import VideoRecorder
import numpy as np


class App(object):
    def __init__(self):
        self.start = datetime.now()
        self.cap = cv2.VideoCapture(0)
        self.recorder = VideoRecorder(self.cap)
        self.show = True
        self.running = True
        self.started = False
        self.first_roi = 3
        self.prev_roi = None
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.click_and_crop)

        self.refPt = []
        self.cropping = False

    @staticmethod
    def has_changed(prev_roi, actual_roi):
        prev_roi = cv2.cvtColor(prev_roi, cv2.COLOR_BGR2GRAY)
        actual_roi = cv2.cvtColor(actual_roi, cv2.COLOR_BGR2GRAY)

        err = np.sum((prev_roi.astype("float") - actual_roi.astype("float")) ** 2)
        err /= float(prev_roi.shape[0] * prev_roi.shape[1])
        return err > 80

    def click_and_crop(self, event, x, y, flags, param):

        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPt = [(x, y)]
            self.cropping = True

        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            self.refPt.append((x, y))
            self.cropping = False

    def run(self):
        while self.show:
            # Capture frame-by-frame
            ret, frame = self.cap.read()

            # Our operations on the frame come here
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = frame
            if self.running:
                actual = datetime.now()
            if self.started:
                diff = actual - self.start
            else:
                diff = timedelta()
            diff_str = str(diff)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(gray, diff_str,(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)
            self.recorder.write(gray)
            if len(self.refPt) == 2:
                clone = gray.copy()
                roi = clone[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]
                cv2.rectangle(gray,(self.refPt[0][0],self.refPt[0][1]),(self.refPt[1][0],self.refPt[1][1]),(0,255,0),1)
                #cv2.imshow("ROI", roi)
                if self.first_roi:
                    self.first_roi -= 1
                else:
                    if self.has_changed(prev_roi, roi):
                        self.started = True
                prev_roi = roi

            # Display the resulting frame
            cv2.imshow('image',gray)
            c = cv2.waitKey(80)
            if not (c == -1):
                if c == 27:
                    self.show = False
                else:
                    self.running = False

        # When everything done, release the capture
        self.recorder.release()
        self.cap.release()
        cv2.destroyAllWindows()