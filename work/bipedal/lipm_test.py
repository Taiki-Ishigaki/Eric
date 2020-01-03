#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

import sys
sys.path.append('../../scripts/')
from bipedal_robot.lipm import LinearInvertedPendulum

def video(x_hs, u_hs, h, t, fig):
    ax = fig.add_subplot(221, aspect='equal', autoscale_on=False, xlim=(-2, 2), ylim=(-0.5, 3.5))
    ax.grid()

    #line
    line, = ax.plot([], [], '-r', lw=2)
    time_text = ax.text(0.02, 0.95, 'time = 0.0', transform=ax.transAxes)

    # cog circle
    circle, = ax.plot([], [], '-r', lw=2)
    radius = 0.1
    angles = np.arange(0.0, np.pi * 2.0, np.radians(3.0))
    ox = radius * np.cos(angles) 
    oy = radius * np.sin(angles)

    rectangle = ax.add_patch(patches.Rectangle(xy=(u_hs[0]-0.25/2, -0.25/2), width=0.25, height=0.25,  ec='r', fill=False, lw=2))

    def init():
        line.set_data([], [])
        circle.set_data([], [])
        rectangle.set_xy([u_hs[0]-0.25/2, -0.25/2])
        time_text.set_text('')
        return line, time_text

    def animate(i):
        line.set_data([u_hs[i], x_hs[i]],[0, h])
        circle.set_data([ox + x_hs[i]],[ oy + h])
        rectangle.set_xy([u_hs[i]-0.25/2, -0.25/2])
        time_text.set_text('time = {0:.2f}'.format(i*t))
        return line, time_text

    ani = animation.FuncAnimation(fig, animate, frames=range(len(x_hs)),
                                  interval=t*1000, blit=False, init_func=init)
    plt.show()
    #ani.save("output.gif", writer="imagemagick")

if __name__ == '__main__':
    x_ref = np.array([[0.5],[0.]])
    u_ref = np.array([[0.5]])
    x_start = 0.0
    dt = 0.01
    period = 4
    height = 1.5
    time_step = (int) (period / dt)
    plant = LinearInvertedPendulum(height)
    plant.init_state(x_start, x_ref, u_ref, dt)
    X_history = np.array(plant.get_X())
    u_history = np.array(plant.get_u())
    for i in range(time_step-1):
        plant.do_action(x_ref, u_ref)
        u_history = np.append(u_history, plant.get_u(), axis=1)
        X_history = np.append(X_history, plant.get_X(), axis=1)

    t = np.linspace(0, time_step*dt, time_step)

    fig = plt.figure()

    plt.subplot(212)
    plt.plot(t, X_history[0], label="COG position")
    plt.plot(t, X_history[1], label="COG velosity")
    plt.plot(t, u_history[0], label="ZMP position")
    plt.legend()
    
    video(X_history[0], u_history[0], plant.height, dt, fig)