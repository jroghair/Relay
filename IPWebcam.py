import cv2
import urllib, time
import numpy as np
import queue

class IPWebcam:
    def __init__(self, inputQueue, outputQueue, visualize):
        self.url = "http://172.17.103.141:8080/shot.jpg"
        self.inputQueue = inputQueue
        self.outputQueue = outputQueue
        self.visualize = visualize
        self.run()
    def run(self):
        while True:
            imageResp = urllib.request.urlopen(self.url)
            image = np.array(bytearray(imageResp.read()), dtype=np.uint8)
            image = cv2.imdecode(image, -1)
            if(self.outputQueue.qsize()==0):
                self.outputQueue.put(image)
            else:
                self.outputQueue.get()
                self.outputQueue.put(image)
            if(self.visualize):
                cv2.imshow("IPWebcam", image)
                cv2.waitKey(1)