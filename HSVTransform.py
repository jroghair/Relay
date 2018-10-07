import cv2
from time import sleep
class HSVTransform:
    def __init__(self, inputImageQueue, outputImageQueue, Visualize):
        print("Creating HSVTransform object")
        self.inputQ = inputImageQueue
        self.outputQ = outputImageQueue
        self.visualize = Visualize
        self.run()

    def run(self):
        while True:
            if(self.inputQ.qsize()>0):
                image = self.inputQ.get()
            else:
                continue
            self.HSVImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            if(self.outputQ.qsize()>1):
                self.outputQ.get()
            self.outputQ.put(self.HSVImage.copy())
            if(self.visualize):
                cv2.imshow("HSVTransform", self.HSVImage)
                cv2.waitKey(1)

