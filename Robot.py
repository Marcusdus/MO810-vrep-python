
from Simulator import Simulator

NUM_SONARS = 16
WHEELS_DIST = 0.381
WHEELS_RAD =  0.0975

class Robot:
    def __init__(self, simulator: Simulator, name: str):
        self.name = name
        self.sim = simulator    
        
        self.velocity = [1] * 2
        self.encoder = [0] * 2
        self.lastEncoder = [0] * 2
        self.sonarReading = [None] * NUM_SONARS

        # Position
        self.position = [0] * 3
        self.lastPosition = [0] * 3
        self.orientation = [0] * 3

        # Handles
        self.handle = self.sim.getHandle(self.name)
        self.encoderHandle = [None] * 2
        self.motorHandle = [None] * 2
        self.sonarHandle = [None] * NUM_SONARS

        # Encoder handle
        self.encoderHandle[0] = self.sim.getHandle("Pioneer_p3dx_leftWheel");
        self.encoderHandle[1] = self.sim.getHandle("Pioneer_p3dx_rightWheel");

        # Motor handle
        self.motorHandle[0] = self.sim.getHandle("Pioneer_p3dx_leftMotor");
        self.motorHandle[1] = self.sim.getHandle("Pioneer_p3dx_rightMotor");

        # Connect to sonar sensors. Requires a handle per sensor. 
        # Sensor name: Pioneer_p3dx_ultrasonicSensorX, where
        # is the sensor number, from 1 - 16
        for i in range(0,NUM_SONARS):
            sensorName = "Pioneer_p3dx_ultrasonicSensor{}".format(i+1)
            self.sonarHandle[i] = self.sim.getHandle(sensorName)
        
        self.initPose = self.sim.getObjectPosition(self.handle)
        self.update()

    def updateSensors(self):
        for i in range(0,NUM_SONARS):
            state = None
            coord = [None] * 3

            state, coord, handle, surface = self.sim.readProximitySensor(self.sonarHandle[i])
            if state > 0:
                self.sonarReading[i] = coord[2]
            else:
                self.sonarReading[i] = -1
        
        self.lastEncoder[0] = self.encoder[0]
        self.lastEncoder[1] = self.encoder[1]

        #TODO: should we really use motorHandle? Shouldn't it be encoderHandle?
        self.encoder[0] = self.sim.getJointPosition(self.motorHandle[0])
        self.encoder[1] = self.sim.getJointPosition(self.motorHandle[1])

    def updatePose(self):
        self.lastPosition = self.position[:]
        
        self.position = self.sim.getObjectPosition(self.handle)
        self.orientation = self.sim.getObjectOrientation(self.handle)

    def update(self):
        self.updateSensors()
        self.updatePose()
    
    def driveAndupdate(self):
        self.drive(10,5)
        self.update()

    def move(self, vLeft, vRight):
        self.sim.setJointTargetVelocity(self.motorHandle[0], vLeft)
        self.sim.setJointTargetVelocity(self.motorHandle[1], vRight)

    def stop(self):
        self.move(0,0)

    def __vRToDrive(self, vLinear, vAngular):
        return (((2*vLinear)+(WHEELS_DIST*vAngular))/2*WHEELS_RAD);
    
    def __vLToDrive(self, vLinear, vAngular):
        return (((2*vLinear)-(WHEELS_DIST*vAngular))/2*WHEELS_RAD);

    def drive(self, vLinear, vAngular):
        self.move(self.__vLToDrive(vLinear, vAngular), self.__vRToDrive(vLinear, vAngular))    
