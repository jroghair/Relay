import cv2

class OpenCVCamera:
    def __init__(self, inputs, imageQueueOut, visualize):
        self.cap = cv2.VideoCapture(1)
        self.cap.set(3, 720) # Set image width
        self.cap.set(4, 480) # Set image height
        self.OutputQueue = imageQueueOut
        self.visualize = visualize
        self.run()

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if(ret):
                if(self.OutputQueue.qsize()>1):
                    self.OutputQueue.get() # Remove last thing from queue
                else:
                    self.OutputQueue.put(frame)
                if(self.visualize):
                    cv2.imshow("OpenCVCamera", frame)
                    cv2.waitKey(1)
