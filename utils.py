import numpy as np
import cv2
import os
import config as cfg


def create_epoch():
    m = 0
    p = os.listdir(cfg.result_path)
    while True:
        ep_dir = "epoch" + str(m)
        if ep_dir in p:
            m += 1
        else:
            break
    ep_dir = cfg.result_path + ep_dir + "/"
    return ep_dir


def put(x, y, this, on_this):
    bh, bw, _ = on_this.shape
    h, w, a = this.shape
    if 1 - w > y or y > bw - 1 or 1 - h > x or x > bh - 1:
        raise Exception("out of bounds")
    fh, th = 0, h
    fw, tw = 0, w
    if x < 0:
        fh = -x
    if y < 0:
        fw = -y
    if h > bh - x:
        th = bh - x
    if w > bw - y:
        tw = bw - y
    bg = on_this.copy()
    paste = bg[max(0, x):min(x + h, bh), max(0, y):min(y + w, bw)]
    obj = this[fh:th, fw:tw, :3]

    if a == 4:
        alpha = this[fh:th, fw:tw, -1] / 255
        alpha_n = np.array([alpha] * 3).transpose((1, 2, 0))
        alpha_t = 1.0 - alpha_n
        bg[max(0, x):min(x + h, bh), max(0, y):min(y + w, bw)] = paste * alpha_t + obj * alpha_n
    else:
        bg[max(0, x):min(x + h, bh), max(0, y):min(y + w, bw)] = obj
    return bg


def add_blur(img, blur_chance, blur_rate):
    if np.random.randint(0, 100) > blur_chance * 100: return img
    blur_rate = get_rate(blur_rate) * 8
    blured_img = cv2.GaussianBlur(img, (0, 0), blur_rate)
    return blured_img


def add_noise(img, noise_rate):
    noise_rate = get_rate(noise_rate)
    arg = int(noise_rate * 127)
    if arg == 0: return img
    noise = np.random.randint(-arg, arg, img.shape)
    return np.clip(img, arg, 255 - arg) + noise


def scale_img(img, scale_rate):
    scale_rate = get_rate(scale_rate)
    h, w, _ = img.shape
    scaled_img = cv2.resize(img, (int(w * scale_rate), int(h * scale_rate)))
    return scaled_img


def get_rate(rate):
    if isinstance(rate, tuple):
        return np.random.rand() * (rate[1] - rate[0]) + rate[0]
    elif isinstance(rate, list):
        return np.random.choice(rate, 1)


def generate_img(bg_img, obj_img):
    scaled_obj = scale_img(obj_img, cfg.scale_rate)
    blured_img = add_blur(scaled_obj, cfg.blur_chance, cfg.blur_rate)
    oh, ow, _ = blured_img.shape
    bh, bw, _ = bg_img.shape
    if cfg.out_of_bounds:
        fx, fy = 0, 0
        tx = bh - oh
        ty = bw - ow
    else:
        fx = - oh // 2
        fy = - ow // 2
        tx = bh + fx
        ty = bw + fy

    cx = (tx - abs(fx)) / 2
    cy = (ty - abs(fy)) / 2
    x = int(np.random.normal(cx, abs(cx / 1.5)))
    y = int(np.random.normal(cy, abs(cy / 1.5)))
    x = np.clip(x, fx, tx)
    y = np.clip(y, fy, ty)
    img = put(x, y, blured_img, bg_img)
    img_noised = add_noise(img, cfg.noise_rate)
    return img_noised
