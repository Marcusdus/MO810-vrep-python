import vrep

def connected(func):
    """
    Decorator to Simulator methods. 
    Use it when the precondition to the method is a valid connection. 
    """
    def function_wrapper(*args, **kwargs):
        if not args[0].isConnected:
            raise Exception("Not connected")
        return func(*args, **kwargs)
    return function_wrapper

class Simulator:
    def __init__(self, host='127.0.0.1', port=25000):
        self.id = -1
        self.host = host
        self.port = port
        self.isConnected = False

    def connect(self):
        self.id = vrep.simxStart(self.host,self.port,True,True,2000,5)
        if self.id == -1:
            self.isConnected = False
            raise Exception("Unable to connect to V-REP Server: {}:{}".format(self.host,self.port))
        else:
            self.isConnected = True
    
    def disconnect(self):
        if self.isConnected:
            vrep.simxFinish(self.id)
            self.isConnected = False

    @connected
    def pause(self):
        vrep.simxPauseCommunication(self.id,1)
    
    @connected
    def resume(self):
        vrep.simxPauseCommunication(self.id, 1)
    
    @connected
    def getHandle(self, name):
        ret, handle = vrep.simxGetObjectHandle(self.id, name, vrep.simx_opmode_oneshot_wait)
        if ret != vrep.simx_return_ok:
            raise NameError("Couldn't get handle for object named {}".format(name))
        return handle

    @connected
    def readProximitySensor(self, handle):
        """
        :return: detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector
        """
        retcode, *ret = vrep.simxReadProximitySensor(self.id, handle, vrep.simx_opmode_buffer)
        self.__assertSimxSuccessRet(retcode)
        return ret
        
    @connected
    def getObjectPosition(self, handle):
        retcode, ret = vrep.simxGetObjectPosition(self.id, handle, -1, vrep.simx_opmode_streaming)
        self.__assertSimxSuccessRet(retcode)
        return ret
    
    @connected
    def getObjectOrientation(self, handle):
        retcode, ret = vrep.simxGetObjectOrientation(self.id, handle, -1, vrep.simx_opmode_streaming)
        self.__assertSimxSuccessRet(retcode)
        return ret
    
    @connected
    def getJointPosition(self, handle):
        retcode, ret = vrep.simxGetJointPosition(self.id, handle, vrep.simx_opmode_streaming)
        self.__assertSimxSuccessRet(retcode)
        return ret

    @connected
    def setJointTargetVelocity(self, handle, velocity):
        retcode, ret = vrep.simxSetJointTargetVelocity(self.id, handle, velocity, vrep.simx_opmode_streaming)
        self.__assertSimxSuccessRet(retcode)
        return ret
    
    def __assertSimxSuccessRet(self, simxRet):
        if simxRet != vrep.simx_return_ok and simxRet != vrep.simx_return_novalue_flag:
            raise Exception("Error in Remote API return: {}".format(simxRet))