import cv2
import os
from progressbar import ProgressBar
from config import obj_path

path = obj_path
result = path[:-1] + "_cut/"
os.makedirs(result)
obj_images = []
for name in os.listdir(path):
    obj_images.append(cv2.imread(path + name, -1))

with ProgressBar(max_value=len(obj_images)) as bar:
    img_n = 0
    for img in obj_images:
        lx, ly, _ = img.shape
        maxX, maxY = -1, -1
        minX, minY = -1, -1

        for x in range(lx):
            if sum(img[x, :, 3]) != 0:
                minX = x
                break
        for x in range(1, lx):
            if sum(img[-x, :, 3]) != 0:
                maxX = lx - x + 1
                break

        for y in range(ly):
            if sum(img[:, y, 3]) != 0:
                minY = y
                break
        for y in range(1, ly):
            if sum(img[:, -y, 3]) != 0:
                maxY = ly - y + 1
                break

        cv2.imwrite(result + str(img_n) + '.png', img[minX - 1:maxX + 2, minY - 1:maxY + 2, :])
        img_n += 1
        bar.update(img_n)
