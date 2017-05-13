import unittest

from andabb.WallFollower import FuzzyWallFollower


class FuzzyAvoidObstacleTest(unittest.TestCase):
    def testTurnRight(self):
        r = [0.002110123634338379, 0.6072200536727905, 2.0]
        r = [0.010628759860992432, 0.6329633593559265, 2.0]
        r = [1.0341405868530273e-05, 0.07219693809747696, 0.7946561574935913, 2.0]
        r = [7.748603820800781e-07, 0.5471609830856323, 0.3700582981109619, 0.4377201199531555]
        r = [0.20466271042823792, 0.5021722316741943, 2.0, 2.0]
        r = [0.0, 2.0, 2.0, 0.09563261270523071]
        r = [-7.569789886474609e-06, 0.5897635817527771, 0.2924635410308838, 0.31005585193634033]


        ctr: FuzzyWallFollower = FuzzyWallFollower()

        print(ctr.computeDelta(r[0], r[1], r[2], r[3]))

        ctr.leftFrontSensor.view(sim=ctr.sys)
        ctr.rightFrontSensor.view(sim=ctr.sys)
        ctr.sideSensor.view(sim=ctr.sys)
        ctr.deltaSide.view(sim=ctr.sys)

        ctr.angularCsq.view(sim=ctr.sys)
        ctr.linearCsq.view(sim=ctr.sys)

        print("End")


if __name__ == '__main__':
    unittest.main()
