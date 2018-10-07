
from tkinter import *
from tkinter.simpledialog import askstring, askinteger
import json
from DragManager import DragManager

class App:
    canvas = None
    height = 500
    width = 800
    opencvVisualize = False
    hsvVisualize = False
    mobnetVisualize = False
    cloudVisualize = False
    zedposVisualize = False
    timVisualize = False
    zedslamVisualize = False
    ipwebVisualize = False

    opencvrec = None
    opencvlab = None
    hsvrec = None
    hsvlab = None
    mobnetrec = None
    mobnetlab = None
    cloudrec = None
    cloudlab = None
    zedposrec = None
    zedposlab = None
    timrec = None
    timlab = None
    zedslamrec = None
    zedslamlab = None
    ipwebrec = None
    ipweblab = None

    #nested dictionary to pass plugins to output json file
    plugins = {'opencv': {}, 'hsv' : {}, 'cloud': {}, 'mobnet': {}, 'zedpos': {}, 'tim': {}, 'zedslam':{}, 'ipweb': {}}


    def __init__(self, master):
        master.title("Relay")
        frame = Frame(master, height=self.height, width=self.width)
        frame.pack()

        # frame.grid()

        self.canvas = Canvas(frame, height=self.height, width=self.width, bg='yellow')

        toolbar = Frame(master, bg="blue")

        self.button = Button(
            toolbar, text="QUIT", fg="red", padx=5, pady=5, command=frame.quit)
        # self.button.grid(column=4, row=0)
        self.button.pack(side=RIGHT)

        opencvCamera = Button(toolbar, text="OpenCV Camera", fg="red", padx=5, pady=5, command=self.opencvCameraRectangle)
        # camera.grid(column=1, row=0)
        opencvCamera.pack(side=LEFT)

        hsv = Button(toolbar, text="HSV Transform", fg="green", padx=5, pady=5, command=self.hsvRectangle)
        # hsv.grid(column=2, row=0)
        hsv.pack(side=LEFT)

        mobnet = Button(toolbar, text="MobileNetSSD", fg="blue", padx=5, pady=5, command=self.mobnetRectangle)
        # opencv.grid(column=3, row=0)
        mobnet.pack(side=LEFT)

        cloud = Button(toolbar, text="Google Cloud", fg="purple", padx=5, pady=5, command=self.cloudRectangle)
        cloud.pack(side=LEFT)

        zed = Button(toolbar, text="Zed Positioning", fg="orange", padx=5, pady=5, command=self.zedposRectangle)
        zed.pack(side=LEFT)

        tim = Button(toolbar, text="Tim", fg="pink", padx=5, pady=5,command=self.timRectangle)
        tim.pack(side=LEFT)

        zedslam = Button(toolbar, text="Zed Slam", fg="gray", padx=5, pady=5, command=self.zedslamRectangle)
        zedslam.pack(side=LEFT)

        ipweb = Button(toolbar, text="IP Webcam", fg="teal", padx=5, pady=5, command=self.ipwebRectangle)
        ipweb.pack(side=LEFT)

        run = Button(toolbar, text="Run", fg="black", padx=5, pady=5, command=self.writeToJson)
        run.pack(side=LEFT)

        toolbar.pack(side=BOTTOM)

        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

    def opencvCameraRectangle(self):
        ans=0
        if self.opencvVisualize==False:
            ans = askinteger('Enter Integer', 'Please enter the plugin ID')
            # saveListLBL = Label(self.canvas, text="Please enter pluginID: ")
            self.opencvrec = self.canvas.create_rectangle(0, 0, self.width*0.25, self.height*0.25, fill='white', outline='black', width=3)
            self.opencvlab = self.canvas.create_text((((self.width*0.25)/2),(self.height*0.25)/2), text="Camera")
            self.opencvVisualize=True
        else:
            self.canvas.delete(self.opencvrec)
            self.canvas.delete(self.opencvlab)
            self.opencvVisualize=False
            #jsonData = self.establishPlugins("OpenCVCamera, "NoInput", "0", "NoInput", "ImageQueue", "Visualize")
        opencvplugin = self.establishPlugins("OpenCVCamera", "NoInput", "NoInput", ans, "NoInput", "NoInput", "ImageQueue", self.opencvVisualize)
        self.plugins["opencv"] = opencvplugin


    def hsvRectangle(self):
        ans=0
        if self.hsvVisualize==False:
            ans = askinteger('Enter Integer', 'Please enter the plugin ID')
            self.hsvrec = self.canvas.create_rectangle(self.width*0.25, 0, self.width*0.5, self.height*0.25, fill='white', outline='black', width=3)
            self.hsvlab = self.canvas.create_text((self.width*0.25 + self.width*0.25/2, self.height*0.25/2), text="HSV")
            self.hsvVisualize=True
        else:
            self.canvas.delete(self.hsvrec)
            self.canvas.delete(self.hsvlab)
            self.hsvVisualize=False
        #jsonData = self.establishPlugins("HSVTransform", "ImageQueue", "1", "0", "ImageQueue", "Visualize")
        hsvplugin = self.establishPlugins("HSVTransform", "ImageQueue", "NoInput", ans, "0", "NoInput", "ImageQueue", self.hsvVisualize)
        self.plugins["hsv"] = hsvplugin

    def mobnetRectangle(self):
        ans=0
        if self.mobnetVisualize==False:
            ans = askinteger('Enter Integer', 'Please enter the plugin ID')
            self.mobnetrec = self.canvas.create_rectangle(self.width*0.5, 0, self.width*0.75, self.height*0.25, fill='white', outline='black', width=3)
            self.mobnetlab = self.canvas.create_text((self.width*0.5 + self.width*0.25/2, self.height*0.25/2), text="Mobile Net")
            #jsonData = self.establishPlugins("OpenCVCamera", "NoInput", "0", "NoInput", "ImageQueue", "Visualize")
            self.mobnetVisualize=True
        else:
            self.canvas.delete(self.mobnetrec)
            self.canvas.delete(self.mobnetlab)
            self.mobnetVisualize=False
        mobnetplugin = self.establishPlugins("MobileNetSSD", "ImageQueue", "NoInput", ans, "0", "NoInput", "ImageQueue", self.mobnetVisualize)
        self.plugins["mobnet"] = mobnetplugin

    def cloudRectangle(self):
        ans=0
        if self.cloudVisualize==False:
            ans = askinteger('Enter Integer', 'Please enter the plugin ID')
            self.cloudrec = self.canvas.create_rectangle(self.width*0.75 , 0, self.width, self.height*0.25, fill="white", outline='black', width=3)
            self.cloudlab = self.canvas.create_text((self.width*0.75 + self.width/8, self.height*0.25/2), text="Google Cloud")
            self.cloudVisualize=True
        else:
            self.canvas.delete(self.cloudrec)
            self.canvas.delete(self.cloudlab)
            self.cloudVisualize=False
        cloudplugin = self.establishPlugins("GoogleCloudAnnotator", "ImageQueue", "NoInput", ans, "0", "NoInput", "Labels", self.cloudVisualize)
        self.plugins["cloud"] = cloudplugin

    def zedposRectangle(self):
        ans=0
        if self.zedposVisualize==False:
            ans = askinteger('Enter Integer', 'Please enter the plugin ID')
            self.zedposrec = self.canvas.create_rectangle(0, self.height*0.25, self.width*0.25, self.height*0.5, fill="white", outline='black', width='3')
            self.zedposlab = self.canvas.create_text((self.width*0.25/2, self.height*0.25 + self.height*0.25/2), text = "Zed Positioning")
            self.zedposVisualize=True
        else:
            self.canvas.delete(self.zedposrec)
            self.canvas.delete(self.zedposlab)
            self.zedposVisualize=False
        zedposplugin = self.establishPlugins("ZedPositioning", "None", "NoInput", ans, "NoInput", "NoInput", "PositionQueue", self.zedposVisualize)
        self.plugins["zedpos"] = zedposplugin

    # def establishPlugins(self, PluginName, InputType, InputType2, PluginID, Inputs, Inputs2, Outputs, Visualize
    def timRectangle(self):
        ans=0
        if self.timVisualize==False:
            ans = askinteger('Enter Integer', 'Please enter the plugin ID')
            self.timrec = self.canvas.create_rectangle(self.width*0.25, self.height*0.25, self.width*0.5, self.height*0.5, fill="white", outline="black", width='3')
            self.timlab = self.canvas.create_text((self.width*0.25 + self.width*0.25/2, self.height*0.25 + self.height*0.25/2), text = "Tim 551 Component")
            self.timVisualize=True
        else:
            self.canvas.delete(self.timrec)
            self.canvas.delete(self.timlab)
            self.timVisualize=False
        timplugin = self.establishPlugins("tim_551_component", "None", "None", ans, "NoInput", "NoInput", "laserscan", self.timVisualize)
        self.plugins["tim"] = timplugin

    def zedslamRectangle(self):
        ans=0
        if(self.zedslamVisualize==False):
            ans = askinteger('Enter Integer', 'Please enter the plugin ID')
            self.zedslamrec = self.canvas.create_rectangle(self.width*0.5, self.height*0.25, self.width*0.75, self.height*0.5, fill="white", outline="black", width='3')
            self.zedslamlab = self.canvas.create_text((self.width*0.5 + self.width*0.25/2, self.height*0.25 + self.height*0.25/2), text = "Zed Lidar Slam")
            self.zedslamVisualize=True
        else:
            self.canvas.delete(self.zedslamrec)
            self.canvas.delete(self.zedslamlab)
            self.zedslamVisualize=False
        zedslamplugin = self.establishPlugins("Zed_Lidar_SLAM", "laserscan", "0", ans, "0", "Position", "map", self.zedslamVisualize)
        self.plugins["zedslam"] = zedslamplugin


    def ipwebRectangle(self):
        ans=0
        if(self.ipwebVisualize==False):
            ans = askinteger('Enter Integer', 'Please enter the plugin ID')
            self.ipwebrec = self.canvas.create_rectangle(self.width*0.75, self.height*0.25, self.width, self.height*0.5, fill="white", outline="black", width='3')
            self.ipweblab = self.canvas.create_text((self.width*0.75 + self.width*0.25/2, self.height*0.25 + self.height*0.25/2), text = "IP WebCam")
            self.ipwebVisualize=True
        else:
            self.canvas.delete(self.ipwebrec)
            self.canvas.delete(self.ipweblab)
            self.ipwebVisualize=False
        ipwebplugin = self.establishPlugins("IPWebcam", "", "", ans, "", "", "", self.ipwebVisualize)
        self.plugins["ipweb"] = ipwebplugin


    #need to modify still
    def writeToJson(self):
        with open('plugins', 'w') as outfile:
            json.dump(self.plugins, outfile)
        print("Data output to json")

    def establishPlugins(self, PluginName, InputType, InputType2, PluginID, Inputs, Inputs2, Outputs, Visualize):
        jsonData = {'PluginName': PluginName, 'InputType': InputType, 'InputType2' : InputType2, 'PluginID': PluginID, 'Inputs' : Inputs, 'Inputs2': Inputs2, 'Outputs': Outputs, 'Visualize': Visualize}
        return jsonData
    # def addWidgets():


root = Tk()
app = App(root)
root.mainloop()
root.destroy() # optional; see description below