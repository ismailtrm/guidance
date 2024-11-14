###################################################################
### Developer(s): umutzan2, ismailtrm                           ###
### Last Update: 14/11/2024 by ismailtrm                         ###
### Notes: minor adjustments                      ###
###                                                             ###
###################################################################

import cv2
import numpy as np
from typing import Tuple

# Define constants for threshold values
AREA_THRESHOLD = 500

# Define color boundaries
COLORS = {
    "black": {"upper": [50, 50, 100], "lower": [0, 0, 0]},
    "white": {"upper": [0, 0, 255], "lower": [0, 0, 0]},
    "red": {"upper": [255, 255, 255], "lower": [171, 160, 60]},
    "green": {"upper": [102, 255, 255], "lower": [25, 52, 72]},
    "blue": {"upper": [126, 255, 255], "lower": [94, 80, 2]},
    "yellow": {"upper": [44, 255, 255], "lower": [24, 100, 100]},
}

def guidance(theColor: str, video: np.ndarray, xDegree: float, yDegree: float, xPixel: int, yPixel: int) -> Tuple[float, float]:
    """
    Function to guide based on color detection in a video frame.

    Parameters:
    - theColor: Color to detect
    - video: Video frame
    - xDegree: Degree per pixel in the x-axis
    - yDegree: Degree per pixel in the y-axis
    - xPixel: Total pixels in the x-axis
    - yPixel: Total pixels in the y-axis

    Returns:
    - xD: Calculated x degree
    - yD: Calculated y degree
    """
    xD = 500.5
    yD = 500.5

    upper_bound = np.array(COLORS[theColor]["upper"])
    lower_bound = np.array(COLORS[theColor]["lower"])
    img_hsv = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, lower_bound, upper_bound)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > AREA_THRESHOLD:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(video, (x, y), (x + w, y + h), (0, 255, 255), 1)

            center_x = int((w / 2) + x)
            center_y = int((h / 2) + y)
            cv2.circle(video, (center_x, center_y), 2, (255, 0, 255), -1)

            Cx = xDegree / xPixel
            Cy = yDegree / yPixel
            xD = (center_x - (xPixel / 2)) * Cx
            yD = (center_y - (yPixel / 2)) * Cy

    return xD, yD