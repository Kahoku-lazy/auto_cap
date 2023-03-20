''' @author: Kahoku '''
import cv2 as cv
import os
import re

class TestDeviceModel:

    def run(self, image_path, classes, ser, bg):
        """ 构造方法 """
        
        self.test_01(image_path, classes, ser, bg)

    def show_img(self, image, delay, winname="imgs"):
        """ 功能：打开图片 """
        img = cv.imread(image)
        cv.namedWindow(winname,cv.WINDOW_NORMAL)
        # cv.resizeWindow(winname, (1920,1080))
        # cv.moveWindow(winname, 1540, 0)
        cv.setWindowProperty(winname, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN) # 全屏
        cv.imshow(winname, img)
        key = cv.waitKey(delay)
        return key

    def model_result(self, img, serila_data, classes):
        """ 模型识别结果: TP
        """
        formula=r".*deteced: (\w+)"
        expect_result = img.split("-")[0].strip()
      
        regex = re.compile(formula)
        for value in serila_data:
            regex_match = regex.search(value)
            if regex_match:
                actual_result = regex_match.group(1)
                if actual_result == expect_result:
                    classes[int(actual_result)] += 1
                return expect_result, actual_result
        return expect_result, None

    
    def test_01(self, image_path, classes, ser, bg):
        """ 功能: 循环播放图片, 获取串口数据"""
        ser.open_serial()

        ser.set_buffer_size()
        for image in os.listdir(image_path):
            img = os.path.join(image_path, image)
            ser.reset_buffer() 

            key = self.show_img(img, 1500)
            serial_data = ser.get_buffer_data()
            result = self.model_result(image, serial_data, classes)
            if result[0] != result[1]:
                print(f">>> model result Error: 输入数据, 预测结果: {result}")
            else:
                print(f">>> model result Pass: 输入数据, 预测结果: {result}")
            self.show_img(bg, 500)
            if key == 27:   break

        ser.close_serial()
        cv.destroyAllWindows()    # 关闭窗口
        

        



if __name__ == "__main__":
    path_ = "D:\Kahoku\HDMI_Project\pictures"
    TestDeviceModel().run(path_, port="com3")
