import unittest

from numpy import matrix
from andabb.BaseDetectionListener import BaseDetector
from andabb.Robot import Pose
from math import radians

class KalmanTest(unittest.TestCase):
    def testX(self):
        m = x()
        print(m)
        print(m[0])
        print(m[1])

    def testBasePosition(self):
        bd = BaseDetector(None)
        base = bd.calculateBase(4.275537967681885, 4.467638969421387, 4.446549892425537)
        p = Pose(-2.81, -3.40, radians(-57.485))
        print(base.getAbsolutePosition(p))

    def testBearing(self):
        bd = BaseDetector(None)
        base = bd.calculateBase(4.083703517913818, 4.02016019821167, 4.288288593292236)
        p = Pose(4.19, -0.02, radians(-17.572))
        eb = base.getEstimatedRangeAndBearing(p)
        rb = base.getRealRangeAndBearing(p)
        print(eb)
        print(rb)


def _qtMatrix():
    errorAccDistance = 0.1
    errorAccAngle = 0.1
    errorAccDistance = 0.1
    errorAccAngle = 0.1
    return matrix([
        [errorAccDistance ** 2, 0],
        [0, errorAccAngle ** 2]
    ])


def x():
    A = matrix([[-9.98804582e-01, 9.61287574e-02],
                [-3.98754095e-02, -2.43117185e+00],
                [7.10362595e-05, -5.48737709e-01]])
    B = matrix([[-5.45581005],
                [-0.03951914]])
    return A * B
