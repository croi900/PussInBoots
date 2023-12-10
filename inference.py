from ultralytics import YOLO
import cv2
import math 
import time
# model
model = YOLO("yolo-Weights/yolov8n.pt")

# object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

class Item(object):
    id = None
    box = None
    confidence = None
    time = None
    room = None
    name = None
    def __init__(self, cls, box, confidence, room):
        self.id = cls 
        self.box = box
        self.confidence = confidence
        self.time = time.time()
        self.room = room
        self.name = classNames[self.id]
def infer(img, room):
    ret = []
    results = model(img)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            confidence = math.ceil((box.conf[0]*100))/100
            #print("Confidence --->",confidence)
            cls = int(box.cls[0])
            #print("Class name -->", classNames[cls])
            ret.append(Item(cls, box, confidence, room))

    return ret




