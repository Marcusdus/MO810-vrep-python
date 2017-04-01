import unittest
from Simulator import Simulator

LEFT_ENCODER = "Pioneer_p3dx_leftWheel"
RIGHT_ENCODER = "Pioneer_p3dx_rightWheel"
LEFT_MOTOR = "Pioneer_p3dx_leftMotor"
RIGHT_MOTOR = "Pioneer_p3dx_rightMotor"

class SimulatorTests(unittest.TestCase):
    def setUp(self):
        self.sim = Simulator()
        self.sim.connect()

    def tearDown(self):
        self.sim.disconnect()

    def testInvalidConnection(self):
        s = Simulator("xxx")
        with self.assertRaises(Exception):
            s.connect()
        self.assertFalse(s.isConnected)
    
    def testGetHandleWhenNotConnected(self):
        s = Simulator()
        with self.assertRaises(Exception):
            s.getHandle("")

    def testHandleNotFound(self):
        with self.assertRaises(NameError):
            self.sim.getHandle("not found")
    
    def testGetEncoder(self):
        leftEncoder = self.sim.getHandle(LEFT_ENCODER)
        rightEncoder = self.sim.getHandle(RIGHT_ENCODER)

        leftMotor = self.sim.getHandle(LEFT_MOTOR)
        rightMotor = self.sim.getHandle(RIGHT_MOTOR)

        self.assertIsNotNone(leftEncoder)
        self.assertIsNotNone(rightEncoder)
        self.assertIsNotNone(leftMotor)
        self.assertIsNotNone(rightMotor)

    def testGetPosition(self):
        handle = self.sim.getHandle("Pioneer_p3dx")
        pos = self.sim.getObjectPosition(handle)
        print("Pos {}".format(pos))

if __name__ == '__main__':
    unittest.main()