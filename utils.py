import numpy as np
import cv2
import os
import config as cfg


def get_new_epoch_path():
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


def get_objects():
    obj_images = []
    for name in os.listdir(cfg.obj_path):
        path = cfg.obj_path + name
        if cfg.ignore_symbol not in name:
            obj_images.append(cv2.imread(path, -1))
    return obj_images


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
    if blur_rate == 0: return img
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
    if scale_rate == 1: return img
    elif scale_rate == 0: return np.zeros(shape=(1, 1, 4))
    h, w, _ = img.shape
    scaled_img = cv2.resize(img, (int(w * scale_rate), int(h * scale_rate)))
    return scaled_img


def get_rate(rate):
    if isinstance(rate, tuple):
        return np.random.rand() * (rate[1] - rate[0]) + rate[0]
    elif isinstance(rate, list):
        return np.random.choice(rate, 1)
    else:
        return rate


def get_coord_info(x, y, h, w, bh, bw):
    cx = str((x + h / 2) / bh)
    cy = str((y + w / 2) / bw)
    ax = str(h / bh)
    ay = str(w / bw)
    return " ".join([cx, cy, ax, ay])


def save_as_txt(text, path):
    with open(path + ".txt", 'w') as f:
        f.write(text)


def generate_img(bg_img, obj_img):
    scaled_obj = scale_img(obj_img, cfg.scale_rate)
    blured_img = add_blur(scaled_obj, cfg.blur_chance, cfg.blur_rate)

    oh, ow, _ = blured_img.shape
    bh, bw, _ = bg_img.shape
    if cfg.out_of_bounds:
        fx = - oh + 1
        fy = - ow + 1
        tx = bh - 1
        ty = bw - 1
    else:
        fx, fy = 0, 0
        tx = bh - oh
        ty = bw - ow

    if cfg.distribution == "gaussian":
        cx = (tx - abs(fx)) / 2
        cy = (ty - abs(fy)) / 2
        x = int(np.random.normal(cx, abs(cx / 1.5)))
        y = int(np.random.normal(cy, abs(cy / 1.5)))
        x = np.clip(x, fx, tx)
        y = np.clip(y, fy, ty)
    elif cfg.distribution == "linear":
        x = np.random.randint(fx, tx)
        y = np.random.randint(fy, ty)
    else:
        x = 0
        y = 0

    img = put(x, y, blured_img, bg_img)
    img_noised = add_noise(img, cfg.noise_rate)
    txt = get_coord_info(x, y, oh, ow, bh, bw)
    return img_noised, txt
