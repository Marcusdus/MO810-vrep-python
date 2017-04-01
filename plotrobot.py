import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from Robot import Robot

def update_line(num, robot:Robot, hl):
    robot.update()
    pos = robot.position[0:2]
    #print(hl.get_xdata())
    #print(hl.get_ydata())
    hl.set_xdata(np.append(hl.get_xdata(), pos[0]))
    hl.set_ydata(np.append(hl.get_ydata(), pos[1]))
    return hl,

def plotRobot(robot: Robot, intervalMs=500):
    fig1 = plt.figure()

    l, = plt.plot([], [], 'ro', markersize=1)
    plt.xlim(-20, 20)
    plt.ylim(-20, 20)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('test')
    line_ani = animation.FuncAnimation(fig1, update_line, None, fargs=(robot, l),
                                    interval=intervalMs, blit=True, repeat=False)

    # To save the animation, use the command: line_ani.save('lines.mp4')
    plt.show()


if __name__ == '__main__':
    from Simulator import Simulator
    
    sim = Simulator()
    sim.connect()

    robot = Robot(sim, "Pioneer_p3dx")
    plotRobot(robot)
    sim.disconnect()