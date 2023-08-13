# -*- coding: utf-8 -*-
"""
Created on Sat May 29 18:30:40 2021

@author: Ananth Rachakonda
"""

from numpy import sin, cos
from collections import deque
import scipy.integrate as integrate
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



M = 0.3
m = 0.2
b = 0.2
k = 0.0
g = 9.8
l = 2

t_stop = 60
history_len = 500

def derivative(state, t):
    
    dydx = np.zeros_like(state)
    theta = state[2]
    theta_dot = state[3]
    x = state[0]
    x_dot = state[1]
    
    dydx[0] = x_dot
    dydx[2] = theta_dot
    
    #evaluating theta double dot and x double dot to assign to derivate return variable
    #assigning x double dot and theta double dot to the derivate return variable
    x_ddot = (4/((4+3*m*cos(theta)**2)*(m+M)))*(m*l*sin(theta)*theta_dot**2 - 
              b*x_dot-k*x- ((3/4)*m*g*sin(theta)*cos(theta)))
    theta_ddot = -((3/(2*l))*(x_ddot*cos(theta)+g*sin(theta)))

    dydx[1]=x_ddot
    dydx[3]=theta_ddot
    
    return dydx

dt = 0.01
t = np.arange(0, t_stop, dt)


x = 0.0
x_dot = 0.0
phi = 120.0
phi_dot = 0.0


state = np.array([x,x_dot, np.radians(phi), np.radians(phi_dot)])

y = integrate.odeint(derivative, state, t)
#the plot of the cart
x1 = y[:, 0]
y1 = np.zeros_like(y[:,0])
#the plot of the pendulum
x2 = l*sin(y[:, 2])+x1
y2 = -l*cos(y[:, 2])-y1

fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(autoscale_on = False, xlim=(-2*l,2*l), ylim=(-2*l,2*l))
ax.set_aspect(1)
ax.grid()

line, = ax.plot([],[],'o-',lw=2, color='blue')
cart, = ax.plot([],[],linestyle=None, marker='s', markersize = 20, color='red')
trace, = ax.plot([],[],',-',lw=1, color='orange')


time_template = 'time = %.1fs'
position_template = 'position = %.001fm'
ang_template = 'ang_velocity = %.001frad/s'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
position_text = ax.text(0.05, 0.85, '', transform = ax.transAxes)
ang_text = ax.text(0.05, 0.80, '', transform=ax.transAxes)
history_x, history_y = deque(maxlen=history_len), deque(maxlen=history_len)

def animate(i):
    linex = [x1[i], x2[i]]
    liney = [y1[i], y2[i]]
    cartx = [x1[i]]
    carty = [y1[i]]

    if i == 0:
        history_x.clear()
        history_y.clear()

    history_x.appendleft(linex[1])
    history_y.appendleft(liney[1])

    line.set_data(linex, liney)
    cart.set_data(cartx, carty)
    trace.set_data(history_x, history_y)
    time_text.set_text(time_template % (i*dt))
    position_text.set_text(position_template % cartx[0])
    ang_text.set_text(ang_template % (y[i,2]))
    
    return line, cart, trace, time_text, position_text, ang_text


ani = animation.FuncAnimation(
    fig, animate, len(y), interval=dt*1000, blit=True)
#ani.save('inverted_pendulum_on_cart_with_friction.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()










