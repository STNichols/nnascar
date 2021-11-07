# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 21:59:47 2021

@author: Sean
"""

import math
import matplotlib.pyplot as plt
import numpy as np

from scipy.interpolate import interp1d

np.random.seed(0)

r_min = 15
r_max = 20

r_width = 4

n_points = 20
n_samples = 100

theta_initial = np.linspace(-1*np.pi, np.pi, num=n_points)
r_initial = np.random.rand(n_points) * (r_max - r_min) + r_min
r_initial[-1] = r_initial[0]

theta = np.linspace(-1*np.pi, np.pi, num=n_samples)
r_smoother = interp1d(theta_initial, r_initial, kind="cubic")
r_in = r_smoother(theta)
r_out = r_in + r_width

x_in = r_in * np.cos(theta)
x_out = r_out * np.cos(theta)

y_in = r_in * np.sin(theta)
y_out = r_out * np.sin(theta)

sp_r = r_smoother(0) + r_width / 2
x_sp = sp_r * np.cos(0)
y_sp = sp_r * np.sin(0)

fig, ax = plt.subplots(figsize=(10,8))

ax.plot(x_in, y_in, '-')
ax.plot(x_out, y_out, '-')
ax.plot(x_sp, y_sp, 'o')
    
fig.show()
