import pyzed

import pyzed.camera as zcam
import pyzed.types as tp
import pyzed.core as core
import pyzed.defines as sl
import threading, os
import pyqtgraph as pg

from PyQt5 import QtCore, QtWidgets, QtGui
import matplotlib.pyplot as plt
import cv2


class ZedPositioning():
    def __init__(self, inputQueue, outputQueue, visualize):
        self.inputQueue = inputQueue
        self.outputQueue = outputQueue
        self.visualize = visualize
        self.xlist = []
        self.ylist = []
        # if(self.visualize):

        init = zcam.PyInitParameters(camera_resolution=sl.PyRESOLUTION.PyRESOLUTION_VGA,
                                     depth_mode=sl.PyDEPTH_MODE.PyDEPTH_MODE_PERFORMANCE,
                                     coordinate_units=sl.PyUNIT.PyUNIT_METER,
                                     coordinate_system=sl.PyCOORDINATE_SYSTEM.PyCOORDINATE_SYSTEM_RIGHT_HANDED_Y_UP,
                                     sdk_verbose=False)
        cam = zcam.PyZEDCamera()
        status = cam.open(init)
        if status != tp.PyERROR_CODE.PySUCCESS:
            print(repr(status))
            exit()

        transform = core.PyTransform()
        tracking_params = zcam.PyTrackingParameters(transform)
        cam.enable_tracking(tracking_params)

        runtime = zcam.PyRuntimeParameters()
        camera_pose = zcam.PyPose()

        py_translation = core.PyTranslation()
        print("Starting ZEDPositioning")
        self.start_zed(cam, runtime, camera_pose, py_translation)

    def start_zed(self, cam, runtime, camera_pose, py_translation):
        zed_callback = threading.Thread(target=self.run, args=(cam, runtime, camera_pose, py_translation))
        zed_callback.start()

    def run(self, cam, runtime, camera_pose, py_translation):
        while True:
            if cam.grab(runtime) == tp.PyERROR_CODE.PySUCCESS:
                tracking_state = cam.get_position(camera_pose)
                text_translation = ""
                text_rotation = ""
                if tracking_state == sl.PyTRACKING_STATE.PyTRACKING_STATE_OK:
                    rotation = camera_pose.get_rotation_vector()
                    rx = round(rotation[0], 2)
                    ry = round(rotation[1], 2)
                    rz = round(rotation[2], 2)

                    translation = camera_pose.get_translation(py_translation)
                    tx = round(translation.get()[0], 2)
                    ty = round(translation.get()[1], 2)
                    tz = round(translation.get()[2], 2)

                    text_translation = str((tx, ty, tz))
                    text_rotation = str((rx, ry, rz))
                    pose_data = camera_pose.pose_data(core.PyTransform())
                    self.x = float(pose_data[0][3])
                    self.y = -float(pose_data[2][3])
                    self.z = float(pose_data[1][3])
                    self.orientation = float(ry)
                    self.xlist.append(self.x)
                    self.ylist.append(self.y)
                    self.position = [self.x, self.y, self.z, self.orientation]
                    if self.outputQueue.qsize()==0:
                        self.outputQueue.put(self.position)
                    else:
                        self.outputQueue.get()
                        self.outputQueue.put(self.position)
                    if(self.visualize):
                        ax2 = plt.subplot(211)
                        ax2.set_aspect("equal")
                        ax2.scatter(self.x, self.y, c = 'r', s = 3)
                        plt.savefig("Test.png")
                        tempimg = cv2.imread("Test.png")
                        cv2.imshow("ZedPositioning", tempimg)
                        os.remove('Test.png')
                        cv2.waitKey(1)
            else:
                tp.c_sleep_ms(1)
