# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 20:56:55 2021

@author: Sean
"""

import numpy as np

class Laser:
    
    def __init__(self, racetrack, range_resolution, max_range, theta_offset=0):
        
        self._racetrack = racetrack
        self._range_resolution = range_resolution
        self._max_range = max_range
        self._theta_offset = theta_offset
        
    def get_range_array(self, x, y, theta):
        
        theta -= self._theta_offset
        
        ranges = np.arange(
            0,
            self._max_range + self._range_resolution,
            self._range_resolution
        )
        
        x_rel = ranges * np.cos(theta)
        x_map = x + x_rel
        
        y_rel = ranges * np.sin(theta)
        y_map = y + y_rel
        
        return ranges, x_map, y_map
    
    def get_range(self, x, y, theta):
        
        ranges, x_map, y_map = self.get_range_array(x, y, theta)
        
        last_in_bounds = self._racetrack.get_last_in_bounds_index(
            x_map, 
            y_map
        )
        
        if last_in_bounds is None:
            detected_range = self._max_range
        else:
            detected_range = ranges[last_in_bounds]
            
        return detected_range
