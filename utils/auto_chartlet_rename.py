import os
import sys
import shutil
import cv2
import time

# 分辨率: 宽 X 高
resolution = {  
    "1080P": (1080, 1920),
    "4K": (2160, 3840)}

def template_rename(file_path):
    timer = time.strftime("%Y%m%d", time.localtime()) 
    count = 0
    for dir in os.listdir(file_path):
        path_dir = os.path.join(file_path, dir)

        for img in os.listdir(path_dir): 
            path_img = os.path.join(path_dir, img)
            img_cv = cv2.imread(path_img)
            (hight, wide, channel) = img_cv.shape

            name = dir + "-%s" + f"{timer}{count}" + os.path.splitext(img)[1]
            if (hight, wide) == resolution["1080P"]:
                name = name % "1080P"
                shutil.move(path_img, os.path.join(path_dir, name))
                # print(f"Picture Resolution = 1080p\nImags: {img}\nhight = {hight}, wide = {wide}, channel= {channel}\n")  

            elif (hight, wide) == resolution["4K"]:
                name = name % "4K"
                shutil.move(path_img, os.path.join(path_dir, name))
                # print(f"Picture Resolution = 4K\nImags: {img}\nhight = {hight}, wide = {wide}, channel= {channel}\n") 

            count += 1 
    return count

def background_rename(file_path):
    timer = time.strftime("%Y%m%d", time.localtime()) 
    count = 0
    for img in os.listdir(file_path): 
        path_img = os.path.join(file_path, img)
        img_cv = cv2.imread(path_img)
        (hight, wide, channel) = img_cv.shape

        name = "%s" + f"{timer}{count}" + os.path.splitext(img)[1]
        if (hight, wide) == resolution["1080P"]:
            name = name % "1080P"
            shutil.move(path_img, os.path.join(file_path, name))
            # print(f"Picture Resolution = 1080p\nImags: {img}\nhight = {hight}, wide = {wide}, channel= {channel}\n")  

        elif (hight, wide) == resolution["4K"]:
            name = name % "4K"
            shutil.move(path_img, os.path.join(file_path, name))
            # print(f"Picture Resolution = 4K\nImags: {img}\nhight = {hight}, wide = {wide}, channel= {channel}\n") 

        count += 1 
    return count

if __name__ == "__main__": 
    # file_path = "D:\Kahoku\HDMI-DATA\Game_Pictures\Fortnite\pictures\Image_Matting\V40_Chartlet\V40Template"

    argv_ = sys.argv
    if len(argv_) == 3 and argv_[1] == '--t':
        count = template_rename(argv_[2])
        print(f"修改了{count}张图片")

    elif len(argv_) == 3 and argv_[1] == '--bg':
        count = background_rename(argv_[2])
        print(f"修改了{count}张图片")

    else:
        print(">>> ERROR!!!\n>>> 参数错误, 请按照下面的格式输入命令")
        print(">>>抠图素材重命名: python auto_chartlet_rename.py --t【文件路径】")
        print(">>>背景图素材重命名: python auto_chartlet_rename.py --bg【文件路径】")
    