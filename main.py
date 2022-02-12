import numpy as np
import cv2
import os
import config as cfg
import Utils

if not os.path.isdir(cfg.result_path): os.makedirs(cfg.result_path)
if not os.path.isdir(cfg.bg_path): raise Exception("Wrong bg_path")
if not os.path.isdir(cfg.object_path): raise Exception("Wrong object_path")

