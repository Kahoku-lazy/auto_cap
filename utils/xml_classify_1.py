# -*- coding: utf-8 -*-
import sys
import xml.etree.ElementTree as ET
import os
import shutil

# 打标内容
classes = ["Matching","Parachuting","Knocked_Down_Anermy","Killed",
           "Asisit","Knocked","Reviving","Friendly_Fire","Bandaging_Wound",
           "First_Aid_Kit","Energy_Drink","Painkillers","Med_Kit","Adrenaline_shot",
           "Match_Finished","Chicken_Dinner","Defeat"]


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
    try:
        tree = ET.parse(in_file)
    except:
        in_file.close()
        out_file.close()
        return
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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_path = sys.argv[1]        # xml 标签文件夹
        # 2.遍历xml文件夹   
        for dir in os.listdir(input_path):
            xml_dir = os.path.join(input_path, dir)
            for xml_files in os.listdir(xml_dir):

                xml_file_name = xml_files.split('.')[0]
                input_file = os.path.join(xml_dir, xml_files)
                out_path = os.path.join(sys.argv[2], dir)
                if not os.path.exists(out_path):
                    os.makedirs(out_path)
                output_file = os.path.join(out_path, xml_file_name + '.txt')
                # 4.转xml文件为txt文件
                print(f"xml to txt >>> {input_file} to {output_file}")
                convert_annotation(input_file, output_file)

