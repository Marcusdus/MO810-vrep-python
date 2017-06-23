import abc
import logging
from math import cos
from math import degrees
from math import sin
from math import sqrt
from time import time
from typing import List

from numpy import concatenate
from numpy import matrix
from numpy import transpose
from numpy import zeros
from numpy.linalg import inv

from andabb.AngleUniverse import addDelta, addAngles
from .BaseDetectionListener import IBaseDetectionListener, DetectedBase
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
        # logging.debug("GT pose: {}".format(p))

        return Pose(position[0], position[1], orientation[2])


class OdometryPoseUpdater(IPoseUpdater):
    def __init__(self):
        self.lastPose = Pose()
        self.lastTimestamp = time()
        self.start = True
        self.vL = 0
        self.vR = 0
        self.deltaTime = 0
        self.deltaTheta = 0
        self.deltaSpace = 0

    def update(self, robot: Robot):
        now = time()

        rWheel = robot.rWheel
        lWheel = robot.lWheel
        vR = rWheel.calculateSpeed()
        vL = lWheel.calculateSpeed()

        if self.start:
            self.lastPose = robot.gtPose
            # logging.debug("Start pose: {}".format(robot.gtPose))
            self.lastTimestamp = now
            self.start = self.lastPose.isZero() or (vR == 0 and vL == 0)

            return self.lastPose

        logging.debug("vR {}, vL{}".format(vR, vL))

        timeDelta = now - self.lastTimestamp
        deltaTheta = (vR - vL) * (timeDelta / WHEELS_DIST)
        deltaSpace = (vR + vL) * (timeDelta / 2)

        logging.debug("deltaSpace {}, deltaTheta{}".format(deltaSpace, degrees(deltaTheta)))

        x = self.lastPose.x + (deltaSpace * cos(addDelta(self.lastPose.orientation, deltaTheta / 2)))
        y = self.lastPose.y + (deltaSpace * sin(addDelta(self.lastPose.orientation, deltaTheta / 2)))
        theta = addDelta(self.lastPose.orientation, deltaTheta)

        self.lastTimestamp = now
        self.lastPose = Pose(x, y, theta)

        self.vL = vL
        self.vR = vR
        self.deltaTheta = timeDelta
        self.deltaTheta = deltaTheta
        self.deltaSpace = deltaSpace

        logging.debug("odometry {}".format(self.lastPose))
        return self.lastPose


class KalmanFilterPoseUpdater(IPoseUpdater, IBaseDetectionListener):
    def __init__(self, odometryUpdater: OdometryPoseUpdater):
        self.odometryUpdater = odometryUpdater
        self.lastPose = Pose()
        self.start = True
        self.lastDetectedBases = None
        self.lastCovariance = matrix([[0, 0, 0],
                                      [0, 0, 0],
                                      [0, 0, 0]])
        self.I = matrix([[1, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1]])

    def update(self, robot: Robot):
        pose = self.odometryUpdater.update(robot)

        deltaTheta = self.odometryUpdater.deltaTheta
        deltaSpace = self.odometryUpdater.deltaSpace
        bases = self.lastDetectedBases

        if self.start:
            self.lastPose = robot.gtPose
            logging.debug("Start pose: {}".format(robot.gtPose))
            self.start = self.lastPose.isZero() or bases is None or (bases[0].localY == 0 and bases[0].localX == 0)
            return self.lastPose

        logging.debug("before kalman: pose {}, gt{}".format(pose, robot.gtPose))

        # Prediction step
        gt = self._gtMatrix(pose.orientation, deltaTheta, deltaSpace)
        vt = self._vtMatrix(pose.orientation, deltaTheta, deltaSpace)
        covDt = self._covarianceDTMatrix(deltaTheta, deltaSpace)
        rt = self._rtMatrix()
        predictCov = ((gt * self.lastCovariance) * transpose(gt)) + ((vt * covDt) * transpose(vt)) + rt

        # Update step
        bases = self.lastDetectedBases
        ht = self._htMatrix(bases, pose.x, pose.y)
        qt = self._qtMatrix(len(bases))
        m = inv(((ht * predictCov) * transpose(ht)) + qt)
        kt = (predictCov * transpose(ht)) * m

        inova = None
        for base in bases:
            mnova = base.calculateResidualRangeAndBearing(pose)
            if inova is None:
                inova = mnova
            else:
                inova = concatenate((inova, mnova))

        logging.debug("inova: {}".format(inova))

        addPose = kt * inova

        logging.debug("deltaPose: {}".format(addPose))

        logging.debug(float(addPose[0][0]))
        self.lastPose = Pose(pose.x + addPose[0, 0], pose.y + addPose[1, 0],
                             addAngles(pose.orientation, addPose[2, 0]))
        logging.debug("after kalman: pose {}, gt{}".format(self.lastPose, robot.gtPose))

        # Updating covariance
        self.lastCovariance = (self.I - (kt * ht)) * predictCov

        # Updating odometry
        self.odometryUpdater.lastPose = self.lastPose

        return self.lastPose

    def _gtMatrix(self, prevTheta, deltaTheta, deltaSpace):
        ang = addAngles(prevTheta, (deltaTheta / 2))
        return matrix([[1, 0, -deltaSpace * sin(ang)],
                       [0, 1, deltaSpace * cos(ang)],
                       [0, 0, 1]])

    def _vtMatrix(self, prevTheta, deltaTheta, deltaSpace):
        ang = addAngles(prevTheta, (deltaTheta / 2))
        sp = deltaSpace / (2 * WHEELS_DIST)
        return matrix([[(0.5 * cos(ang)) - (sp * sin(ang)), (0.5 * cos(ang) + (sp * sin(ang)))],
                       [(0.5 * sin(ang)) + (sp * cos(ang)), (0.5 * sin(ang) - (sp * cos(ang)))],
                       [1 / WHEELS_DIST, -1 / WHEELS_DIST]])

    def _covarianceDTMatrix(self, deltaTheta, deltaSpace):
        ks = 0.1
        kt = 0.1
        return matrix([[ks * abs(deltaSpace), 0],
                       [0, kt * abs(deltaTheta)]])

    def _rtMatrix(self):
        errorX = 1
        errorY = 1
        errorTheta = 1
        return matrix([[errorX ** 2, 0, 0],
                       [0, errorY ** 2, 0],
                       [0, 0, errorTheta ** 2]])

    def _htMatrix(self, bases: List[DetectedBase], x, y):
        m = None
        for base in bases:
            rx = base.realX
            ry = base.realY
            q = ((rx - x) ** 2) + ((ry - y) ** 2)
            sqrtq = sqrt(q)

            n = matrix([[-(rx - x) / (sqrtq), -(ry - y) / sqrtq, 0],
                        [(ry - y) / q, -(rx - x) / q, -1]])
            if m is None:
                m = n
            else:
                m = concatenate((m, n))
        return m

    def _qtMatrix(self, num):
        errorAccDistance = 0.5
        errorAccAngle = 0.1
        m = zeros(shape=(2 * num, 2 * num))
        for i in range(0, num):
            j = i * 2
            m[j, j] = errorAccDistance ** 2
            m[j + 1, j + 1] = errorAccAngle ** 2

        return m

    def baseDetected(self, bases: List[DetectedBase]):
        self.lastDetectedBases = bases
