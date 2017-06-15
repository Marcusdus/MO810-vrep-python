import unittest
from math import pi
from math import radians

from andabb.AngleUniverse import addDelta
from andabb.AngleUniverse import calculateDelta
from andabb.AngleUniverse import calculateFirstAngleFromTriangle


class AngleUniverTest(unittest.TestCase):
    paramsDiffRadians = [
        [180, 0, 180],
        [180, 0, -180],
        [0, -60, -60],
        [0, 180, 180],
        [20, 10, 30],
        [250, 10, -100],
        [70, -60, 10],
        [35, -10, 25]
    ]

    def testDiffRadians(self):
        for expected, start, end in self.paramsDiffRadians:
            with self.subTest(msg='{} = {}, {} (left orientation)'.format(expected, end, start)):
                expected = radians(expected)
                expectedRight = (2 * pi) - expected if expected != 0 else 0
                self.assertAlmostEqual(expected, calculateDelta(radians(start), radians(end), False),
                                       delta=0.000001)
                self.assertAlmostEqual(expectedRight, calculateDelta(radians(start), radians(end), True),
                                       delta=0.000001)

    paramsSumRadians = [
        [180, 0, 180],
        [180, 0, -180],
        [170, -170, -20],
        [-150, -170, 20]
    ]

    def testSumRadians(self):
        i = 0
        for expected, start, delta in self.paramsSumRadians:
            i += 1
            with self.subTest('final position {} = {} + delta({})'.format(expected, start, delta)):
                self.assertAlmostEqual(radians(expected), addDelta(radians(start), radians(delta)),
                                       delta=0.000001)

    def testAngleFromTriangle(self):
        self.assertAlmostEqual(radians(75.5), calculateFirstAngleFromTriangle(8, 6, 7), delta=0.001)


if __name__ == '__main__':
    unittest.main()
