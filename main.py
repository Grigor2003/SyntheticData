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
p = os.listdir(cfg.result_path)
while True:
    ep_dir = "epoch" + str(m)
    if ep_dir in p:
        m += 1
    else:
        break
ep_dir = cfg.result_path + ep_dir + "/"

os.makedirs(ep_dir)
bgs = os.listdir(cfg.bg_path)
objs = os.listdir(cfg.object_path)

a = time()
n = 0

bgs_img = [cv2.imread(cfg.bg_path + bg) for bg in bgs]
objs_img = [cv2.imread(cfg.object_path + obj, -1) for obj in objs]
for bg in bgs_img:
    for obj in objs_img:
        for _ in range(cfg.count):
            data = generate_img(bg, obj)
            cv2.imwrite(f"{ep_dir}data{n}.jpg", data)
            n += 1
b = time()
print(b-a)