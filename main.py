from Simulator import Simulator
from Robot import Robot
from RobotMonitor import RobotMonitor
from time import sleep
from plotrobot import plotRobot
import threading
from ObjectDetectionListener import PrinterObjectDetectionListener
from PositionListener import PrinterPositionListerner

def main():
    sim = Simulator()
    sim.connect()

    stopEvent = threading.Event()

    robot = Robot(sim, "Pioneer_p3dx")
    monitor = RobotMonitor(robot, stopEvent)

    robot.drive(10,0)
    objD = PrinterObjectDetectionListener()
    rbP = PrinterPositionListerner()

    monitor.subscribeChangePosition(rbP)
    monitor.subscribeToFrontObjectDetection(objD)

    monitor.start()
    plotThread = threading.Thread(target=plotRobot, args=(robot,))
    plotThread.start()

    try:
        while monitor.is_alive():
            monitor.join(timeout=1.0)
    except (KeyboardInterrupt, SystemExit):
        stopEvent.set()
    
    plotThread.join()
    sim.disconnect()

if __name__ == '__main__':
    main()