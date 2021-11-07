# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 22:28:20 2021

@author: Sean
"""


from parameters import (
    MAX_ACCELERATION,
    MAX_BREAKING,
    MAX_STEERING_CHANGE,
    MAX_VELOCITY
)


def simple_drive(ranges, vel, acc):
    
    new_acc = 0
    steering_change = 0
    
    left_range = ranges[1] #ranges[0] + ranges[1]
    front_range = ranges[2]
    right_range = ranges[3] #+ ranges[4]
    
    steering_change = (
        (left_range - right_range) /
        max(left_range, right_range) *
        MAX_STEERING_CHANGE
    )
        
    e_stop_range = 5
    caution_range = 8
    coast_range = 12
    if front_range < e_stop_range:
        new_acc = MAX_BREAKING
    elif front_range < caution_range:
        new_acc = (
            (caution_range - front_range) /
            (caution_range - e_stop_range)
        ) * MAX_BREAKING
    elif front_range < coast_range:
        new_acc = 0
    else:
        new_acc = MAX_ACCELERATION
        
    # Override steering if clear shot
    if front_range > 25:
        steering_change = 0
        
    if vel == 0:
        new_acc = MAX_ACCELERATION
        if left_range > right_range:
            steering_change = MAX_STEERING_CHANGE
        if right_range > left_range:
            steering_change = -1 * MAX_STEERING_CHANGE
    if vel >= MAX_VELOCITY / 1.25:
        if left_range > right_range:
            steering_change = MAX_STEERING_CHANGE
        if right_range > left_range:
            steering_change = -1 * MAX_STEERING_CHANGE
        
    return new_acc, steering_change
