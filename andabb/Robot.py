from math import degrees

from .Simulator import Simulator
from .Wheel import Wheel

NUM_SONARS = 16
WHEELS_DIST = 0.381
WHEELS_RAD = 0.0975


class Robot:
    def __init__(self, simulator: Simulator, name: str, lWheel: Wheel, rWheel: Wheel):
        self.name = name
        self.sim = simulator

        self.sonarReading = [None] * NUM_SONARS

        # Position
        self.pose = Pose()

        # Ground-Truth pose
        self.gtPose = Pose()

        self.lWheel = lWheel
        self.rWheel = rWheel

        # Handles
        self.handle = self.sim.getHandle(self.name)
        self.sonarHandle = [None] * NUM_SONARS

        # Connect to sonar sensors. Requires a handle per sensor. 
        # Sensor name: Pioneer_p3dx_ultrasonicSensorX, where
        # is the sensor number, from 1 - 16
        for i in range(0, NUM_SONARS):
            sensorName = "Pioneer_p3dx_ultrasonicSensor{}".format(i + 1)
            self.sonarHandle[i] = self.sim.getHandle(sensorName)

        self.initPose = self.sim.getObjectPosition(self.handle)

    def updateSensors(self):
        for i in range(0, NUM_SONARS):
            state, coord, handle, surface = self.sim.readProximitySensor(self.sonarHandle[i])
            if state > 0:
                self.sonarReading[i] = coord[2]
            else:
                self.sonarReading[i] = -1

    def stop(self):
        self.lWheel.stop()
        self.rWheel.stop()

    def __vRToDrive(self, vLinear, vAngular):
        return ((2 * vLinear) + (WHEELS_DIST * vAngular)) / (2 * WHEELS_RAD);

    def __vLToDrive(self, vLinear, vAngular):
        return ((2 * vLinear) - (WHEELS_DIST * vAngular)) / (2 * WHEELS_RAD);

    def drive(self, vLinear, vAngular):
        self.lWheel.setSpeed(self.__vLToDrive(vLinear, vAngular))
        self.rWheel.setSpeed(self.__vRToDrive(vLinear, vAngular))


class Pose:
    def __init__(self, x=0, y=0, orientation=0):
        self.x = x
        self.y = y
        self.orientation = orientation

    def isZero(self):
        if self.x == 0 and self.y == 0 and self.orientation == 0:
            return True
        return False

    def __str__(self):
        return "[{:.2f}, {:.2f}, {:.3f} degrees]".format(self.x, self.y, degrees(self.orientation))


def newPioonerRobot(sim: Simulator):
    lWheel = Wheel(sim, "Pioneer_p3dx_leftMotor")
    rWheel = Wheel(sim, "Pioneer_p3dx_rightMotor")
    return Robot(sim, "Pioneer_p3dx", lWheel, rWheel)
