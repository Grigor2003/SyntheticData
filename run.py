from utils import *
from progressbar import ProgressBar

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
    txt_path = ep_dir
else:
    data_path = ep_dir + "data/"
    txt_path = ep_dir + "label/"
    os.makedirs(data_path)
    os.makedirs(txt_path)

bg_names = os.listdir(cfg.bg_path)

obj_images = get_objects()

with ProgressBar(max_value=get_amount(obj_images, bg_names)) as bar:
    name_amount = 0
    for bg_name in bg_names:
        bg = cv2.imread(cfg.bg_path + bg_name)

        curr_data_path = data_path
        curr_txt_path = txt_path
        if cfg.bg_packages:
            curr_data_path += bg_name.replace(".", "__") + "/"
            curr_txt_path += bg_name.replace(".", "__") + "/"
            os.makedirs(curr_data_path)
            if not cfg.merge:
                os.makedirs(curr_txt_path)

        for obj in obj_images:
            for _ in range(cfg.count):
                img, txt = generate_img(bg, obj)
                save_as_txt(txt, curr_txt_path + str(name_amount))
                cv2.imwrite(curr_data_path + str(name_amount) + ".jpg", img)
                name_amount += 1
                bar.update(name_amount)
