import os
import numpy as np
import shutil

def del_repeat_image(image_path):
    """ 删除重复的图片 """
    list_ = []
    count = 0
    for dir in os.listdir(image_path):
        dir_path = os.path.join(image_path, dir)
        for img in os.listdir(dir_path):
            if img in list_:
                os.remove(os.path.join(dir_path, img))
                count += 1
                continue
            list_.append(img)
            
    print(f"删除了{count}张图片， 还剩下{len(list_)}张图片")

def move_same_name_image(image_, image2_):

    image_name = os.listdir(image_)
    file_path = r"D:\Kahoku\HDMI-DATA\Game_Pictures\Overwatch\pictures\Power\pictures"

    count = 0
    for img in os.listdir(image2_):
        path_ = os.path.join(image2_, img)
        if img in image_name:
            shutil.move(path_, os.path.join(file_path, img))
            print(f"move to {img}")
            count += 1
    print(f"move count {count}")



if __name__ == "__main__":
    # path_ = r"D:\Kahoku\HDMI-DATA\Game_Pictures\Overwatch\pictures\Power\crops"
    # path_2 = r"D:\Kahoku\HDMI_Project\overwatch\All\Eliminated"
    # move_same_name_image(path_, path_2)

    new_path = r"../Model_Result/images"
    print(os.path.split(new_path))