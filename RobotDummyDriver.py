from PositionListener import IPositionListener
from ObjectDetectionListener import IObjectDetectionListener
from ObjectDetectionListener import DetectedObject
from Robot import Robot
from typing import List
from enum import Enum
import math
import threading
from time import sleep
import copy
import random

class DrivingState(Enum):
    STRAIGHT = 0
    LEFT_TURN = 1

class RobotDummyDriver(threading.Thread, IObjectDetectionListener):
    '''
    This is a pretty dummy driver: everytime it detects an
    object (front sensors) the robot turns to the left (random)
    '''
    def __init__(self, robot: Robot, stopEvent: threading.Event):
        threading.Thread.__init__(self)
        self.robot = robot
        self.state = DrivingState.STRAIGHT
        self.stopEvent = stopEvent
        self.detectedObject = None
        random.seed(1)
    

    def objectDetected(self, detectedObjs: List[DetectedObject]):
        for d in detectedObjs:
            if self.state != DrivingState.STRAIGHT:
                pass
            # Front object detected
            if d.sensorIndex == 3 or d.sensorIndex == 4:
                self.detectedObject = d

    def __objectDetected(self, detectedObj : DetectedObject):
        self.turnLeft()
            
    def run(self):
        self.driveStraight()
        while not self.stopEvent.is_set():   
            if self.detectedObject:
                d = copy.copy(self.detectedObject)
                self.detectedObject = None
                self.__objectDetected(d) 
            sleep(0.01)

    def driveStraight(self):
        self.state = DrivingState.STRAIGHT
        self.robot.drive(15,0)

    def turnLeft(self):
        self.robot.stop()
        self.state = DrivingState.LEFT_TURN
        self.robot.drive(0, 25)
        sleep(random.random())
        self.driveStraight()
