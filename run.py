from utils import *
from progressbar import ProgressBar
from config import obj_count
import random

if not os.path.isdir(cfg.result_path):
    os.makedirs(cfg.result_path)
if not os.path.isdir(cfg.bg_path):
    raise Exception("Wrong bg_path")
if not os.path.isdir(cfg.obj_path):
    raise Exception("Wrong obj_path")

ep_dir = get_new_epoch_path()
os.makedirs(ep_dir)
if cfg.merge:
    data_path = ep_dir
    out_path = ep_dir
else:
    data_path = ep_dir + "data/"
    out_path = ep_dir + "label/"
    os.makedirs(data_path)
    os.makedirs(out_path)

bg_names = os.listdir(cfg.bg_path)

obj_images = get_objects()

with ProgressBar(max_value=get_amount(obj_images, bg_names)) as bar:
    name_amount = 0
    for bg_name in bg_names:
        bg = cv2.imread(cfg.bg_path + bg_name)

        curr_data_path = data_path
        curr_out_path = out_path
        if cfg.bg_packages:
            curr_data_path += bg_name.replace(".", "__") + "/"
            curr_out_path += bg_name.replace(".", "__") + "/"
            os.makedirs(curr_data_path)
            if not cfg.merge:
                os.makedirs(curr_out_path)

        for i in range(len(obj_images)):
            for _ in range(cfg.count):
                edited_img = bg
                for j, el in enumerate(random.sample(obj_images, random.randint(*obj_count))):
                    img, out = generate_img(edited_img, el)
                    edited_img = img
                    if cfg.save_type == "classification":
                        save_as_txt(out, curr_out_path + str(name_amount))
                    elif cfg.save_type == "segmentation":
                        if not os.path.isdir(curr_out_path + str(name_amount)):
                            os.makedirs(curr_out_path + str(name_amount))
                        save_as_grayscale_img(out, curr_out_path + str(name_amount) + '/' + f'{j}.jpg')
                blured_img = add_blur(img.astype(np.float32), cfg.blur_chance, cfg.blur_spatial_rate,
                                      cfg.blur_intensity_rate).astype(np.uint8)
                noised_img = add_noise(img, cfg.noise_rate)
                cv2.imwrite(curr_data_path + str(name_amount) + ".jpg", noised_img)
                name_amount += 1
                bar.update(name_amount)
