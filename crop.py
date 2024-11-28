import cv2
import os
from progressbar import ProgressBar
from config import obj_path

path = obj_path
result = path[:-1] + "_cut/"
if not os.path.isdir(result):
    os.makedirs(result)
obj_images = []
for name in os.listdir(path):
    obj_images.append(cv2.imread(path + name, -1))

with ProgressBar(max_value=len(obj_images)) as bar:
    img_n = 0
    for img in obj_images:
        ly, lx, _ = img.shape
        maxY, maxX = -1, -1
        minY, minX = -1, -1

        for y in range(ly):
            if sum(img[y, :, 3]) != 0:
                minY = y
                break
        for y in range(1, ly):
            if sum(img[-y, :, 3]) != 0:
                maxY = ly - y + 1
                break

        for x in range(lx):
            if sum(img[:, x, 3]) != 0:
                minX = x
                break
        for x in range(1, lx):
            if sum(img[:, -x, 3]) != 0:
                maxX = lx - x + 1
                break

        cv2.imwrite(result + str(img_n) + '.png', img[max(0, minY - 1):maxY + 2, max(0, minX - 1):maxX + 2, :])
        img_n += 1
        bar.update(img_n)
