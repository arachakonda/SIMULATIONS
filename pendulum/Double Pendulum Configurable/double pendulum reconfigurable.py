# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 23:22:30 2021

@author: anant
"""

from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from collections import deque

G = 9.8  # acceleration due to gravity, in m/s^2
l1 = 2.0  # length of pendulum 1 in m
l2 = 2.0  # length of pendulum 2 in m
L = l1 + l2  # maximal length of the combined pendulum
m1 = 1.0  # mass of pendulum 1 in kg
m2 = 1.0  # mass of pendulum 2 in kg
t_stop = 20  # how many seconds to simulate
history_len = 50  # how many trajectory points to display

pend_number = 100000
factor = 0.0001

def derivs(state, t):

    dydx = np.zeros_like(state)
    dydx[0] = state[1]
    dydx[2] = state[3]
    
    t1 = state[0]
    t1_dot = state[1]
    t2 = state[2]
    t2_dot = state[3]
    
    A1 = 2*(m1*(l1**2)/3 + m2*l1**2)
    B1 = m2*l1*l2*cos(t1- t2)
    C1 = 0
    D1 = -(m2*l1*l2*sin(t1-t2)*(t1_dot - t2_dot))
    
    B2 = 2*(m2*(l2**2)/3)
    A2 = m2*l1*l2*cos(t1-t2)
    C2 = -(m2*l1*l2*sin(t1-t2)*(t1_dot - t2_dot))
    D2 = 0
    
    A = np.array([[A1, B1],[A2, B2]])
    DEF = np.array([[C1, D1],[C2, D2]])
    
    DEL1 = -(1/2)*t1_dot*t2_dot*(m2*l1*l2*sin(t1-t2)) - (sin(t1)*((m1*G*l1/2) + (m2*G*l1)))
    DEL2 = (1/2)*t1_dot*t2_dot*(m2*l1*l2*sin(t1-t2)) - (sin(t2)*m2*G*l2/2)
    
    DEL = np.array([[DEL1], [DEL2]])
    
        
    S_DOT = np.array([[t1_dot], [t2_dot]])
    
    B = 2*DEL - np.matmul(DEF, S_DOT)
    
    X = np.matmul(np.linalg.pinv(A),B)
    
    dydx[1] = X[0,0]
    dydx[3] = X[1,0]


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

state = np.zeros((pend_number,4))


for i in range(pend_number):
    state[i] =  np.radians([th1+factor*i, w1, th2+factor*i, w2])

# integrate your ODE using scipy.integrate.

y = np.zeros((pend_number,np.size(t),4))


for i in range(pend_number):
    y[i] = integrate.odeint(derivs, state[i], t)
    

x1= np.zeros((pend_number,np.size(t)))
y1= np.zeros((pend_number,np.size(t)))
x2= np.zeros((pend_number,np.size(t)))
y2= np.zeros((pend_number,np.size(t)))

for i in range(pend_number):
    x1[i] = l1*sin(y[i,:, 0])
    y1[i] = -l1*cos(y[i,:, 0])

    x2[i] = l2*sin(y[i,:, 2]) + x1[i]
    y2[i] = -l2*cos(y[i,:, 2]) + y1[i]


fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(autoscale_on=False, xlim=(-2*L, 2*L), ylim=(-2*L, 2*L))
ax.set_aspect('equal')
ax.grid()

"""lines = []
traces = []
for i in range(pend_number):
    l, = ax.plot([], [], 'o-', lw=2)
    lines.append(l)

for i in range(pend_number):
    t, = ax.plot([], [], ',-', lw=1)
    traces.append(t)  """
colors = plt.cm.prism(np.linspace(0, 1, pend_number))
lines = sum([ax.plot([], [], 'o-', lw=2)
             for c in colors], [])    
traces = sum([ax.plot([], [], ',-', lw=1)
             for c in colors], [])      

time_template = 'number = %i' % pend_number
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

historys_x = []
historys_y = []

for i in range(pend_number):
    historys_x.append(deque(maxlen=history_len))
    historys_y.append(deque(maxlen=history_len))
    

thisx = np.zeros((pend_number,3))
thisy = np.zeros((pend_number,3))

def animate(i):
    

    for j in range(pend_number):
        thisx[j] = [0, x1[j][i],x2[j][i]]
        thisy[j] = [0, y1[j][i],y2[j][i]]
    
    if i == 0:
        for history_x in historys_x:
            history_x.clear()
        for history_y in historys_y:
            history_y.clear()    
            
            
    for j in range(pend_number):        
        historys_x[j].appendleft(thisx[j][2])
        historys_y[j].appendleft(thisy[j][2])

    for line_number,line in enumerate(lines):
        line.set_data(thisx[line_number], thisy[line_number])
        
    for trace_number,trace in enumerate(traces):    
        trace.set_data(historys_x[trace_number], historys_y[trace_number])

    
    time_text.set_text(time_template)
    
    return lines+traces


ani = animation.FuncAnimation(
    fig, animate, len(y[0]), interval=dt*1000, blit=True)
ani.save('double_pendulum_%i.mp4'%pend_number, fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()