""" 坐标转换 """
import cv2
import os

fname = 'D:\Kahoku\HDMI_Project\Overwatch_classes\Change_Hero'

def read_txt(txt_path):
    """ 每行后有\n字符串"""
    values = []
    with open(txt_path, 'r', encoding="utf8") as f:
        for value in f:
            values.append(value.strip())
    return values


def coord_to_label():
     """(yolo 坐标转label)
    x_center = (box[0]+box[1])/2.0
    y_center = (box[2]+box[3])/2.0
    x = x_center / size[0]
    y = y_center / size[1]

    w = (box[1] - box[0]) / size[0]
    h = (box[3] - box[2]) / size[1]
    
    # print(x, y, w, h)
    return (x,y,w,h)

    """

def label_to_coord(img_path, label_txt):
    """ 标签转换为坐标 """
    img = cv2.imread(img_path)
    height_img, width_img, channel= img.shape

    # 画矩形框 距离靠左靠上的位置 (yolo label转坐标)
    x_center = float(label_txt[1])*width_img + 1
    y_center = float(label_txt[2])*height_img + 1

    xminVal = int(x_center - 0.5*float(label_txt[3])*width_img)   # int(label_txt列表中的元素都是字符串类型
    yminVal = int(y_center - 0.5*float(label_txt[4])*height_img)
    xmaxVal = int(x_center + 0.5*float(label_txt[3])*width_img)
    ymaxVal = int(y_center + 0.5*float(label_txt[4])*height_img)

    pt1 = (xmaxVal, ymaxVal)   
    pt2 = (xminVal, yminVal)
    cv2.rectangle(img, pt1, pt2, (0, 0, 255), 2)
    
    cv2.imwrite(os.path.join(fname, os.path.split(img_path)[1]), img)

def main():
    img_path = r"D:\Kahoku\HDMI_Project\Overwatch\images\Change_Hero"
    images = os.listdir(img_path)

    label_path = r"D:\Kahoku\HDMI_Project\Overwatch\labels\Change_Hero"
    labels = os.listdir(label_path)

    for label in labels:
        img = label[:-3] + "jpg"

        path_lbl = os.path.join(label_path, label)
        label_txt = read_txt(path_lbl) 
        for lbl in label_txt:
            value = lbl.split(" ")
            path_img = os.path.join(img_path, img)
            print(path_img)
            label_to_coord(path_img, value)
        

if __name__ == "__main__":
    main()
