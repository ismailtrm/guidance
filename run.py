###################################################################
### Developer(s): umutzan2, ismailtrm                           ###
### Last Update: 14/11/2024by ismailtrm                          ###
### Notes: minor adjustments                             ###
###                                                             ###
###################################################################

import sys
from pymavlink import mavutil
import cv2
from theScript import guidance
import time

def initialize_camera(camera_index):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Unable to open camera {camera_index}")
        sys.exit()
    return cap

def initialize_mavlink(connection_string, baud_rate):
    master = mavutil.mavlink_connection(connection_string, baud=baud_rate)
    if not master:
        print("Error: Unable to establish mavlink connection")
        sys.exit()
    return master

def set_rc_channel_pwm(master, id, pwm=1500):
    if id < 1:
        print("Channel does not exist.")
        return
    
    if id < 9:
        rc_channel_values = [65535 for _ in range(8)]
        rc_channel_values[id - 1] = pwm
        master.mav.rc_channels_override_send(
            master.target_system,
            master.target_component,
            *rc_channel_values
        )

def process_video(cap, cap2, master):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from camera 0")
            break

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        x, y = guidance("red", frame, 135, 135, width, height)

        if x == 500.5:
            set_rc_channel_pwm(master, 6, 1450)
            set_rc_channel_pwm(master, 3, 1950)
            set_rc_channel_pwm(master, 5, 1600)

        elif -6 < x < 6:
            set_rc_channel_pwm(master, 6, 1500)
            set_rc_channel_pwm(master, 3, 1500)
            set_rc_channel_pwm(master, 5, 1500)
            process_secondary_camera(cap2, master)

        elif 0 < x < 200:
            set_rc_channel_pwm(master, 6, 1500)
            set_rc_channel_pwm(master, 3, 1500)
            set_rc_channel_pwm(master, 5, 1500)
            print("Object on the right")
            while x > 5:
                print(x)
                set_rc_channel_pwm(master, 6, 1550)
            set_rc_channel_pwm(master, 6, 1500)

        elif x < 0:
            set_rc_channel_pwm(master, 6, 1500)
            set_rc_channel_pwm(master, 5, 1500)
            set_rc_channel_pwm(master, 3, 1500)
            print("Object on the left")
            while x < -5:
                print(x)
                set_rc_channel_pwm(master, 6, 1450)
            set_rc_channel_pwm(master, 6, 1500)

    cap.release()
    cv2.destroyAllWindows()

def process_secondary_camera(cap2, master):
    while True:
        ret, frame2 = cap2.read()
        if not ret:
            print("Error: Unable to read from camera 2")
            break

        width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
        height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))

        x2, y2 = guidance("red", frame2, 135, 135, width2, height2)
        set_rc_channel_pwm(master, 5, 1600)
        if y2 < -16:
            print("Reached")
            set_rc_channel_pwm(master, 5, 1500)
            set_rc_channel_pwm(master, 3, 1950)
            time.sleep(7)
            sys.exit()

def main():
    cap = initialize_camera(0)
    cap2 = initialize_camera(2)
    master = initialize_mavlink('/dev/serial0', 57600)
    
    process_video(cap, cap2, master)

if __name__ == "__main__":
    main()