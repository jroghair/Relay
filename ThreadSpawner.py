import threading
import queue
import csv
import json
from OpenCVCamera import OpenCVCamera
from HSVTransform import HSVTransform
from GoogleCloudAnnotator import GoogleCloudAnnotator
import random
# Use this file to spawn all threads once the GUI has been used to configure everything

ClassDict = {"OpenCVCamera": OpenCVCamera, "HSVTransform": HSVTransform}

ImageQueue0 = queue.Queue(maxsize=2)
HSVQueue1 = queue.Queue()


configFilename = "SampleJSON.json"

threadList = []
with open(configFilename) as fp:
    json_object = json.load(fp)
    ThreadDefinitionsList = [thread for thread in json_object]
    for defin in ThreadDefinitionsList:
        objectType = eval(defin["PluginName"])
        Output_Queue_name = defin["Outputs"] + defin["PluginID"]
        exec(Output_Queue_name + " = queue.Queue()")
        outputQueue = eval(Output_Queue_name) # outputQueue is the queue object for the output

        InputQueueName = defin["InputType"] + defin["Inputs"] # Ex: "ImageQueue4"
        # Check if the object already exists so we don't overwrite it
        try:
            if type(eval(InputQueueName)) is not None:
                inputQueue = eval(InputQueueName)
            else:
                inputQueue = queue.Queue()
        except:
            inputQueue = queue.Queue()
        visualizeTemp = eval(defin["Visualize"])

        tempargs = (inputQueue, outputQueue, visualizeTemp)
        tempThread = threading.Thread(target=objectType, args=tempargs)
        print(tempargs)
        threadList.append(tempThread)
    for thread in threadList:
        thread.start()





    # Thread1 = threading.Thread(target=OpenCVCamera, args=(ImageQueue0, True))
    # Thread2 = threading.Thread(target = HSVTransform, args=(ImageQueue0, HSVQueue1, True))
    #
    # threadList = [Thread1, Thread2]
    #
    # for thread in threadList:
    #     thread.start()