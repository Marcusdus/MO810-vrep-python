import threading

from .PoseUpdater import GroundTruthPoseUpdater
from .Robot import Robot
from .RobotDummyDriver import RobotDummyDriver
from .RobotMonitor import RobotMonitor
from .Simulator import Simulator
from .plotrobot import plotRobotAndObjects


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
