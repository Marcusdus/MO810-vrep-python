from andabb.Robot import Robot
from andabb.ObjectDetectionListener import IObjectDetectionListener
from andabb.ObjectDetectionListener import DetectedObject
from andabb.PositionListener import IPositionListener
from time import sleep
import threading
from typing import List
import math


class RobotMonitor(threading.Thread):
    def __init__(self, robot: Robot, stopEvent: threading.Event, intervalMs=200):
        threading.Thread.__init__(self)
        self.robot = robot
        self.intervalSeconds = intervalMs/1000
        self.stopEvent = stopEvent
        self.frontObjDetecListeners = []
        self.positionListeners = []

    def run(self):
        while not self.stopEvent.is_set():
            self.robot.update()
            self.readPosition()   
            self.readSonarReadings()  
            sleep(self.intervalSeconds)

    def readSonarReadings(self):
        #FIXME: robot should know the position of each sonar
        # 0: 90
        # 1: 50
        # 2: 30
        # 4: 10
        # 5: -10
        # ...
        angles = [math.radians(x) for x in [90, 50, 30, 10, -10, -30, -50, -90]]
        detectedObjs = []
        for i in range(0,8):
            if self.robot.sonarReading[i] != -1:
                detectedObjs.append(DetectedObject(self.robot.sonarReading[i], angles[i], i))

        self.__frontObjectDetected(detectedObjs)

    def readPosition(self):
        if (self.robot.lastPosition != self.robot.position or 
            self.robot.lastOrientation != self.robot.orientation):
            self.__positionChanged(self.robot.position, self.robot.orientation)

    def subscribeToFrontObjectDetection(self, listener: IObjectDetectionListener ):
        self.frontObjDetecListeners.append(listener)
    
    def subscribeChangePosition(self, listener: IPositionListener):
        self.positionListeners.append(listener)

    def __frontObjectDetected(self, detectedObjs: List[DetectedObject]):
        for l in self.frontObjDetecListeners:
            l.objectDetected(detectedObjs)
    
    def __positionChanged(self, newPosition, newOrientation):
        for l in self.positionListeners:
            l.newPosition(newPosition, newOrientation)
