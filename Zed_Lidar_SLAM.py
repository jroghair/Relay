import queue
from math import sin, cos, tan, atan2, pi
import matplotlib.pyplot as plt
import pyqtgraph as pg
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui

class Zed_Lidar_SLAM:
    def __init__(self, inputQueue1, inputQueue2, outputQueue, visualize):
        self.inputQueue1 = inputQueue1
        self.inputQueue2 = inputQueue2
        self.outputQueue = outputQueue
        self.visualize = visualize
        self.map_x_points = []
        self.map_y_points = []
        if(self.visualize):
            self.pw = pg.plot()
            # self.fig = plt.figure()
            # self.ax  = self.fig.add_subplot(111)
            # x = [0]
            # y = [0]
            # self.li, = self.ax.plot(x, y, 'o')
            # self.fig.canvas.draw()
            # plt.pause(.001)


        print("Starting Zed_Lidar_SLAM")
        self.run()

    def map_scan_to_world(self, laserscan, position):
        x, y, z, orientation = position
        global_x = []
        global_y = []
        for theta, radius in laserscan:
            if radius >9.9:
                continue
            theta = theta*pi/180.0
            tempx = x + radius*cos(orientation + theta)
            tempy = y + radius*sin(orientation + theta)
            #print(str(tempx) + ", " + str(tempy))
            global_x.append(tempx)
            global_y.append(tempy)
        return global_x, global_y

    def run(self):
        self.count = 0
        while True:
            self.count+=1
            self.laserscan = self.inputQueue1.get(block=True)
            self.position = self.inputQueue2.get(block=True)
            self.x = self.position[0]
            self.y = self.position[1]
            xlist, ylist = self.map_scan_to_world(self.laserscan, self.position)
            if(self.visualize):
                self.pw.plot(xlist, ylist, clear=False, pen=None, symbol="o")
                pg.QtGui.QGuiApplication.processEvents()
                # if self.count%1 ==0:
                #     self.li.set_xdata(xlist)
                #     self.li.set_ydata(ylist)
                #     self.ax.relim()
                #     self.ax.set_aspect("equal")
                #     self.ax.set_xlim((-10, 10))
                #     self.ax.set_ylim((-10, 10))
                #     self.fig.canvas.draw()
                #     plt.pause(.01)
            # self.map_x_points.extend(xlist)
            # self.map_y_points.extend(ylist)
            # print(list(zip(self.map_x_points, self.map_y_points)))
