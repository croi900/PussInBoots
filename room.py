import math
import time
class Room(object):
    items = []
    cameras = []
    id = None 
    def update(self, items):
        new_items = []
        for item in self.items:
            if abs(item.time - time.time()) < 5:
                new_items.append(item)
        self.items.clear()
        self.items = self.items + new_items
        for item in items:
            if item.confidence > 0.25:    
                x1, y1, x2, y2 = item.box.xyxy[0]
                mx = (x1 + x2)/2
                my = (y1 + y2)/2

                b = True
                pos = []
                for p, i in enumerate(self.items):
                    x1, y1, x2, y2 = i.box.xyxy[0]

                    mxi = (x1 + x2)/2
                    myi = (y1 + y2)/2
                    
                    if math.sqrt((mx - mxi)**2 + (my-myi)**2) < 48 and i.name == item.name:
                        b = False
                if b:
                    self.items.append(item)


    def __init__(self, cameras, id):
        self.id = id
        for camera in cameras:
            self.cameras.append(camera)
