import io
import os
import cv2
import time
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'C:/Users/xpist/Pictures/roadster2.jpg')

# Loads the image into memory
start = time.time()
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations
end = time.time()
print('Labels:')
for label in labels:
    print(label.description)

print(end-start)