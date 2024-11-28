import numpy as np
import cv2
import os
import config as cfg


def get_amount(obj, bg):
    return cfg.count * len(obj) * len(bg)


def get_new_epoch_path():
    m = 0
    p = os.listdir(cfg.result_path)
    while True:
        ep_dir = f"epoch{m}"
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
    bh, bw, c = on_this.shape
    h, w, a = this.shape
    if 1 - w > x or x > bw - 1 or 1 - h > y or y > bh - 1:
        print('hello')
        raise Exception("out of bounds")
    fh, th = 0, h
    fw, tw = 0, w
    if x < 0:
        fw = -x
    if y < 0:
        fh = -y
    if h > bh - y:
        th = bh - y
    if w > bw - x:
        tw = bw - x
    bg = on_this.copy()
    paste = bg[max(0, y):min(y + h, bh), max(0, x):min(x + w, bw)]
    obj = this[fh:th, fw:tw, :3]

    bg_alpha = None
    if a == 4:
        alpha = this[fh:th, fw:tw, -1] / 255
        alpha_n = np.array([alpha] * 3).transpose((1, 2, 0))
        alpha_t = 1.0 - alpha_n
        bg[max(0, y):min(y + h, bh), max(0, x):min(x + w, bw)] = paste * alpha_t + obj * alpha_n

        bg_alpha = np.zeros((bh, bw, c), dtype=np.uint8)
        #
        bg_alpha[max(0, y):min(y + h, bh), max(0, x):min(x + w, bw)] = alpha_n * 255
    else:
        bg[max(0, y):min(y + h, bh), max(0, x):min(x + w, bw)] = obj

    return bg, bg_alpha


def flip_img(img, flip_chance):
    if np.random.randint(0, 100) > flip_chance * 100: return img
    return cv2.flip(img, 1)


def add_blur(img, blur_chance, blur_spatial_rate, blur_intensity_rate=None):
    blured_img = img
    if np.random.randint(0, 100) > blur_chance * 100: return img
    blur_spatial_rate = get_rate(blur_spatial_rate) * 8
    if blur_intensity_rate:
        blur_intensity_rate = int(get_rate(blur_intensity_rate))
    if blur_spatial_rate == 0: return img
    if cfg.blur_filter == 'GaussianBlur':
        blured_img = cv2.GaussianBlur(img, (0, 0), blur_spatial_rate)
    elif cfg.blur_filter == 'bilateralFilter':
        blured_img = cv2.bilateralFilter(img, d=0, sigmaSpace=blur_spatial_rate, sigmaColor=blur_intensity_rate)
    return blured_img


def add_noise(img, noise_rate):
    noise_rate = get_rate(noise_rate)
    arg = int(noise_rate * 127)
    if arg == 0: return img

    if cfg.noise_type == 'uniform':
        noise = np.random.randint(-arg, arg, img.shape)
    elif cfg.noise_type == 'gaussian':
        # mean
        noise = np.random.randn(*img.shape) * arg
        noise = np.clip(noise, -arg, arg)

    return np.clip(img, arg, 255 - arg) + noise


def scale_img(img, scale_rate):
    scale_rate = get_rate(scale_rate)
    if scale_rate == 1:
        return img
    elif scale_rate == 0:
        return np.zeros(shape=(1, 1, 4))
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
    cx = str((x + w / 2) / bw)
    cy = str((y + h / 2) / bh)
    ax = str(w / bw)
    ay = str(h / bh)
    return " ".join([cx, cy, ax, ay])


def save_as_txt(text, path):
    with open(path + ".txt", 'a') as f:
        f.write(text + '\n')


def save_as_grayscale_img(img, path):
    if img.ndim != 3 or img.shape[2] != 3:
        raise ValueError("Input image must have shape (height, width, 3)")
    if img.dtype != np.uint8:
        img = np.clip(img, 0, 255).astype(np.uint8)
    success = cv2.imwrite(path, img)
    if not success:
        raise IOError(f"Failed to save image to {path}")


def generate_img(bg_img, obj_img):
    flipped_obj = flip_img(obj_img, cfg.flip_chance)
    # cv2.imwrite("alpha_step1.png", flipped_obj[:, :, -1])
    scaled_obj = scale_img(flipped_obj, cfg.scale_rate)
    # cv2.imwrite("alpha_step2.png", scaled_obj[:, :, -1])
    blured_img = scaled_obj.copy()
    alpha = (blured_img[:, :, -1] / 255.0).astype(np.float32)
    blurred_alpha = add_blur(alpha, cfg.blur_chance, cfg.blur_spatial_rate, cfg.blur_intensity_rate)
    blured_img[:, :, -1] = (blurred_alpha * alpha * 255).astype(np.uint8)
    # cv2.imwrite("alpha_step3.png", blured_img[:, :, -1])

    oh, ow, c = blured_img.shape
    bh, bw, _ = bg_img.shape

    if cfg.out_of_bounds:
        out_of_bounds_rate_w = get_rate(cfg.out_of_bounds_rate)
        out_of_bounds_rate_h = get_rate(cfg.out_of_bounds_rate)
        fx = - int(out_of_bounds_rate_w * ow)
        fy = - int(out_of_bounds_rate_h * oh)
        tx = bw - int((1 - out_of_bounds_rate_w) * ow)
        ty = bh - int((1 - out_of_bounds_rate_h) * oh)

    else:
        fx, fy = 0, 0
        tx = max(1, bw - ow)
        ty = max(1, bh - oh)

    if cfg.distribution == "gaussian":
        cx = (tx - abs(fx)) / 2
        cy = (ty - abs(fy)) / 2
        x = int(np.random.normal(cx, abs(cx / 1.5*4)))
        y = int(np.random.normal(cy, abs(cy / 1.5*4)))
        x = np.clip(x, fx, tx)
        y = np.clip(y, fy, ty)

    elif cfg.distribution == "uniform":
        x = np.random.randint(fx, tx)
        y = np.random.randint(fy, ty)
    else:
        x = 0
        y = 0

    img, bg_alpha = put(x, y, blured_img, bg_img)
    img_noised = add_noise(img, cfg.noise_rate)
    output = None
    if cfg.save_type == 'classification':
        output = get_coord_info(x, y, oh, ow, bh, bw)
    elif cfg.save_type == 'segmentation':
        output = bg_alpha
    return img_noised, output
