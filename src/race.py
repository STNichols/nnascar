# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 21:51:12 2021

@author: Sean
"""

import os
import glob
import matplotlib.pyplot as plt
import numpy as np

from parameters import (
    DEG_TO_RAD,
    DEFAULT_TRACK_MAX,
    DEFAULT_TRACK_MIN,
    DEFAULT_TRACK_WIDTH,
    NNASCAR_DATA,
    RACE_TIME,
    STARTING_THETA,
    TICK_TIME,
    MAX_ACCELERATION,
    MAX_BREAKING,
    MAX_VELOCITY
)
from race_track import RaceTrack
from car import Car
from utils import simple_drive

MAX_BOUNDS = DEFAULT_TRACK_MAX + DEFAULT_TRACK_WIDTH
FRAME_PATH = os.path.join(NNASCAR_DATA, "frames")

def race():
    
    os.makedirs(FRAME_PATH, exist_ok=True)
    for frame in glob.glob(FRAME_PATH + "/*png"):
        os.remove(frame)
    
    racetrack = RaceTrack()
    
    start_x = racetrack.starting_point_x
    start_y = racetrack.starting_point_y
    car = Car(
        racetrack,
        start_x,
        start_y,
        90,
        start_acc=1.5,
    )
    
    kin_fig, kin_ax = plt.subplots(nrows=2, ncols=1, figsize=(10,8))
    vel_ax = kin_ax[0]
    acc_ax = kin_ax[1]
    
    in_bounds = True
    current_time = 0
    frame_i = 0
    times = []
    vels = []
    accs = []
    while in_bounds and (car.laps < 1):
        current_time += TICK_TIME
        
        fig, ax = plt.subplots(figsize=(10,8))
        racetrack.ax = ax
        racetrack.plot_track(ax)
        
        racetrack.ax = ax
        car.plot_position(ax)
        in_bounds = car.check_in_bounds()
        ranges = car.get_lidar_ranges()
        
        a, s = simple_drive(ranges, car._vel, car._acc)
        
        car.update_state(a, s, TICK_TIME)
        times.append(current_time)
        vels.append(car._vel)
        accs.append(car._acc)
                
        ax.set_xlim([-MAX_BOUNDS, MAX_BOUNDS])
        ax.set_ylim([-MAX_BOUNDS, MAX_BOUNDS])
        
        # Lidar
        lidar_str = "Lidar Measurements:\n"
        positions = ["left", "front_left", "front", "front_right", "right"]
        for rng, position in zip(ranges, positions):
            rng = np.round(rng, decimals=1)
            lidar_str += f"{position}: {rng}\n"
        ax.text(0, 0, lidar_str)
        
        # Motion
        acc = car._acc
        vel = car._vel
        theta = car._theta / DEG_TO_RAD
        motion_str = "Kinematics:\n"
        for param, name in zip([acc, vel, theta], ["Acc", "Speed", "Angle"]):
            param = np.round(param, decimals=1)
            motion_str += f"{name}: {param}\n"
        ax.text(-DEFAULT_TRACK_MIN, 0, motion_str)
        
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        fig.suptitle(f"Time: {np.round(current_time, decimals=1)}")
        fig.tight_layout(pad=0.5)
        fig.savefig(os.path.join(FRAME_PATH, f'frame_{frame_i}.png'))
        plt.close()
        frame_i += 1
    
    print(f"Frames alive: {frame_i}, Time alive: {frame_i * TICK_TIME}")
    if car.laps == 1:
        print("Lap Complete!")
    
    # Plot kinematics
    vel_ax.plot(times, vels, '.-')
    vel_ax.plot([times[0], times[-1]], [MAX_VELOCITY, MAX_VELOCITY], 'r-')
    vel_ax.grid()
    vel_ax.set_ylabel("Velocity (u/s)")
    vel_ax.set_xlabel("Time (s)")
    
    acc_ax.plot(times, accs, '.-')
    acc_ax.plot([times[0], times[-1]], [MAX_ACCELERATION, MAX_ACCELERATION], 'r-')
    acc_ax.plot([times[0], times[-1]], [MAX_BREAKING, MAX_BREAKING], 'r-')
    acc_ax.grid()
    acc_ax.set_ylabel("Acceleration (u/s^2)")
    acc_ax.set_xlabel("Time (s)")
    
    kin_fig.suptitle("Race Kinematics")
    kin_fig.tight_layout(pad=0.5)
    kin_fig.savefig(os.path.join(NNASCAR_DATA, 'kinematics.png'))

if __name__ == '__main__':
    race()
