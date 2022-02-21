# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 20:49:39 2021

@author: Sean
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

from parameters import (
    DEFAULT_TRACK_MIN,
    DEFAULT_TRACK_MAX,
    DEFAULT_TRACK_WIDTH,
    N_CURVES,
    N_SAMPLES,
    STARTING_THETA,
    TRACK_SEED
)

class RaceTrack:
    
    def __init__(
            self,
            track_r_min=DEFAULT_TRACK_MIN,
            track_r_max=DEFAULT_TRACK_MAX,
            track_width=DEFAULT_TRACK_WIDTH,
            map_index=TRACK_SEED,
            ax=None
        ):
        
        # Set track seed
        np.random.seed(map_index)
        
        self.track_r_min = track_r_min
        self.track_r_max = track_r_max
        self.track_width = track_width
        
        self.ax = ax
        
        self.generate_track_grid()
        
    def generate_track_grid(self, n_curves=N_CURVES, n_samples=N_SAMPLES):
        
        theta_initial = np.linspace(0, 2 * np.pi, num=N_CURVES)
        r_initial = (
            np.random.rand(N_CURVES) *
            (self.track_r_max - self.track_r_min) +
            self.track_r_min
        )
        r_initial[-1] = r_initial[0]
        
        theta = np.linspace(0, 2 * np.pi, num=n_samples)
        range_func = interp1d(theta_initial, r_initial, kind="cubic")
        r_in = range_func(theta)
        r_out = r_in + self.track_width
        
        x_in = r_in * np.cos(theta)
        x_out = r_out * np.cos(theta)
        
        y_in = r_in * np.sin(theta)
        y_out = r_out * np.sin(theta)
        
        r_sp = range_func(STARTING_THETA) + self.track_width / 2
        
        self.starting_point_x = r_sp * np.cos(STARTING_THETA)
        self.starting_point_y = r_sp * np.sin(STARTING_THETA)
        self.range_func = range_func
        
        self.x_in = x_in
        self.x_out = x_out
        self.y_in = y_in
        self.y_out = y_out
        
    def plot_track(self, ax):
        ax.plot(self.x_in, self.y_in, 'k-', label='min')
        ax.plot(self.x_out, self.y_out, 'k-', label='max')
        
    def get_min_range(self, theta):
        return self.range_func(theta)
        
    def get_max_range(self, theta):
        return self.range_func(theta) + self.track_width
    
    def get_theta(self, x, y):
        return np.arctan(y / x)
    
    def check_points_in_bounds(self, x, y):
        
        r_actual = np.sqrt(x ** 2 + y ** 2)
        neg_x = x < 0
        neg_y = y < 0
        theta = np.arctan(y / x)
        # Correct theta
        theta[neg_x & neg_y] += np.pi
        theta[neg_x & ~neg_y] += np.pi
        theta[~neg_x & neg_y] += 2 * np.pi
        
        r_min = self.get_min_range(theta)
        r_max = self.get_max_range(theta)
        
        min_check = r_actual >= r_min
        max_check = r_actual <= r_max
        in_bounds = min_check & max_check
        
        return in_bounds
    
    def get_last_in_bounds_index(self, x, y):
        
        last_index = None
        in_bounds = self.check_points_in_bounds(x, y)
        index_in_bounds = np.where(in_bounds == True)[0]
        index_out_of_bounds = np.where(in_bounds == False)[0]
        
        if len(index_out_of_bounds) > 0:
            last_index = index_out_of_bounds[0] - 1
        elif len(index_in_bounds) > 0:
            last_index = index_in_bounds[-1]
            
        if self.ax:
            if last_index:
                self.ax.plot(x[last_index], y[last_index], 'g.')
                self.ax.plot(x[:last_index+1], y[:last_index+1], 'g-', linewidth=0.5)
            
        return last_index
