# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 00:50:35 2021

@author: Sean
"""

import glob
import imageio
import os
from PIL import Image

from parameters import NNASCAR_DATA

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

frame_path = os.path.join(NNASCAR_DATA, "frames")
all_frames = glob.glob(frame_path + "/frame*png")

images = []
for i in range(len(all_frames)):
    filename = os.path.join(frame_path, f"frame_{i}.png")
    images.append(imageio.imread(filename))
imageio.mimsave(os.path.join(NNASCAR_DATA, "racing.gif"), images)
