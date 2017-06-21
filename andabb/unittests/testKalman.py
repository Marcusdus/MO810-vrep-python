import logging
import unittest

from andabb.BaseDetectionListener import BaseDetector
from andabb.Robot import Pose


class KalmanTest(unittest.TestCase):
    def testBasePosition(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        bd = BaseDetector(None)
        base = bd.calculateBase(1.04, 1.04, 0.75)
        pose = Pose(-1.02, 0.37, -0.28)
        print(base.getAbsolutePosition(pose))
        print(base.localX)
        print(base.localY)
        print(base.calculateResidualRangeAndBearing(pose))

    def testBasePosition2(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        bd = BaseDetector(None)
        base = bd.calculateBase(4.00, 4.01, 4.26)
        pose = Pose(4.57, -0.05, 0.07)
        print(base.getAbsolutePosition(pose))
        print(base.localX)
        print(base.localY)
        print(base.calculateResidualRangeAndBearing(pose))

    def testBasePosition3(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        bd = BaseDetector(None)
        base = bd.calculateBase(0.69, 0.51, 0.71)
        # pose = Pose(3.66, 1.89, -1.20)
        # print(base.getAbsolutePosition(pose))
        print(base.localX)
        print(base.localY)
        # print(base.calculateResidualRangeAndBearing(pose))
