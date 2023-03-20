import os
import pandas as pd

from utils.run_detect import RunDetect
from utils.bese_utils import GetData, SerialWindows, GetLog
from utils.file_handling import FileHandling
from test.test_device_model import TestDeviceModel

config_path = "./config/config.yaml"        # 配置文件路径

class Runner:

    def __init__(self, game_serial_number):

        self.data_ = GetData()

        self.test = TestDeviceModel()
        self.file_handling = FileHandling()
        self.run_detect = RunDetect()

        # config
        self.config = self.data_.read_yaml(config_path)

        # classes.txt
        self.classes_txt_path = self.config["classes_txt_path"].format(game_serial_number)
        self.classes_txt = self.data_.read_text(self.classes_txt_path)
        
        # model path
        self.model_path = self.config["yolo_model"].format(game_serial_number)

    def _replace_classes_txt_data(self, classed, classesing):
        values = self.data_.read_text(classed)
        self.data_.wirte_text(classesing, values)

    def _file_path(self, file_path):
        image_path = os.path.join(file_path, "images")
        label_path = os.path.join(file_path, "labels")

        return image_path, label_path
    
    def _get_methods(self, class_name):
        return (list(filter(lambda m: not m.startswith("_") and callable(getattr(self, m)),
                    dir(self))))
    
    def _count_show_format(slef, df):
        for i in range(len(df)):
            list_ = df.loc[i].values.tolist()
            print(f"{list_[0]}, {list_[1]}")


    def move_(self, args):
        """ file_path, new_path, max_count
            将file_path目录下的图片与标签一起移动只 new_path 目录下"""

        if len(args) == 3:
            file_path, new_path, max_count = args[0], args[1], args[2]
            image_path, label_path = self._file_path(file_path)  
        elif len(args) == 4:
             image_path, label_path, new_path, max_count = args[0], args[1], args[2], args[3]
        elif len(args) == 2:
            file_path, new_path, max_count = args[0], args[1], "None"
            image_path, label_path = self._file_path(file_path)  
        try:
            max_count = int(max_count) 
        except:
            pass   
        count = self.file_handling.move_file_match(image_path, label_path, new_path, max_count)
        print(f"成功移动了 {count} 张图片")

    def count_(self, path_):
        """ 统计数量 """
        classes_dict = self.data_.get_classes_dict(self.classes_txt)

        if len(path_) == 1 and os.path.isdir(path_[0]):
            dict_ = self.file_handling.statistic_file_amount(path_[0])
            df = self.file_handling.dict_to_df(dict_, "dir_name", "count")
            self._count_show_format(df)

        elif len(path_) > 1 and os.path.isdir(path_[0]):
            dict_ = self.file_handling.statistic_file_amount(path_[0], classes_dict)
            df = self.file_handling.dict_to_df(dict_, "dir_name", "count")
            self._count_show_format(df)

        return df

    def rename(self, args):
        """ file_path, ver, number
            文件重命名 """
        if len(args) != 3: 
            print("参数错误")
            return
        
        file_path, ver, number = args[0], args[1], int(args[2]) 
        image_path, label_path = self._file_path(file_path) 
        self.file_handling.rename_file_match(image_path, label_path, ver, number, self.classes_txt)

    def check(self, args):
        ''' 校验数据 '''
        if len(args) != 1: 
            print("参数错误")
            return
        
        image_path, label_path = self._file_path(args[0]) 
        self.file_handling.check_demo(image_path, label_path, self.data_)

    def classes_txt_(self, args):
        """ 添加或删除 classes.txt"""
        if len(args) != 2: 
            print("参数错误")
            return

        file_path, ele = args[0], args[1]
        print(file_path)
        classes_path = self.config["classes_txt_path"].format("classes")

        image_path, label_path = self._file_path(file_path)
        self._replace_classes_txt_data(self.classes_txt_path, classes_path)
        self.file_handling.classes_txt(label_path, ele, classes_path)
       
    def rm_empty_folder(self, args):
        """ 删除空文件夹 """
        folders = os.listdir(args[0])
        for folder in folders:
            folder_path = os.path.join(args[0], folder)
            file_count = len(os.listdir(folder_path))
            if file_count == 0:
                os.rmdir(folder_path)
                print(f"已删除{folder}")
        print("END")

    def test_01(self, args):
        image_path, port = args[0], args[1]
        bg = self.config["images"]["bg"]
        ser = SerialWindows(port, baudrate=115200)
        self.test_01_result = [0 for x in range(len(self.classes_txt))]
        df = self.test.run(image_path, self.test_01_result, ser, bg)
        dict_ = {
            "name": self.classes_txt,
            "TP": self.test_01_result
        }
        df = pd.DataFrame(dict_)
        df.to_excel(os.path.join(self.config['report']['excel_path'], "test_01.xlsx"))

    def detect_(self):
        """ 运行模型 """
        self.run_detect.run(self.model_path)

    def video_cap(self):
        """ 图片分帧"""
        self.run_detect.video_subframe()

    def labelimg_(self):
        """ 打开 labelImg"""
        classes_path = self.config['labelImg_classes_path']
        self._replace_classes_txt_data(self.classes_txt_path, classes_path)

        cmd = "python labelImg.py"
        os.chdir("./labelImg")
        os.system(cmd) 

    def label_amount(self, args):
        """ 统计标签数量"""
        label_path = args[0]
        amount_ = self.file_handling.statistic_label_amount(label_path, self.data_)
        dict_ = {
            "name": self.classes_txt,
            "amount": amount_[:len(self.classes_txt)]
        }
        df = pd.DataFrame(dict_)
        print(df)

    def del_repeat_image(self, args):
        """ 去掉重复的图片，将重复的图片移动到新的位置"""
        if len(args) == 2:
            image_path, similarity = args[0], args[2]
        elif len(args) == 1:
            image_path, similarity = args[0], 0.70

        self.file_handling.del_repeat_image_similarity(image_path, similarity)

    def collect_classes_image(self, args):
        ''' 汇总模型分类后 classes目录下的图片'''
        classes_img_path, image_path = args[0], args[1]
        self.file_handling.collect_classes_image(classes_img_path, image_path)

    def collect_picture(self, args):
        image_path, picture_path = args[0], args[1]
        self.file_handling.collect_picture(image_path, picture_path)

    def picture_classify(self, args):

        picture_path, image_path= args[0], args[1]
        self.file_handling.picture_classify(picture_path, image_path, self.classes_txt)

    def compare_move(self, args):
        """ 移动图片 """
        crop_path, picture_path = args[0], args[1]
        for picture_dir in os.listdir(picture_path):
            for dir in os.listdir(crop_path):
                path_ = os.path.join(crop_path, dir)
                self.file_handling.crops_move(path_ , os.path.join(picture_path, picture_dir))