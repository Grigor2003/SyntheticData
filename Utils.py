import numpy as np
import cv2
import config as cfg

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
    if np.random.randint(0, 100) > blur_chance: return img

def add_noise(img, noise_rate):
    noise_rate = get_rate(noise_rate)
    arg = int(noise_rate * 127)
    if arg == 0: return img
    noise = np.random.randint(-arg, arg, img.shape)
    return np.clip(img, arg, 255 - arg) + noise

def get_rate(rate):
    if isinstance(rate, tuple):
        return np.random.rand() * (rate[1] - rate[0]) + rate[0]
    elif isinstance(rate, list):
        return np.random.choice(rate, 1)

def generate_img(bg, obj):
    bg_img = cv2.imread(f"{cfg.bg_path}{bg}")
    obj_img = cv2.imread(f"{cfg.object_path}{obj}", -1)
    img = bg_img

    for _ in range(cfg.count):
        x = np.random.randint(-obj_img.shape[0] + 1, bg_img.shape[0] - 1)
        y = np.random.randint(-obj_img.shape[1] + 1, bg_img.shape[1] - 1)
        img = put(x, y, obj_img, img)
    img_noised = add_noise(img, cfg.noise_rate)
    return img_noised
