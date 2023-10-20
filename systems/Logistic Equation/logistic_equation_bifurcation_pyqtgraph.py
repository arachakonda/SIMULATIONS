# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 21:10:44 2021

@author: anant
"""
import sys
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

x0 = 0.1
a_stop = 4
a_interval = 0.001
max_period = 100
dis_iter_num = 1000

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

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

app = pg.mkQApp()

# Create the view
view = pg.PlotWidget()
view.resize(800, 600)
view.setWindowTitle('Scatter plot using pyqtgraph with PyQT5')
view.setAspectLocked(True)
view.show()



scatter = pg.ScatterPlotItem(pen=pg.mkPen(width=1, color='r'), symbol='o', size=1)
view.addItem(scatter)
pos_dict=[]

for a_index,a in enumerate(a_domain):
    for i in range(max_period):
        pos_dict = pos_dict+[{'pos':[a,y[a_index,i]]}]

print(pos_dict)
  
scatter.setData(pos_dict)
    
sys.exit(app.exec_())








