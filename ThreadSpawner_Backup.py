import threading
import queue
import csv
import json
from OpenCVCamera import OpenCVCamera
from HSVTransform import HSVTransform
from MobileNetSSD import MobileNetSSD
from GoogleCloudAnnotator import GoogleCloudAnnotator
from ZedPositioning import ZedPositioning
from tim_551_component import tim_551_component
from Zed_Lidar_SLAM import Zed_Lidar_SLAM
from IPWebcam import IPWebcam
from differential_drive_plug_in import Motor_Interface
from Zed_PointToPoint import Zed_PointToPoint

import random

# Use this file to spawn all threads once the GUI has been used to configure everything



#configFilename = "SampleJSON_zed_ard_p2p.json"
#configFilename = "SampleJSON_opencvcam_ipcam.json"
#configFilename = "plugins.json"
configFilename = "SampleJSON.json"

threadList = []
outputQueueList = []  # Keep track of all outputs for use in the main thread later
with open(configFilename) as fp:
    json_object = json.load(fp)
    ThreadDefinitionsList = [thread for thread in json_object]
    for defin in ThreadDefinitionsList:
        print("Defin: " + str(defin))
        objectType = eval(defin["PluginName"])
        Output_Queue_name = defin["Outputs"] + defin["PluginID"]
        exec(Output_Queue_name + " = queue.LifoQueue(maxsize=4)")
        outputQueue = eval(Output_Queue_name)  # outputQueue is the queue object for the output
        outputQueueList.append(outputQueue)

        InputQueueName = defin["InputType"] + defin["Inputs"]  # Ex: "ImageQueue4"
        # Check if the object already exists so we don't overwrite it
        try:
            if type(eval(InputQueueName)) is not None:
                inputQueue = eval(InputQueueName)
            else:
                inputQueue = queue.Queue()
        except:
            inputQueue = queue.Queue()

        if(defin["InputType2"] == "Position"):
            print(defin["InputType2"])
            inputQueue2Name = defin["InputType2"] + defin["Inputs2"]
            inputQueue2 = eval(inputQueue2Name)
        else:
            if(defin["InputType2"] == "COM_Port"):
                inputQueue2 = defin["Inputs2"]
            else:
                inputQueue2 = False
        visualizeTemp = eval(defin["Visualize"])
        if inputQueue2:
            tempargs = (inputQueue, inputQueue2, outputQueue, visualizeTemp)
        else:
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
