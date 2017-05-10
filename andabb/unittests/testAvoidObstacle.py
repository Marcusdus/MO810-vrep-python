import unittest

from andabb.AvoidObstacle import FuzzyAvoidObstacle

class FuzzyAvoidObstacleTest(unittest.TestCase):
    def testTurnRight(self):
        #reading = [2.0, 2.0, 0.8262460827827454, 0.7765557765960693, 0.7817856073379517, 0.8111905455589294, 2.0, 2.0]
        #reading = [2.0, 0.43701598048210144, 0.32800212502479553, 0.29767173528671265, 0.29861152172088623, 0.32163161039352417, 0.42007696628570557, 2.0]
        #reading = [2.0, 0.2909226417541504, 0.25831153988838196, 0.2611534595489502, 0.2805742621421814, 0.36760589480400085, 2.0,2.0]
        reading = [2.0, 0.29345953464508057, 0.26922813057899475, 0.2705088257789612, 0.29806870222091675, 0.398640513420105, 2.0,2.0]

        ctr:FuzzyAvoidObstacle = FuzzyAvoidObstacle()

        print(ctr.compute(reading))

        for r in ctr.sensors:
            r.view(sim=ctr.sys)

        ctr.angularCsq.view(sim=ctr.sys)
        ctr.linearCsq.view(sim=ctr.sys)

        print("End")


if __name__ == '__main__':
    unittest.main()
