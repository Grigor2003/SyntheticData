import numpy as np
import cv2
import os
import config as cfg
from utils import *
from time import time

if not os.path.isdir(cfg.result_path): os.makedirs(cfg.result_path)
if not os.path.isdir(cfg.bg_path): raise Exception("Wrong bg_path")
if not os.path.isdir(cfg.obj_path): raise Exception("Wrong obj_path")

ep_dir = create_epoch()
os.makedirs(ep_dir)
bgs = os.listdir(cfg.bg_path)
objs = os.listdir(cfg.obj_path)

a = time()
n = 0
bg_n = 0
pack_path = ""
bgs_img = [cv2.imread(cfg.bg_path + bg) for bg in bgs]
objs_img = [cv2.imread(cfg.obj_path + obj, -1) for obj in objs]
for bg in bgs_img:
    if cfg.bg_packages:
        n = 0
        pack_path = "bg" + str(bg_n) + "/"
        os.makedirs(ep_dir + pack_path)
    for obj in objs_img:
        for _ in range(cfg.count):
            data = generate_img(bg, obj)
            cv2.imwrite(ep_dir + pack_path + "data" + str(n) + ".jpg", data)
            n += 1
    bg_n += 1

b = time()
print(b - a)
