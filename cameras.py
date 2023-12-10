import cv2
import inference
from room import Room
import localization as loc
import sys
import time
import curses
    # Open the camera
filtered_classes = ["apple","laptop", "mouse", "bottle", "wine glass", "cup", "remote", "toothbrush", "handbag",
                    "suitcase", "tie", "keyboard", "cell phone", "pizza", "sofa", "chair", "fork", "scissors", "book", "banana"]

rooms = []

def get_capture_devices():
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing. 
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                working_ports.append((dev_port,camera))
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
    return working_ports

devices = get_capture_devices()

def get_frame_it(rooms):
    while True:
        for room in rooms:
            for cap in room.cameras:
                ret, frame = cap.read()
                if not ret:
                    break;
                yield (room.id, frame)

def get_frame(rooms):
    res = []
    for room in rooms:
        for cap in room.cameras:
            ret, frame = cap.read()
            if not ret:
                break;
            res.append((room.id,frame))

    return res

def get_house_objects():
    for idx, frame in get_frame(rooms):
        #if idx == 0: continue
        res = inference.infer(frame, 0)
        new_res = []
        for item in res:
            if item.name in filtered_classes:
                new_res.append(item)
        res = new_res
        

        #for item in res:
         #   print(idx,item.name)
        #print(res)
        for item in res:
            if True:
                x1, y1, x2, y2 = item.box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values
                
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.6
                font_thickness = 2

                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.putText(frame, item.name + " " + str(item.confidence), (x1, y1 + 15), font, font_scale, (0, 255, 0), font_thickness)

        cv2.imshow("Camera", frame)  # Display the frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return
        # Press 'q' to exit
        for room in rooms:
            if room.id == idx:
                room.update(res)
    
    


def main(stdscr):

    stdscr.clear()
    for idx, dev in devices:
        room = Room([],idx)
        room.cameras = [dev]
        rooms.append(room)
    while True:

        get_house_objects()

        loc.localization(rooms)

        stdscr.clear()

            # Display the lists
        for i, lst in enumerate([room.items for room in rooms]):
            stdscr.addstr(i, 0, str([item.name for item in sorted(lst, key=lambda x: x.name)]))

            # Refresh the screen
        stdscr.refresh()

            # Wait for a short period

    for idx, cap in devices:
        cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    curses.wrapper(main)
