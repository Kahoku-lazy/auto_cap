""" 通过对比图片相似度, 删除图片 """
import numpy
import cv2
import os
import shutil
import time
from PIL import Image


 
 
if __name__ == '__main__':
    path = r"D:\Kahoku\HDMI-DATA\Game_Pictures\Apex_Legends\Pictures\test_set\VXX\images"
    path_invalid = r"D:\Kahoku\HDMI-DATA\Game_Pictures\Apex_Legends\Pictures\test_set\VXX-similarity_0.65"

    start_time = time.time()
    count = 0
    for dir in os.listdir(path):
        dir_path = os.path.join(path, dir)
        dir_invalid = os.path.join(path_invalid, dir)

        images = os.listdir(dir_path)
        images_count = len(images)  # debug
        for i in range(1, len(images)):
            img_01 = os.path.join(dir_path, images[i-1])
            img_02 = os.path.join(dir_path, images[i])

            result = classify_hist_with_split(img_01, img_02)
            if result > 0.65:       # similarity
                if not os.path.exists(dir_invalid):
                    os.makedirs(dir_invalid)
                shutil.move(img_01, os.path.join(dir_invalid, images[i-1]))
                count += 1

                images_count = images_count - 1      # debug
                print(f"{dir} images {images_count}/{len(images)} {img_01}")

    end_time = time.time()
    print(f"总共有：{len(images)}图片, 相识度大于0.65的有{count}张,总共花费{(end_time - start_time)//1}S.")