import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from andabb.Robot import Robot
from andabb.Robot import WHEELS_RAD
from andabb.ObjectDetectionListener import IObjectDetectionListener
from andabb.PositionListener import IPositionListener
from andabb.ObjectDetectionListener import DetectedObject
from andabb.RobotMonitor import RobotMonitor
from .PoseUpdater import GroundTruthPoseUpdater
from .PoseUpdater import Pose
from typing import List
import math
import threading

class DynamicPlot(IPositionListener, IObjectDetectionListener):
    def __init__(self):
        self.pos_x = []
        self.pos_y = []
        self.detected = []

        self.lastX = 0
        self.lastY = 0
        self.lastAngle = 0

    def newPosition(self, pose: Pose):
        self.pos_x.append(pose.x)
        self.pos_y.append(pose.y)
        self.lastX, self.lastY = pose.x, pose.y
        self.lastAngle = pose.orientation

    def objectDetected(self, detectedObjs: List[DetectedObject] ):
        for d in detectedObjs:
            self.detected.append(d)

    # TODO: we need to check if this is correct!
    def abs_pos_x(self, d):
        return self.lastX + ((WHEELS_RAD + d.dist) * math.cos(self.lastAngle + d.angle))

    def abs_pos_y(self, d):
        return self.lastY + ((WHEELS_RAD + d.dist) * math.sin(self.lastAngle + d.angle))

def updateRobotAndObjects(num, d:DynamicPlot, robotGraph, linesList):
    robotGraph.set_xdata(d.pos_x)
    robotGraph.set_ydata(d.pos_y) 

    for detected in d.detected:
        hl = linesList[detected.sensorIndex]
        hl.set_xdata(np.append(hl.get_xdata(), d.abs_pos_x(detected)))
        hl.set_ydata(np.append(hl.get_ydata(), d.abs_pos_y(detected)))

    d.detected.clear()

    return robotGraph,(*linesList),

def plotRobotAndObjects(monitor: RobotMonitor, intervalMs=500):
    dp = DynamicPlot()
    monitor.subscribeChangePosition(dp)
    monitor.subscribeToFrontObjectDetection(dp)

    fig1 = plt.figure()
    linesList = [None] * 8 

    robotLine, = plt.plot([], [], 'ro', label='robot')
    robotLine.set_markersize(1)

    for i in range(0,8):
        l, = plt.plot([], [], 'o', label='sensor'+(str(i+1)))
        l.set_markersize(1)
        linesList[i] = l
        l.set_color('C' + str(i))

    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Robot and Objects detected by Sensors')
    leg = plt.legend(bbox_to_anchor=(1.1, 1.05))

    for l in leg.get_lines():
        l.set_marker('.')
        l.set_markersize(5)

    line_ani = animation.FuncAnimation(fig1, updateRobotAndObjects, None, fargs=(dp, robotLine, linesList),
                                    interval=intervalMs, blit=True, repeat=False)

    # To save the animation, use the command: line_ani.save('lines.mp4')
    plt.show()

def update_line(num, robot:Robot, hl):
    robot.update()
    pos = robot.position[0:2]
    hl.set_xdata(np.append(hl.get_xdata(), pos[0]))
    hl.set_ydata(np.append(hl.get_ydata(), pos[1]))
    return hl,

def plotRobot(robot: Robot, intervalMs=500):
    fig1 = plt.figure()

    l, = plt.plot([], [], 'ro', markersize=1)
    plt.xlim(-20, 20)
    plt.ylim(-20, 20)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('test')
    line_ani = animation.FuncAnimation(fig1, update_line, None, fargs=(robot, l),
                                    interval=intervalMs, blit=True, repeat=False)

    # To save the animation, use the command: line_ani.save('lines.mp4')
    plt.show()

def main():
    from andabb.Simulator import Simulator
    
    sim = Simulator()
    sim.connect()

    poseUpdater = GroundTruthPoseUpdater()

    robot = Robot(sim, "Pioneer_p3dx", poseUpdater)
    stopEvent = threading.Event()
    monitor = RobotMonitor(robot, stopEvent)
    monitor.start()
    plotRobotAndObjects(monitor)
    stopEvent.set()
    monitor.join()
    sim.disconnect()
