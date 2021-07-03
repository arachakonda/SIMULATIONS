# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 15:23:30 2021

@author: anant
"""

from numpy import sin, cos
from collections import deque
import scipy.integrate as integrate
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

M = 10
m1 = 1
m2 = 1
l1 = 2.0
l2 = 2.0
k = 0.0
g= 9.8
b= 0.2

t_stop = 200

history_len = 500



def derivative(state,t):
    
    # the state vector has [x,x',theta_1,theta_1',theta_2, theta_2']
    
    dydx = np.zeros_like(state)
    x= state[0]
    x_dot = state[1]
    t1 = state[2]
    t1_dot = state[3]
    t2 = state[4]
    t2_dot = state[5]
    
    
    A1 = 2*(M+m1+m2)
    B1 = l1*cos(t1)*(m1 + 2*m2)
    C1 = m2*l2*cos(t2)
    D1 = 0
    E1 = -((m1 + 2*m2)*l1*sin(t1)*t1_dot)
    F1 = -(m2*l2*sin(t2)*t2_dot)
    
    
    A2 = (m1+2*m2)*l1*cos(t1)
    B2 = 2*(((m1*l1**2)/3) + (m2*l1**2))
    C2 = (m2*l1*l2*cos(t1-t2))
    D2 = -t1_dot*l1*sin(t1)*(m1 + 2*m2 )
    E2 = -t2_dot*m2*l1*l2*sin(t1-t2)
    F2 = m2*l1*l2*sin(t1-t2)*t2_dot
    
    
    
    A3 = m2*l2*cos(t2)
    B3 = m2*l1*l2*cos(t1-t2)
    C3 = 2*(m2*(l2**2))/3
    D3 = -m2*l2*sin(t2)*t2_dot
    E3 = -t1_dot*m2*l1*l2*sin(t1-t2)
    F3 = t1_dot*m2*l1*l2*sin(t1-t2)
    
    A = np.array([[A1, B1, C1], [A2, B2, C2], [A3, B3, C3]])
    DEF = np.array([[D1, E1, F1], [D2, E2, F2], [D3, E3, F3]])
    DEL1 = -k*x-b*x_dot
    DEL2 = -(1/2)*( (t1_dot*t2_dot)*(m2*l1*l2*sin(t1-t2)) + (x_dot*t1_dot)*(m1*l1+2*m2*l1)*sin(t1)  
    + sin(t1)*g*l1*(m1 + 2*m2) )
    DEL3 = (1/2)*( (t1_dot*t2_dot)*(m2*l1*l2*sin(t1-t2)) - (x_dot*t2_dot)*(m2*l2*sin(t2))  - sin(t2)*m2*g*l2 ) 
    
    DEL = np.array([[DEL1],[DEL2],[DEL3]])
    
    S_DOT = np.array([[x_dot], [t1_dot], [t2_dot]])
    
    B = 2*DEL - np.matmul(DEF, S_DOT)
    
    X = np.matmul(np.linalg.pinv(A),B)
    
    x_ddot = X[0,0]
    t1_ddot = X[1,0]
    t2_ddot = X[2,0]
    
    dydx[0] = x_dot
    dydx[1] = x_ddot
    dydx[2] = t1_dot
    dydx[3] = t1_ddot
    dydx[4] = t2_dot
    dydx[5] = t2_ddot
    
    return dydx

dt = 0.01
t = np.arange(0, t_stop, dt)


x = 0.0
x_dot = 0.0
theta1 = 120.0
theta1_dot = 0.0
theta2 = -10.0
theta2_dot = 0.0


state = np.array([x,x_dot, np.radians(theta1), np.radians(theta1_dot), np.radians(theta2), np.radians(theta2_dot)])


y = integrate.odeint(derivative, state, t)
#the plot of the cart
x1 = y[:, 0]
y1 = np.zeros_like(y[:,0])
#the plot of the first pendulum
x2 = l1*sin(y[:, 2])+x1
y2 = -l1*cos(y[:, 2])+y1

#the plot of the second pendulum
x3 = l2*sin(y[:, 4])+x2
y3 = (-l2*cos(y[:, 4])+y2)


fig = plt.figure(figsize=(15,7))
ax = fig.add_subplot(autoscale_on = False, xlim=(-5*(l1+l2),5*(l1+l2)), ylim=(-2*(l1+l2),2*(l1+l2)))
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
    linex = [x1[i], x2[i],x3[i]]
    liney = [y1[i], y2[i],y3[i]]
    cartx = [x1[i]]
    carty = [y1[i]]

    if i == 0:
        history_x.clear()
        history_y.clear()

    history_x.appendleft(linex[2])
    history_y.appendleft(liney[2])

    line.set_data(linex, liney)
    cart.set_data(cartx, carty)
    trace.set_data(history_x, history_y)
    time_text.set_text(time_template % (i*dt))
    position_text.set_text(position_template % cartx[0])
    ang_text.set_text(ang_template % (y[i,2]))
    
    return line, cart, trace, time_text, position_text, ang_text


ani = animation.FuncAnimation(
    fig, animate, len(y), interval=dt*1000, blit=True)
"""if(b == 0.0):
    ani.save('frictionless_double_pendulum_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
else:
    ani.save('frictionful_double_pendulum_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])"""
plt.show()