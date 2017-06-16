import math
import logging
import threading
from time import sleep
from typing import List

from .ISensorBasedController import ISensorBasedController
from .ObjectDetectionListener import DetectedObject
from .ObjectDetectionListener import IObjectDetectionListener
from .PoseUpdater import GroundTruthPoseUpdater
from .PoseUpdater import IPoseUpdater
from .PositionListener import IPositionListener
from .Robot import Pose
from .Robot import Robot
from .BaseDetectionListener import BaseDetector

from math import degrees

class RobotMonitor(threading.Thread):
    def __init__(self, robot: Robot, poseUpdater: IPoseUpdater, controller: ISensorBasedController,
                 stopEvent: threading.Event, intervalMs=200):
        threading.Thread.__init__(self)
        self.robot = robot
        self.poseUpdater = poseUpdater
        self.gtPoseUpdater = GroundTruthPoseUpdater()
        self.intervalSeconds = intervalMs / 1000
        self.stopEvent = stopEvent
        self.frontObjDetecListeners = []
        self.positionListeners = []
        self.lastRobotPose = Pose()
        self.controller = controller
        self.baseDetector = BaseDetector(self.robot)

    def run(self):
        while not self.stopEvent.is_set():
            self.update()
            sleep(self.intervalSeconds)

    def update(self):
        self.robot.updateSensors()
        self.lastRobotPose = self.robot.pose
        self.robot.gtPose = self.gtPoseUpdater.update(self.robot)
        self.robot.pose = self.poseUpdater.update(self.robot)
        b = self.baseDetector.detectBase()
        print("base: {},{}".format(b.distance,degrees(b.angle)))
        print("base {}".format(b.getAbsolutePosition(self.robot.gtPose)))
        self.readPosition()

        if self.controller:
            lspeed, aspeed = self.controller.compute(self.readSonarReadings())
            logging.debug("Speed: {}, Ang:{} ".format(lspeed, aspeed))
            self.robot.drive(lspeed, aspeed)

    def readSonarReadings(self):
        # 0: 90
        # 1: 50
        # 2: 30
        # 3: 10
        # 4: -10
        # ...
        angles = [math.radians(x) for x in [90, 50, 30, 10, -10, -30, -50, -90]]
        detectedObjs = []
        sensorReadings = []
        for i in range(0, 8):
            if self.robot.sonarReading[i] != -1:
                detectedObjs.append(DetectedObject(self.robot.sonarReading[i], angles[i], i))
                sensorReadings.append(self.robot.sonarReading[i])
            else:
                sensorReadings.append(2.0)

        self.__frontObjectDetected(detectedObjs)
        return sensorReadings

    def readPosition(self):
        if self.lastRobotPose != self.robot.pose:
            self.__positionChanged(self.robot.pose)

    def subscribeToFrontObjectDetection(self, listener: IObjectDetectionListener):
        self.frontObjDetecListeners.append(listener)

    def subscribeChangePosition(self, listener: IPositionListener):
        self.positionListeners.append(listener)

    def __frontObjectDetected(self, detectedObjs: List[DetectedObject]):
        for l in self.frontObjDetecListeners:
            l.objectDetected(detectedObjs)

    def __positionChanged(self, pose):
        for l in self.positionListeners:
            l.newPosition(pose)
