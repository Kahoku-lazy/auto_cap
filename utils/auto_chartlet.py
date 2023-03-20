import cv2
import numpy as np
import os
import sys
import time

# 分辨率: 宽 X 高
resolution = {  
    "1080P": (1080, 1920),
    "4K": (2160, 3840)}

def add_alpha_channel(img):
    b_channel, g_channel, r_channel = cv2.split(img) 
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 
    img_new = cv2.merge((b_channel, g_channel, r_channel, alpha_channel)) 
    return img_new
 
def merge_img(jpg_img, png_img, y1, y2, x1, x2):
    if jpg_img.shape[2] == 3:
        jpg_img = add_alpha_channel(jpg_img)   
    yy1, xx1 = 0, 0
    yy2 , xx2 = png_img.shape[0], png_img.shape[1]
    alpha_png = png_img[yy1:yy2,xx1:xx2,3] / 255.0
    alpha_jpg = 1 - alpha_png
    for c in range(0,3):
        jpg_img[y1:y2, x1:x2, c] = ((alpha_jpg * jpg_img[y1:y2,x1:x2,c]) + (alpha_png * png_img[yy1:yy2,xx1:xx2,c]))

    return jpg_img

def start_chartlet(template_png, background_jpg, path_):

    template= cv2.imread(template_png, cv2.IMREAD_UNCHANGED)
    background = cv2.imread(background_jpg, cv2.IMREAD_UNCHANGED)
    x1, y1 = 0, 0
    x2, y2 = x1 + template.shape[1], y1 + template.shape[0]
    img = merge_img(background, template, y1, y2, x1, x2)
    
    cv2.imwrite(path_, img)

def get_imginfo(img):

    img_cv = cv2.imread(img)
    hight, wide, channel = img_cv.shape

    return (hight, wide, channel)


if __name__ == '__main__':

    file_path = "D:\Kahoku\HDMI-DATA\Game_Pictures\Fortnite\pictures\V40-ImageMatting\V40-Chartlet"


    start_time = time.time()
    timer = time.strftime("%Y%m%d", time.localtime())
    argv_ = sys.argv

    if len(argv_) == 3:
        background_path = os.path.join(argv_[2])
        chartlet_path = os.path.join(os.path.split(argv_[2])[0], "Chartlet")
        print(f"background_path={background_path}\nchartlet_path={chartlet_path}")

        count = 0
        for dir in os.listdir(argv_[1]):
            img_path = os.path.join(argv_[1], dir)
            for img in os.listdir(img_path):
                template_png = os.path.join(img_path, img)
                template_resolution = get_imginfo(template_png)

                for bg in os.listdir(background_path):
                    background_jpg = os.path.join(background_path, bg)
                    background_resolution = get_imginfo(background_jpg)

                    if template_resolution[:2] == background_resolution[:2]:
                        chartlet_path_ = os.path.join(chartlet_path, dir)
                        if not os.path.exists(chartlet_path_):
                            os.makedirs(chartlet_path_)
                        print(f"background_path={background_path}\nchartlet_path={chartlet_path_}")

                        img_name = chartlet_path_ + f'/{dir}-{bg}'
                        start_chartlet(template_png, background_jpg, img_name)
                        count += 1
     

        print(f"总共贴了{count}张图片")


    else:
        print(">>> ERROR!!!\n>>> 参数错误, 请按照下面的格式输入命令\n>>> python auto_chartlet.py 【文件路径】【背景图文件名称】")
 

    
