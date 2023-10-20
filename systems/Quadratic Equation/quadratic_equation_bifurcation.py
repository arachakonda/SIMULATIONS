# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 16:45:54 2021

@author: Ananth

"""

import numpy as np
import matplotlib.pyplot as plt

x0 = 0.1
a_start = -3
a_stop = 0
a_interval = 0.001
max_period = 100
dis_iter_num = 10000


def quadratic_map(x0, a):
    return x0**2+x0+a

def quadratic_ss_val(a, dis_iter_num, max_period):
    x = x0
    for i in range(dis_iter_num):
        x = quadratic_map(x,a)
    y_l = np.zeros(max_period)
    for i in range(max_period):
        x = quadratic_map(x,a)
        y_l[i] = x
    return np.unique(y_l)


def quadratic_populate_ss(a_domain, max_period):
    y = np.zeros((int((a_stop-a_start)/a_interval), max_period))
    for a_index, a in enumerate(a_domain):
        y_l = quadratic_ss_val(a, dis_iter_num, max_period)
        for i in range(np.size(y_l)):
            y[a_index][i] = y_l[i]
    return y
    
a_domain = np.arange(a_start,a_stop,a_interval)
y = quadratic_populate_ss(a_domain, max_period)

print(y)

for x_e,y_e in zip(a_domain,y):
    plt.scatter([x_e]*len(y_e), y_e, s = 0.1,color = 'b')

#plt.xticks([0.5,1,1.5,2,2.5,3,3.5,4])  

plt.show()


        

    
        
    
    