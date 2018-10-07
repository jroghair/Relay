import io
import os
import cv2
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
import os

class GoogleCloudAnnotator:
    def __init__(self, inputQueue, outputQueue, visualize):
        self.inputQueue = inputQueue
        self.outputQueue = outputQueue
        self.visualize = visualize
        self.client = vision.ImageAnnotatorClient()
        self.run()

    def run(self):
        while True:
            if (self.inputQueue.qsize() > 0):
                image = self.inputQueue.get()
            else:
                continue
            content = cv2.imencode('.jpg', image)[1].tostring()
            image = types.Image(content=content)
            response = self.client.label_detection(image=image)
            labels = response.label_annotations
            if(self.visualize):
                print('Labels:')
                for label in labels:
                    if(label.score>.8):
                        print(label.description)