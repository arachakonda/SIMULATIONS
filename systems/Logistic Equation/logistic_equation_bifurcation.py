# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 16:45:54 2021

@author: Ananth

"""

import numpy as np
import matplotlib.pyplot as plt

x0 = 0.1
a_stop = 4
a_interval = 0.0001
max_period = 100
dis_iter_num = 10000


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
    y = np.zeros((int(a_stop/a_interval), max_period))
    for a_index, a in enumerate(a_domain):
        y_l = logistic_ss_val(a, dis_iter_num, max_period)
        for i in range(np.size(y_l)):
            y[a_index][i] = y_l[i]
    return y
    
a_domain = np.arange(0,a_stop,a_interval)
y = logistic_populate_ss(a_domain, max_period)

print(y)

for x_e,y_e in zip(a_domain,y):
    plt.scatter([x_e]*len(y_e), y_e, s = 2)

plt.xticks([0.5,1,1.5,2,2.5,3,3.5,4])  

plt.show()


        

    
        
    
    