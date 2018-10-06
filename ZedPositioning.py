import pyzed

import pyzed.camera as zcam
import pyzed.types as tp
import pyzed.core as core
import pyzed.defines as sl
import threading

class ZedPositioning():
    def __init__(self, inputQueue, outputQueue, visualize):
        self.inputQueue = inputQueue
        self.outputQueue = outputQueue
        self.visualize = visualize
        init = zcam.PyInitParameters(camera_resolution=sl.PyRESOLUTION.PyRESOLUTION_HD720,
                                     depth_mode=sl.PyDEPTH_MODE.PyDEPTH_MODE_PERFORMANCE,
                                     coordinate_units=sl.PyUNIT.PyUNIT_METER,
                                     coordinate_system=sl.PyCOORDINATE_SYSTEM.PyCOORDINATE_SYSTEM_RIGHT_HANDED_Y_UP,
                                     sdk_verbose=True)
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
        print(camera_pose)

        py_translation = core.PyTranslation()

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
                    self.outputQueue.put(pose_data)
                    if(self.visualize):
                        print(pose_data)
            else:
                tp.c_sleep_ms(1)
