import numpy as np
import cv2
import os
import config as cfg
from utils import *
from time import time

if not os.path.isdir(cfg.result_path): os.makedirs(cfg.result_path)
if not os.path.isdir(cfg.bg_path): raise Exception("Wrong bg_path")
if not os.path.isdir(cfg.object_path): raise Exception("Wrong object_path")

m = 0
ep_dir = f"{cfg.result_path}epoch{m}/"
if os.path.exists(ep_dir):
    m = max(int(i[5:]) for i in os.listdir(cfg.result_path)) + 1
    ep_dir = f"{cfg.result_path}epoch{m}/"
os.makedirs(ep_dir)
bgs = os.listdir(cfg.bg_path)
objects = os.listdir(cfg.object_path)

a = time()
n = 0
for bg in bgs:
    for obj in objects:
        data = generate_img(bg, obj)

        cv2.imwrite(f"{ep_dir}data{n}.jpg", data)
        n += 1
b = time()
print(b-a)