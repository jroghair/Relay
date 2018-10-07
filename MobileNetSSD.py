import cv2
import numpy as np
import time, random



# THIS CODE HAS BEEN ADAPTED FROM https://www.pyimagesearch.com/2017/09/11/object-detection-with-deep-learning-and-opencv/
# It is used to illustrate the functionality of our framework.
# We did not design or train the network.

class MobileNetSSD:
    def __init__(self, inputQueue, outputQueue, visualize):
        self.inputQueue = inputQueue
        self.outputQueue = outputQueue
        self.visualize = visualize
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))
        self.net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
        self.minConfidence = .5
        self.id = random.random()
        self.run()

    def run(self):
        while True:
            if(self.inputQueue.qsize()>0):
                image = self.inputQueue.get()
            else:
                continue
            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
            self.net.setInput(blob)
            self.detections = self.net.forward()
            if(self.visualize):
                for i in np.arange(0, self.detections.shape[2]):
                    # extract the confidence (i.e., probability) associated with the
                    # prediction
                    confidence = self.detections[0, 0, i, 2]

                    # filter out weak detections by ensuring the `confidence` is
                    # greater than the minimum confidence
                    if confidence > self.minConfidence:
                        # extract the index of the class label from the `detections`,
                        # then compute the (x, y)-coordinates of the bounding box for
                        # the object
                        idx = int(self.detections[0, 0, i, 1])
                        box = self.detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")

                        # display the prediction
                        label = "{}: {:.2f}%".format(self.CLASSES[idx], confidence * 100)
                        # print("[INFO] {}".format(label))
                        cv2.rectangle(image, (startX, startY), (endX, endY),
                                      self.COLORS[idx], 2)
                        y = startY - 15 if startY - 15 > 15 else startY + 15
                        cv2.putText(image, label, (startX, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS[idx], 2)

                # show the output image
                #cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
                    windowName = "Output: " + str(self.id)
                    cv2.imshow(windowName, image)
                    key = cv2.waitKey(1) & 0xFF
