import unittest
from math import pi
from math import radians
from andabb.utils import diffRadians


class UtilsTest(unittest.TestCase):
    paramsDiffRadians = [
        [pi, 0, pi],
        [pi, 0, -pi],
        [radians(60), 0, radians(60)],
        [radians(300), 0, radians(-60)],
        [radians(70), radians(-60), radians(10)],
        [radians(0), radians(-60), radians(-60)],
        [radians(0), radians(pi), radians(pi)],
    ]

    def testDiffRadians(self):
        i = 0
        for expected, start, end in self.paramsDiffRadians:
            i += 1
            with self.subTest(msg=i):
                self.assertAlmostEqual(expected, diffRadians(start, end), delta=0.000001)


if __name__ == '__main__':
    unittest.main()
