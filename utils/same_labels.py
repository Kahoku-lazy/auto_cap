import os
import shutil
import sys

#使用方法
# python same_labels.py img路径 labels路径

 # 创建一个txt文件
def create_txt(label_file, msg):
    file = open(label_file, 'w')
    file.writelines(msg)
    file.close()
    print(f"text:{msg}")
    print(f"{label_file}创建成功")


def same_labels(i_path, o_path):
    imgs_file = sorted(os.listdir(i_path))
    text = None
    cnt = 0
    for file_name in imgs_file:
        # print(file_name)
        if file_name.split(".")[-1] == "jpg" or "png":
            img_file = os.path.join(i_path, file_name)
            label_file_name = file_name[:-4] + ".txt"
            label_file = os.path.join(o_path, label_file_name)
            label_text = ""
            # if os.path.exists(label_file):
            #     with open(label_file, "r", encoding="utf-8") as f:
            #         for msg in f:
            #             label_text += msg
            #             if text == None:
            #                 text = label_text
            #         print("---test---")
            txt_file = os.listdir(o_path)
            for file in txt_file:
                txt = os.path.join(o_path, file)
                if file == "classes.txt":
                    continue
                else:
                    with open(txt, "r", encoding="utf-8") as f:
                        for msg in f:
                            label_text += msg
                        if text == None:
                            text = label_text
                # print(type(text))
            if not os.path.exists(label_file):
                # print(f"text:{text}")
                create_txt(label_file, text)
                cnt += 1
            # print(f"file_name:{file_name}")
    print(f"----count:{cnt}----")


                # create_txt(o_path, img_file[:-4], )



if __name__ == '__main__':
    #图片路径
    img_path = None
    #标签路径
    label_path = None

    if len(sys.argv) > 1:
        img_path = sys.argv[1]


    if len(sys.argv) > 2:
        label_path = sys.argv[2]

    same_labels(img_path, label_path)
    # create_txt("E:\\test\\T\\labels\\1.txt", "123456")