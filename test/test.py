import os
import numpy as np
import shutil
import pandas as pd

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

def atuo_test_case():
    """ 自动生成H6601项目, AI灯效的测试用例 """
    title = ["用例编号", "用例标题", "测试点", "优先级", "前提条件", "操作步骤", "输入数据", "预期结果", "执行结果", "关联需求"]

    df = pd.DataFrame(columns=title)
    for i in range(9):
        df.loc[i, "用例编号"]= "HDMI-LAMP_EFFECT_%d" % i
        df.loc[i, "用例标题"]= "%s特征, 灯效内容显示正确" % "Eliminated"
        df.loc[i, "测试点"]= "游戏特征对应灯效显示正确"
        df.loc[i, "优先级"]= "高"
        df.loc[i, "前提条件"]= "显示器连接到H6601设备\r\n已知播放图片特征内容, 图片模型可识别"
        df.loc[i, "操作步骤"]= "播放%s特征图片" % "Eliminated"
        df.loc[i, "输入数据"]= "%s特征图片" % "Eliminated"
        df.loc[i, "预期结果"]= "灯效显示正确"
        df.loc[i, "执行结果"]= "None"
        df.loc[i, "关联需求"]= "None"
    df.to_excel(r"C:\Users\dingd\Desktop\test_case.xlsx")
    print(df)





if __name__ == "__main__":

    atuo_test_case()