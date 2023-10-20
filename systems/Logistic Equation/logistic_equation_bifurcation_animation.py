# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 01:43:18 2021

@author: anant
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

x0 = 0.1
a_start = 2.5
a_stop = 4.0
a_interval = 0.001
max_period = 100
dis_iter_num = 100000


def logistic_map(x0, a):
    return a*x0*(1-x0)

def logistic_ss_val(a, dis_iter_num, max_period):
    x = x0
    for i in range(dis_iter_num):
        x = logistic_map(x,a)
    y_l = np.zeros(max_period)
    for i in range(max_period):
        x = logistic_map(x,a)
        y_l[i] = x
    return np.unique(y_l)

#print(np.size(logistic_ss_val(3.6,1000,10000)))


def logistic_populate_ss(a_domain, max_period):
    y = np.zeros((int((a_stop-a_start)/a_interval), max_period))
    for a_index, a in enumerate(a_domain):
        y_l = logistic_ss_val(a, dis_iter_num, max_period)
        for i in range(np.size(y_l)):
            y[a_index][i] = y_l[i]
    return y
    
a_domain = np.arange(a_start,a_stop,a_interval)
y = logistic_populate_ss(a_domain, max_period)

print(y)


fig = plt.figure(figsize=(15,15))
ax = fig.add_subplot(autoscale_on = False, xlim=(a_start,a_stop), ylim=(0,1))
ax.set_aspect(1)

lines = sum([ax.plot([], [], '.', ms=1, lw=0.1)
             for a in a_domain], [])  


def animate(i):
    linex = [a_domain[i]]*max_period
    liney = y[i]
    lines[i].set_data(linex, liney)

    return lines

#plt.xticks([0.5,1,1.5,2,2.5,3,3.5,4])  
ani = animation.FuncAnimation(
    fig, animate, len(y), interval=a_interval*1000, blit=True)
ani.save('logistic_equation_bifurcation_animation%i.mp4'%5, fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()
