# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 20:50:23 2021

@author: Sean
"""

import numpy as np
from laser import Laser
from parameters import (
    DEG_TO_RAD,
    LIDAR_MAX_RANGE,
    LIDAR_RANGE_RESOLUTION,
    MAX_ACCELERATION,
    MAX_BREAKING,
    MAX_STEERING_CHANGE,
    MAX_VELOCITY
)

class Car:
    
    lidar_offsets = np.array(
        [-90, -75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75, 90]
    ) * DEG_TO_RAD
    lidar_range_resolution = LIDAR_RANGE_RESOLUTION
    lidar_max_range = LIDAR_MAX_RANGE
    
    def __init__(
            self,
            racetrack,
            start_x,
            start_y,
            start_theta,
            start_acc=0
        ):
        
        self._racetrack = racetrack
        self._pos_x = start_x
        self._pos_y = start_y
        self._vel = 0
        self._acc = start_acc
        self._theta = start_theta * DEG_TO_RAD
        
        self.laps = 0
        self._track_theta = 0
        
        self.setup_lidar()
    
    def setup_lidar(self):
        
        self.lidar_system = {}
        for l_index in range(len(self.lidar_offsets)):
            self.lidar_system[f'l{l_index}'] = Laser(
                self._racetrack,
                range_resolution=self.lidar_range_resolution,
                max_range=self.lidar_max_range,
                theta_offset=self.lidar_offsets[l_index]
            )
            
    def plot_position(self, ax):
        ax.plot(self._pos_x, self._pos_y, 'bo')
            
    def update_state(self, acceleration, steering_change, dt):
                
        # Acceleration change check
        if acceleration > MAX_ACCELERATION:
            acceleration = MAX_ACCELERATION
        if acceleration < MAX_BREAKING:
            acceleration = MAX_BREAKING
            
        # Steering change check
        if steering_change > MAX_STEERING_CHANGE:
            steering_change = MAX_STEERING_CHANGE
        if steering_change < -1 * MAX_STEERING_CHANGE:
            steering_change  = -1 * MAX_STEERING_CHANGE
            
        self._theta += steering_change * DEG_TO_RAD
        
        new_vel = self._vel + acceleration * dt
        
        # Velocity check
        if new_vel > MAX_VELOCITY:
            self._vel = MAX_VELOCITY
            self._acc = 0
        elif new_vel < 0:
            self._vel = 0
            self._acc = 0
        else:
            self._vel = new_vel
            self._acc = acceleration
        
        diff_x = self._vel * dt * np.cos(self._theta)
        diff_y = self._vel * dt * np.sin(self._theta)
        
        # Check laps
        if self._pos_y < 0:
            if (self._pos_y + diff_y) > 0:
                self.laps += 1
        
        self._pos_x += diff_x
        self._pos_y += diff_y
        
    def check_in_bounds(self):
        
        current_x = np.array([self._pos_x])
        current_y = np.array([self._pos_y])
        
        in_bounds = self._racetrack.check_points_in_bounds(
            current_x,
            current_y
        )[0]
        
        return in_bounds
        
    def get_lidar_ranges(self):
        
        ranges = []
        for li, lidar in self.lidar_system.items():
            ranges.append(
                lidar.get_range(self._pos_x, self._pos_y, self._theta)
            )
        ranges = np.array(ranges)
        
        return ranges

    def get_lidar_ranges(self):
        
        for l_index, lidar in self.lidar_system.items():
            ranges, x_map, y_map = lidar.get_range_array(
                self._pos_x,
                self._pos_y,
                self._theta
            )
        
        last_in_bounds = self._racetrack.get_last_in_bounds_index(