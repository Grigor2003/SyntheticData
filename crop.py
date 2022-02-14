import cv2
import os
from config import obj_path

path = obj_path
result = "Cut_" + path
os.makedirs(result)
obj_images = []
for name in os.listdir(path):
    obj_images.append(cv2.imread(path + name, -1))

img_n = 0
for img in obj_images:
    lx, ly, _ = img.shape
    maxX, maxY = -1, -1
    minX, minY = -1, -1
    for x in range(lx):
        for y in range(ly):
            if img[x, y, 3] != 0:
                if x > maxX: maxX = x
                if y > maxY: maxY = y
                if minX == -1:
                    minX = x
                elif minX > x:
                    minX = x
                if minY == -1:
                    minY = y
                elif minY > y:
                    minY = y
    cv2.imwrite(result + str(img_n) + '.png', img[minX:maxX + 1, minY:maxY + 1, :])
    img_n += 1
