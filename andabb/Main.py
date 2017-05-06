from andabb.Simulator import Simulator
from andabb.Robot import Robot
from andabb.RobotMonitor import RobotMonitor
from time import sleep
from andabb.plotrobot import plotRobotAndObjects
import threading
from andabb.ObjectDetectionListener import PrinterObjectDetectionListener
from andabb.PositionListener import PrinterPositionListerner
from andabb.RobotDummyDriver import RobotDummyDriver
from .PoseUpdater import GroundTruthPoseUpdater

def main():
    sim = Simulator()
    sim.connect()

    stopEvent = threading.Event()

    poseUpdater = GroundTruthPoseUpdater()

    robot = Robot(sim, "Pioneer_p3dx", poseUpdater)
    monitor = RobotMonitor(robot, stopEvent)

    driver = RobotDummyDriver(robot, stopEvent)

    monitor.subscribeToFrontObjectDetection(driver)

    driver.start()
    monitor.start()

    plotThread = threading.Thread(target=plotRobotAndObjects, args=(monitor,))
    plotThread.start()

    try:
        while monitor.is_alive():
            monitor.join(timeout=1.0)
            driver.join(timeout=1.0)
    except (KeyboardInterrupt, SystemExit):
        stopEvent.set()
    
    plotThread.join()
    sim.disconnect()

if __name__ == '__main__':
    main()
