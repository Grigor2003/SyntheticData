import numpy as np
import cv2
import os
import config as cfg
from utils import *
from time import time

if not os.path.isdir(cfg.result_path):
    os.makedirs(cfg.result_path)
if not os.path.isdir(cfg.bg_path):
    raise Exception("Wrong bg_path")
if not os.path.isdir(cfg.obj_path):
    raise Exception("Wrong obj_path")

ep_dir = get_new_epoch_path()
os.makedirs(ep_dir)
bg_names = os.listdir(cfg.bg_path)
obj_names = os.listdir(cfg.obj_path)

s1 = time()
##########################
obj_images = [cv2.imread(cfg.obj_path + obj, -1) for obj in obj_names]
name_amount = 0
for bg_name in bg_names:
    bg = cv2.imread(cfg.bg_path + bg_name)

    curr_pack_path = ep_dir
    if cfg.bg_packages:
        curr_pack_path += bg_name.replace(".", "__") + "/"
        os.makedirs(curr_pack_path)

    for obj in obj_images:
        for _ in range(cfg.count):
            data = generate_img(bg, obj)
            cv2.imwrite(curr_pack_path + str(name_amount) + ".jpg", data)
            name_amount += 1
######################
s2 = time()
print(s2 - s1)
