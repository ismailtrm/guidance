###################################################################
### Developer(s): umutzan2, ismailtrm                           ###
### Last Update: 14/11/2024 by ismailtrm                         ###
### Notes: upper red and lower red, configured with using cam.  ###
###                                                             ###
###################################################################

import cv2
import numpy as np

def initialize_camera(camera_index=0):
    return cv2.VideoCapture(camera_index)

def process_frame(frame, lower_red, upper_red, x_axis, y_axis):
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) > 500:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 1)
            center_x = int((w / 2) + x)
            center_y = int((h / 2) + y)
            cv2.circle(frame, (center_x, center_y), 2, (255, 0, 255), -1)
            if x_axis - 20 < center_x < x_axis + 20 and y_axis - 20 < center_y < y_axis + 20:
                cv2.putText(frame, 'Locked', (100, frame.shape[0] - 100), cv2.FONT_ITALIC, 1, (0, 0, 0), 2, cv2.LINE_AA)

    return frame

def main():
    upper_red = np.array([255, 255, 255])
    lower_red = np.array([171, 160, 60])
    
    with initialize_camera() as cap:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            x_axis, y_axis = width // 2, height // 2

            frame = cv2.line(frame, (x_axis, 0), (x_axis, height), (255, 0, 0), 1)
            frame = cv2.line(frame, (0, y_axis), (width, y_axis), (255, 0, 0), 1)
            frame = cv2.circle(frame, (x_axis, y_axis), 20, (0, 0, 255), 1)

            frame = process_frame(frame, lower_red, upper_red, x_axis, y_axis)
            cv2.imshow("window", frame)

            if cv2.waitKey(1) == ord('q'):
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

