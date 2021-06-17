# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from collections import deque

'''G = 9.8  # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
L2 = 1.0  # length of pendulum 2 in m
L = L1 + L2  # maximal length of the combined pendulum
M1 = 1.0  # mass of pendulum 1 in kg
M2 = 1.0  # mass of pendulum 2 in kg
t_stop = 5  # how many seconds to simulate
history_len = 500  # how many trajectory points to display'''

#inverted pendulum on cart parameters
G = 9.8 # Acceleration due to gravity
L = 1.0 # length of inverted pendulum
M = 1 # mass of inverted pendulum
t_stop = 20 # number of seconds to simulate
history_len = 2000 # number of trajectory points to display



def derivs(state, t):

    '''dydx = np.zeros_like(state)
    dydx[0] = state[1]

    delta = state[2] - state[0]
    den1 = (M1+M2) * L1 - M2 * L1 * cos(delta) * cos(delta)
    dydx[1] = ((M2 * L1 * state[1] * state[1] * sin(delta) * cos(delta)
                + M2 * G * sin(state[2]) * cos(delta)
                + M2 * L2 * state[3] * state[3] * sin(delta)
                - (M1+M2) * G * sin(state[0]))
               / den1)

    dydx[2] = state[3]

    den2 = (L2/L1) * den1
    dydx[3] = ((- M2 * L2 * state[3] * state[3] * sin(delta) * cos(delta)
                + (M1+M2) * G * sin(state[0]) * cos(delta)
                - (M1+M2) * L1 * state[1] * state[1] * sin(delta)
                - (M1+M2) * G * sin(state[2]))
               / den2)'''
    
    #calculate dydx based on current state in this function
    dydx = np.zeros_like(state) #defining a vector like the state vector to return the rates of state variables
    
    dydx[0] = state[1]
    
    dydx[1] = (-G/L)*sin(state[0])
    

    return dydx

# create a time array from 0..t_stop sampled at 0.02 second steps
dt = 0.02
t = np.arange(0, t_stop, dt)

# th1 and th2 are the initial angles (degrees)
# w10 and w20 are the initial angular velocities (degrees per second)
th1 = 120.0
w1 = 0.0
th2 = -10.0
w2 = 0.0

# initial state
#state = np.radians([th1, w1, th2, w2])
state = np.radians([th1,w1])

# integrate your ODE using scipy.integrate.
y = integrate.odeint(derivs, state, t)


#x1 = L1*sin(y[:, 0])
#y1 = -L1*cos(y[:, 0])

x1 = L*sin(y[:,0])
y1 = -L*cos(y[:,0])

#print (x1)
#print (y1)

#x2 = L2*sin(y[:, 2]) + x1
#y2 = -L2*cos(y[:, 2]) + y1

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(autoscale_on=False, xlim=(-3*L, 3*L), ylim=(-3*L, 3*L))
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'o-', lw=2)
trace, = ax.plot([], [], ',-', lw=1)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
history_x, history_y = deque(maxlen=history_len), deque(maxlen=history_len)





def animate(i):
    thisx = [0, x1[i]]
    thisy = [0, y1[i]]

    if i == 0:
        history_x.clear()
        history_y.clear()

    history_x.appendleft(thisx[1])
    history_y.appendleft(thisy[1])

    line.set_data(thisx, thisy)
    trace.set_data(history_x, history_y)
    time_text.set_text(time_template % (i*dt))
    return line, trace, time_text


ani = animation.FuncAnimation(
    fig, animate, len(y), interval=dt*1000, blit=True)
ani.save('single_pendulum.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()