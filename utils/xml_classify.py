# -*- coding: utf-8 -*-
import sys
import xml.etree.ElementTree as ET
import os
import shutil


# 打标内容
classes = ["Matching","Parachuting","Knocked_Down_Anermy","Killed","Asisit","Knocked","Reviving","Friendly_Fire","Bandaging_Wound","First_Aid_Kit","Energy_Drink","Painkillers","Med_Kit","Adrenaline_shot","Match_Finished","Chicken_Dinner","Defeat"]
current_path = os.getcwd()
# 训练集 验证集名称
images_train_path = os.path.join(current_path, "images/train")
labels_train_path = os.path.join(current_path, "labels/train")
images_val_path = os.path.join(current_path, "images/val")
labels_val_path = os.path.join(current_path, "labels/val")


def convert(img_size, box):
    dw = 1. / (img_size[0])
    dh = 1. / (img_size[1])
    x = (box[0] + box[2]) / 2.0 - 1
    y = (box[1] + box[3]) / 2.0 - 1
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(input_file, output_file):
    in_file = open(input_file, encoding='UTF-8')
    out_file = open(output_file, 'w')
    # xml解析文件
    tree = ET.parse(in_file)
    root = tree.getroot()
    # 获得size字段内容
    size = root.find('size')
    # 获得图片宽高
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    # 遍历object内容
    for obj in root.iter('object'):
        # 获得difficult字段(困难度)
        difficult = obj.find('difficult').text
        # 获得标签名
        cls = obj.find('name').text
        # 标签名不在分类中，或困难度等于1
        if cls not in classes or int(difficult) != 0:
            print(f"cls not in classes or difficult != 0, skip this obj, cls = {cls} difficult = {difficult}")
            continue
        # 获得打标元祖下标
        cls_id = classes.index(cls)
        # 获得打标框内容
        xml_box = obj.find('bndbox')
        box = (float(xml_box.find('xmin').text),
               float(xml_box.find('ymin').text),
               float(xml_box.find('xmax').text),
               float(xml_box.find('ymax').text))

        convert_box = convert((w, h), box)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in convert_box]) + '\n')
    in_file.close()
    out_file.close()


# 对数据集分类
def dataset_classify(train_percent, images_dir, labels_dir):
    if train_percent > 99 or train_percent < 1:
        print(f"train percent error :{train_percent}")
        return False
    elif not os.path.exists(images_dir):
        print(f"images dir no exists {images_dir}")
        return False
    elif not os.path.exists(labels_dir):
        print(f"labels dir no exists {labels_dir}")
        return False
    else:
        # 删除分类文件夹
        if os.path.exists(images_train_path):
            shutil.rmtree(images_train_path)
        if os.path.exists(labels_train_path):
            shutil.rmtree(labels_train_path)
        if os.path.exists(images_val_path):
            shutil.rmtree(images_val_path)
        if os.path.exists(labels_val_path):
            shutil.rmtree(labels_val_path)

        # 获取文件总数
        sum_file_num = len(os.listdir(images_dir))

        # 训练集文件数
        train_file_num = int(sum_file_num * train_percent / 100)

        # 验证集文件数
        val_file_num = sum_file_num - train_file_num

        print(f"sum file num:{sum_file_num} train file num:{train_file_num} val file num:{val_file_num}")

        # 训练集文件名
        train_file_list = []
        # 验证集文件名
        val_file_list = []
        # 文件计数
        cnt = 0

        # 对images下文件进行分类
        for each in os.listdir(images_dir):
            cnt += 1
            # 训练集文件名
            if cnt <= train_file_num:
                train_file_list.append(each)
            # 验证集文件名
            else:
                val_file_list.append(each)

        # 创建训练集和验证集文件夹
        os.mkdir(images_train_path)
        os.mkdir(labels_train_path)
        os.mkdir(images_val_path)
        os.mkdir(labels_val_path)

        # 复制训练集到指定文件夹
        for each in train_file_list:
            cur_path = os.path.join(images_dir, each)
            shutil.copy(cur_path, images_train_path)

        # # 复制验证集到指定文件夹
        for each in val_file_list:
            cur_path = os.path.join(images_dir, each)
            shutil.copy(cur_path, images_val_path)

        # 复制训练集label到指定文件夹
        for each in train_file_list:
            # 截断字符串 .jpg
            label_name = each[:-4] + ".txt"
            shutil.move(labels_dir + "/" + label_name, labels_train_path)

        # 复制验证集label到指定文件夹
        for each in val_file_list:
            # 截断字符串 .jpg
            label_name = each[:-4] + ".txt"
            shutil.move(labels_dir + "/" + label_name, labels_val_path)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 1.对输入文件夹进行转化
        input_folder = sys.argv[1]
        input_path = os.path.join(current_path, input_folder)

        if os.path.exists(input_path):
            # 2.删除原有文件夹
            label_path = os.path.join(current_path, "labels")
            if os.path.exists(label_path):
                shutil.rmtree(label_path)
            os.mkdir(label_path)

            # 3.遍历xml文件夹
            for xml_files in os.listdir(input_path):
                # 遍历jpg图片
                if xml_files.find('.xml') != -1:
                    # 获得文件名
                    xml_file_name = xml_files.split('.')[0]
                    input_file = os.path.join(input_path, xml_files)
                    output_file = os.path.join(label_path, xml_file_name + '.txt')
                    # 4.转xml文件为txt文件
                    convert_annotation(input_file, output_file)

            # 5.对文件进行分类 80%是训练集 20%是验证集
            dataset_classify(80, os.path.join(current_path, 'images'), label_path)
