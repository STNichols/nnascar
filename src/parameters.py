# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 20:59:01 2021

@author: Sean
"""

import os
import numpy as np

# Constants
DEG_TO_RAD = np.pi / 180
HOME = os.environ.get("HOME")
NNASCAR_DATA = os.path.join(HOME, "data", "nnascar")

# Race Parameters
TICK_TIME = 0.1 # s
RACE_TIME = 60 # s

# Race Track Parameters
DEFAULT_TRACK_MIN = 20
DEFAULT_TRACK_MAX = 35 #60
DEFAULT_TRACK_WIDTH = 8 #15
N_CURVES = 20
N_SAMPLES = 1000
STARTING_THETA = 0 * DEG_TO_RAD
TRACK_SEED = 0

# Car Parameters
MAX_ACCELERATION = 3.0 # u/s^2
MAX_BREAKING = -8.0 # u/s^s
MAX_VELOCITY = 12 # u/s
MAX_STEERING_CHANGE = 5 # deg

# Laser Parameters
LIDAR_RANGE_RESOLUTION = 0.20
LIDAR_MAX_RANGE = 100
