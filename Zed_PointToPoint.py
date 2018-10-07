import queue
from math import atan2, sin, cos, sqrt, tan, pow, pi
class Zed_PointToPoint:
    def __init__(self, inputQ1, outputQ, vis):
        self.positionQueue = inputQ1
        self.outputQueue = outputQ
        self.visualize = vis
        self.run()

    def distToNextPoint(self, xcur, ycur, xdes, ydes):
        return sqrt(pow(xcur-xdes,2) + pow(ycur-ydes,2))

    def travelForward(self):
        if(self.outputQueue.qsize()>0):
            self.outputQueue.get()
        self.outputQueue.put('f')
        if (self.visualize):
            print("Driving Forward")

    def turnLeft(self):
        if (self.outputQueue.qsize() > 0):
            self.outputQueue.get()
        self.outputQueue.put('l')
        if (self.visualize):
            print("Turning Left")

    def turnRight(self):
        if (self.outputQueue.qsize() > 0):
            self.outputQueue.get()
        self.outputQueue.put('r')
        if (self.visualize):
            print("Turning Right")

    def stop(self):
        if(self.outputQueue.qsize() > 0):
            self.outputQueue.get()
        self.outputQueue.put('s')
        if self.visualize:
            print("Stopping")

    def run(self):
        while True:
            userx = float(eval(input("Input desired x location: " )))
            usery = float(eval(input("Input desired y location: " )))
            distToWaypoint = 100000000
            while distToWaypoint > .5:
                self.position = self.positionQueue.get()
                x, y, z, orientation = self.position
                orientation *= -1
                headingDesired = atan2(usery-y, userx-x)
                smallestDif = headingDesired - orientation
                smallestDif = (((smallestDif*180/pi)+180) % 360 - 180)*pi/180
                atPoint = False
                distToWaypoint = self.distToNextPoint(x, y, userx, usery)
                if self.distToNextPoint(x, y, userx, usery) < .5:
                    atPoint = True
                    if(self.visualize):
                        print("At desired waypoint")
                else:
                    if abs(smallestDif)<20*pi/180:
                        self.travelForward()
                    else:
                        if smallestDif > 0:
                            self.turnRight()
                        else:
                            self.turnLeft()
