import cv2
import datetime
import imutils
from globals.constants import MD_MIN_OBJECT_AREA

class MotionDetector:
    def __init__(self):
        self.avg_image = None

    def detect(self, image):
        # Resize the image, grayscale and median blur
        image = imutils.resize(image, width=600)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the average image is None, initialize it
        if self.avg_image is None:
            self.avg_image = blur.copy().astype("float")
            return (False, 0)
        else:
            # accumulate the weighted average
            # compute the difference between 
            # the current image and average
            cv2.accumulateWeighted(blur, self.avg_image, 0.5)
            diff = cv2.absdiff(blur, cv2.convertScaleAbs(self.avg_image))

            # threshold the diff image, dilate and find contours
            thresholded = cv2.threshold(diff, 5, 255, cv2.THRESH_BINARY)[1]
            thresholded = cv2.dilate(thresholded, None, iterations=2)
            cnts = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            
            cnts = list(filter(lambda cnt: cv2.contourArea(cnt) > MD_MIN_OBJECT_AREA, cnts))
            n_cnts = len(cnts)

            return (len(cnts) > 0, n_cnts)