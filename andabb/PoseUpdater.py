import abc
from math import cos
from math import degrees
from math import sin
from time import time

from andabb.AngleUniverse import addDelta
from .Robot import Pose
from .Robot import Robot
from .Robot import WHEELS_DIST


class IPoseUpdater(object, metaclass=abc.ABCMeta):
    """
    Pose Updater strategy.
    """

    @abc.abstractmethod
    def update(self, robot):
        """
        This method returns the actual object pose.  
        :return: the object pose
        """
        raise NotImplementedError('This method must be implemented')


class GroundTruthPoseUpdater(IPoseUpdater):
    def update(self, robot: Robot):
        position = robot.sim.getObjectPosition(robot.handle)
        orientation = robot.sim.getObjectOrientation(robot.handle)
        p = Pose(position[0], position[1], orientation[2])
        #print("GT pose: {}".format(p))

        return Pose(position[0], position[1], orientation[2])


class OdometryPoseUpdater(IPoseUpdater):
    def __init__(self):
        self.lastPose = Pose()
        self.lastTimestamp = time()
        self.start = True

    def update(self, robot: Robot):
        now = time()

        rWheel = robot.rWheel
        lWheel = robot.lWheel

        if self.start:
            self.lastPose = robot.gtPose
            print("Start pose: {}".format(robot.gtPose))
            self.lastTimestamp = now
            self.start = self.lastPose.isZero()

            return self.lastPose

        vR = rWheel.calculateSpeed()
        vL = lWheel.calculateSpeed()

        print("vR {}, vL{}".format(vR, vL))

        timeDelta = now - self.lastTimestamp
        deltaTheta = (vR - vL) * (timeDelta / WHEELS_DIST)
        deltaSpace = (vR + vL) * (timeDelta / 2)

        print("deltaSpace {}, deltaTheta{}".format(deltaSpace, degrees(deltaTheta)))

        x = self.lastPose.x + (deltaSpace * cos(addDelta(self.lastPose.orientation, deltaTheta / 2)))
        y = self.lastPose.y + (deltaSpace * sin(addDelta(self.lastPose.orientation, deltaTheta / 2)))
        theta = addDelta(self.lastPose.orientation, deltaTheta)

        self.lastTimestamp = now
        self.lastPose = Pose(x, y, theta)

        print("odometry {}".format(self.lastPose))
        return self.lastPose
