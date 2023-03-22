''' @author: Kahoku 
    @date: 2023/3/10
'''
import os
import time
import shutil
import re
import pandas as pd
import numpy
import cv2
from PIL import Image

class FileHandling:

    def __init__(self):
        self.timer = time.strftime("%Y%m%d", time.localtime()) 
        self.file_suffix = ['.jpg', '.txt', '.png']

    def _create_dir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def move_file_match(self, image_path, label_path, new_path, max_count=None):
        """ 移动文件，图片标签匹配"""
        count_sum = 0
        for dir in os.listdir(image_path):
            img_dir_path = os.path.join(image_path, dir)
            try: 
                label_dir_path = os.path.join(label_path, dir)
            except:
                print(f">>> {dir}文件移动失败，图片没有对应的标签。")
                continue

            count = 0
            for image in os.listdir(img_dir_path):
                img  = os.path.join(img_dir_path, image)
                name = image.replace(self.file_suffix[0], self.file_suffix[1])   # 替换
                label = os.path.join(label_dir_path, name)
                if isinstance(max_count, int) and count == max_count:
                    break
                label_new_path = f"{new_path}/labels/{dir}"
                image_new_path = f"{new_path}/images/{dir}"
                if name in os.listdir(label_dir_path):
                    self._create_dir(label_new_path)
                    self._create_dir(image_new_path)
                    shutil.move(label, os.path.join(label_new_path, name))
                    shutil.move(img, os.path.join(image_new_path, image))
                    count += 1
                    count_sum += 1
        return count_sum

    def rename_file(self, file_path, fname, number):
        """ 文件重命名"""
        for dir in os.listdir(file_path):
            path_ = os.path.join(file_path, dir)
            for img in os.listdir(path_ ):
                (name, extension) = os.path.splitext(img)
                img_name = fname + self.timer + number + extension
                shutil.move(os.path.join(path_, img), 
                            os.path.join(path_, img_name)) 
                number += 1

    def rename_file_match(self, image_path, label_path, ver, number, classes):
        """ 文件重命名 标签图片匹配"""
        for dir in os.listdir(image_path):
            img_path = os.path.join(image_path, dir)
            lbl_path = os.path.join(label_path, dir)
            serial_number = classes.index(dir)
            for img in os.listdir(img_path):
                (name, extension) = os.path.splitext(img)
                label = img.replace(self.file_suffix[0], self.file_suffix[1])   # 替换
                new_name = str(serial_number) + '-' + ver + self.timer + str(number)

                if label in os.listdir(lbl_path):  
                    shutil.move(os.path.join(lbl_path, label), f"{lbl_path}/{new_name}{self.file_suffix[1]}") # label name
                    shutil.move(os.path.join(img_path, img), f"{img_path}/{new_name}{self.file_suffix[0]}") # img name
                    number += 1
        print(f"number: {number}")

    def classes_txt(self, label_path, ele, classes_path):
        """ function: 功能： 添加 classes.txt 标签到指定目录下
        """
        add_count, del_count  = 0, 0
        classes_name = os.path.basename(classes_path)  #  classes.txt

        for dir in os.listdir(label_path):
            path_ =os.path.join(label_path, dir)
            if ele == "del" and  classes_name in os.listdir(path_):
                os.remove(os.path.join(path_ , classes_name))
                del_count += 1
            elif ele == "add" and classes_name not in os.listdir(path_):
                shutil.copy(classes_path, os.path.join(path_, classes_name))
                add_count += 1

        print(f"已添加{add_count}, 已删除{del_count}")

    def replace_label_number(self, label_path, classes_file, data_):
        """ 修改标签序号 """
        count = 0   # 改动的标签计数

        classed = data_.read_text(classes_file[0])     # classes 
        classing = data_.read_text(classes_file[1])    # new classes
       
        if len(classes_file) > 2 and len(classes_file[0]) <= len(classes_file[1]):
            for dir in os.listdir(label_path):
                for label in os.listdir(os.path.join(label_path, dir)):
                    path = os.path.join(os.path.join(label_path, dir), label)
                    label_txt = data_.read_text(path)
                    values = []
                    for value in label_txt:
                        numbered = value.split(' ')[0].strip()
                        numbering = classing.index(classed[int(numbered)])
                        value = re.sub(r"^\d+", numbering, value)
                        values.append(value)
                    data_.wirte_text(path)  
                    
    def statistic_label_amount(slef, label_path, data_):
        ''' 统计标签数量 '''
        amount = [0 for i in range(100)]
        for dir in os.listdir(label_path):
            path_ = os.path.join(label_path, dir)
            for txt_ in os.listdir(path_):
                values = data_.read_text(os.path.join(path_, txt_))
                for value in values:
                    sn = value.split(" ")[0].strip()
                    amount[int(sn)] += 1
        return amount

    def statistic_file_amount_match(self, file_path, classes_dict):
        """ function: 统计目录下文件数目 """
        for dir in os.listdir(file_path):
            path = os.path.join(file_path, dir)
            classes_dict[dir] = len(os.listdir(path))
        return classes_dict
    
    def statistic_file_amount(self, file_path, dict_=None):
        """ function: 统计目录下文件数目 """
        if not dict_:
            dict_ = {}
        for dir in os.listdir(file_path):
            path = os.path.join(file_path, dir)
            dict_[dir] = len(os.listdir(path))
        return dict_
                  
    def dict_to_df(self, data_dict, df_column_1, df_column_2):
        """ 字典转df"""
        df = pd.DataFrame.from_dict(data_dict, orient='index', columns=[df_column_2])
        df = df.reset_index().rename(columns={'index': df_column_1})
        return df
    
    def check_count(self, image_count_dict, label_count_dict):
        """ function:  校验数据： 标签与图片的数量是否一致
        return df"""

        img_df = self.dict_to_df(image_count_dict, "dir_name", "image_count")
        label_df = self.dict_to_df(label_count_dict,"dir_name", "label_count")
        df = pd.merge(img_df, label_df)

        for i in range(len(df)):
            if df.loc[i, "image_count"] == df.loc[i, "label_count"]:
                df.loc[i, "relust"]= "Pass"
            else:
                df.loc[i, "relust"] = "Fail"
                # debug
                list_ = df.loc[i].values.tolist()
                print(f"Error>>> {list_[0]}目录下的图片与标签数量不相等")
                print(f"--- 图片数量{list_[1]}, 标签数量{list_[2]}， 相差{abs(list_[1]-list_[2])}")
        return df

    def check_file_name(self, image_path, label_path):
        """ function: 校验文件名是否一致 """
        dir_dict = {
            "img_dir_name": os.listdir(image_path),
            "label_dir_name": os.listdir(label_path)
        }
        dir_df = pd.DataFrame(dir_dict)
        for i in range(len(dir_df)):
            if dir_df.loc[i, "img_dir_name"] == dir_df.loc[i, "label_dir_name"]:
                dir_df.loc[i, "relust"]= "Pass"
            else:
                dir_df.loc[i, "relust"] = "Fail"
                print(dir_df.loc[i].values.tolist())
        if len(dir_dict['img_dir_name']) != len(dir_dict['label_dir_name']):
            print("Error>>> images目录下的文件夹与images目录下的文件夹数量不相等")
            return
        
        for dir in dir_dict['img_dir_name']:  
            labels = os.listdir(os.path.join(label_path, dir))
            for img in os.listdir(os.path.join(image_path, dir)):
                label = img.replace(self.file_suffix[0], self.file_suffix[1]) 
                if label not in labels:
                    print(f"Error>>> {dir}/{img}没有对应的label")

        return dir_df
    

    def check_labels(self, label_path, data_):
        """ 校验标签内容"""
        for dir in os.listdir(label_path):
            path_ = os.path.join(label_path, dir)
            for label in os.listdir(path_):
                values = data_.read_text(os.path.join(path_, label))
                label_value = set(values)
                if len(label_value) != len(values):
                    print(f"Error>>> {os.path.join(path_, label)} 标签内容重复")
                    print(f"--- {values}")
                    print(f"--- {label}内容已修改请检查 {os.path.join(path_, label)}")
                    data_.wirte_text(os.path.join(path_, label), list(label_value))

                if len(values) == 0:
                    print(f"Error>>> {os.path.join(path_, label)} 标签为空")
                    print(f"--- {values}")
                    print(f"--- {label}标签为空，请重新标注")
                    
    def check_demo(self, image_path, label_path, data_):
        """ function: 校验数据, 日志路径："""
        print(">>>", "strat check data", "<<<")
        print("************************************************************")
        print(">>> 开始校验文件名称: ")
        df = self.check_file_name(image_path, label_path)
        print(">>> 开始校验文件数量: ")
        img_count = self.statistic_file_amount(image_path)
        label_count = self.statistic_file_amount(label_path)
        df = self.check_count(img_count, label_count)
        print(">>>> 开始校验标签内容: ")
        self.check_labels(label_path, data_)
        print("***", "check data end", "***")

    def _calculate(self, image1, image2):
        image1 = cv2.cvtColor(numpy.asarray(image1), cv2.COLOR_RGB2BGR)
        image2 = cv2.cvtColor(numpy.asarray(image2), cv2.COLOR_RGB2BGR)
        hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
        hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
        # 计算直方图的重合度
        degree = 0
        for i in range(len(hist1)):
            if hist1[i] != hist2[i]:
                degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
            else:
                degree = degree + 1
        degree = degree / len(hist1)
        return degree
 
    def _classify_hist_with_split(self, image1, image2, size=(256, 256)):
        image1 = Image.open(image1)
        image2 = Image.open(image2)
        # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
        image1 = cv2.cvtColor(numpy.asarray(image1), cv2.COLOR_RGB2BGR)
        image2 = cv2.cvtColor(numpy.asarray(image2), cv2.COLOR_RGB2BGR)
        image1 = cv2.resize(image1, size)
        image2 = cv2.resize(image2, size)
        sub_image1 = cv2.split(image1)
        sub_image2 = cv2.split(image2)
        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += self._calculate(im1, im2)
        sub_data = sub_data / 3
        return sub_data
    
    def del_repeat_image_similarity(self, image_path, similarity=0.75):
        """ 将image_path目录下的相似度大于0.75的图片，移动到invalid_path目录下"""
        start_time = time.time()
        count = 0
        for dir in os.listdir(image_path):
            dir_path = os.path.join(image_path, dir)

            images = os.listdir(dir_path)
            images_count = len(images)  # debug
            for i in range(1, len(images)):
                img_01 = os.path.join(dir_path, images[i-1])
                img_02 = os.path.join(dir_path, images[i])

                result = self._classify_hist_with_split(img_01, img_02)
                if result > similarity:       # similarity
                    os.remove(img_01)
                    count += 1

                    images_count = images_count - 1      # debug
                    print(f"{dir} images {images_count}/{len(images)} {img_01}")

        end_time = time.time()
        print(f"总共有：{len(images)}图片, 相识度大于0.65的有{count}张,总共花费{(end_time - start_time)//1}S.")
    

    def collect_classes_image(self, classes_img_path, image_path):
        ''' 汇总模型分类后 classes目录下的图片'''
        for video_name in os.listdir(classes_img_path):
            dir_path = os.path.join(classes_img_path, video_name)
            for dir in os.listdir(dir_path):
                img_path = os.path.join(dir_path, dir)
                new_path = f"{image_path}/{dir}"
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                for img in os.listdir(img_path):
                    shutil.move(os.path.join(img_path, img), os.path.join(new_path, img))

    def collect_picture(self, image_path, picture_path):
        """ 将image中图片，汇总到picture目录下"""
        for dir in os.listdir(image_path):
            img_path = os.path.join(image_path, dir)
            for img in os.listdir(img_path):
                shutil.move(os.path.join(img_path, img), os.path.join(picture_path, img))

    def picture_classify(self, picture_path, image_path, classes):
        """将picture分类放到image到目录下"""       
        for img in os.listdir(picture_path):
            sn = img.split("-")[0].strip()
            try:
                dir_name = classes[int(sn)]
                path_ = f"{image_path}/{dir_name}"
                if not os.path.exists(path_):
                    os.makedirs(path_)
                shutil.move(os.path.join(picture_path, img), os.path.join(path_, img))
            except:
                print("标签序号超出classes标签文本的范围")

    def picture_classify(self, picture_path, image_path, classes):
        """将picture分类放到image到目录下"""       
        for img in os.listdir(picture_path):
            sn = img.split("-")[0].strip()
            try:
                dir_name = classes[int(sn)]
                path_ = f"{image_path}/{dir_name}"
                if not os.path.exists(path_):
                    os.makedirs(path_)
                shutil.move(os.path.join(picture_path, img), os.path.join(path_, img))
            except:
                print("标签序号超出classes标签文本的范围")

    def del_repeat_image(self, image_path):
        """ 删除重复的图片 """
        list_ = []
        for dir in os.listdir(image_path):
            dir_path = os.path.join(image_path, dir)
            for img in os.listdir(dir_path):
                if img in list_:
                    os.remove(os.path.join(dir_path, img))
                    continue
                list_.append(img)

    def crops_move(self, crops_path, picture_path, count):
        """参考模型crops结果 移动图片"""
        pictures = os.listdir(picture_path)
        new_path = f"../Model_Result/images/{os.path.split(crops_path)[-1]}"
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        for i in os.listdir(crops_path):
            if i in pictures:
                shutil.move(os.path.join(picture_path, i), os.path.join(new_path, i))
                print(f"{os.path.split(picture_path)[-1]} >>> move to {i}")
                count += 1
        return count 
