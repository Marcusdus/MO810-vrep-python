import logging
import unittest

from math import radians

from andabb.BaseDetectionListener import BaseDetector
from andabb.Robot import Pose
from andabb.BaseDetectionListener import RealLandmark

base1 = RealLandmark("Base", 0.0, 0.0)
base2 = RealLandmark("Base2", -0.5, -0.5)

class KalmanTest(unittest.TestCase):


    def testBasePosition(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        bd = BaseDetector(None)
        base = bd.calculateBase(base1, 1.04, 1.04, 0.75)
        pose = Pose(-1.02, 0.37, -0.28)
        print(base.getAbsolutePosition(pose))
        print(base.localX)
        print(base.localY)
        print(base.calculateResidualRangeAndBearing(pose))

    def testBasePosition2(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        bd = BaseDetector(None)
        base = bd.calculateBase(base1, 4.00, 4.01, 4.26)
        pose = Pose(4.57, -0.05, 0.07)
        print(base.getAbsolutePosition(pose))
        print(base.localX)
        print(base.localY)
        print(base.calculateResidualRangeAndBearing(pose))

    def testBasePosition3(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        bd = BaseDetector(None)
        base = bd.calculateBase(base1, 6.941843032836914, 6.944105625152588, 6.692421913146973)
        pose = Pose(-4.84, -0.30, radians(-3.528))
        print(base.getAbsolutePosition(pose))
        print(base.localX)
        print(base.localY)
        print(base.calculateResidualRangeAndBearing(pose))

    def testBasePosition4(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        bd = BaseDetector(None)
        base = bd.calculateBase(base2, 4.494799613952637, 4.484289169311523, 4.737865924835205)
        pose = Pose(4.20, -0.06, radians(1.52))
        print(base.getAbsolutePosition(pose))
        print(base.localX)
        print(base.localY)
        print(base.calculateResidualRangeAndBearing(pose))
