''' @author: Kahoku '''
import cv2 as cv
import os
import re

class TestDeviceModel:

    def run(self, image_path, classes, ser, bg, Lamp_effect, log):
        """ 构造方法 """
        
        self.test_01(image_path, classes, ser, bg, Lamp_effect, log)

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

    def model_result(self, serila_data, regex_expression):
        """ 模型识别结果: TP
        """
        regex = re.compile(regex_expression)
        for value in serila_data:
            regex_match = regex.search(value)
            if regex_match:
                actual_result = regex_match.group(1)    # 模型预测结果
                return actual_result
        return None
    
    
    def test_01(self, image_path, classes, ser, bg, Lamp_effect, log):
        """ 功能: 循环播放图片, 获取串口数据"""
        ser_wifi, ser_ble = ser[0], ser[1]

        ser_wifi.open_serial()      # wifi串口
        ser_ble.open_serial()       # 蓝牙串口

        ser_wifi.set_buffer_size()
        ser_ble.set_buffer_size()
        for image in os.listdir(image_path):
            image_serial_number = image.split("-")[0].strip()  
            img = os.path.join(image_path, image)
            ser_wifi.reset_buffer() 
            ser_ble.reset_buffer() 

            key = self.show_img(img, 1500)
            ser_wifi_data = ser_wifi.get_buffer_data()
            ser_ble_data = ser_ble.get_buffer_data()
            wifi_result = self.model_result(ser_wifi_data, r".*deteced: (\w+)")
            ble_result = self.model_result(ser_ble_data, r".*: id (\w+)")
            print(f">>> model result: image name={image}, model id={wifi_result}, Lamp_effect id={ble_result}")
            if wifi_result and wifi_result.isdigit() and int(wifi_result) >= len(Lamp_effect) and wifi_result == image_serial_number:
                log.info(f">>> model result(Not Lamp Effect): image name={image}, model id={wifi_result}, Lamp_effect id={ble_result}")
                continue
            elif wifi_result and wifi_result.isdigit()  and int(wifi_result) >= len(Lamp_effect) and wifi_result != image_serial_number:
                log.error(f">>> model result: image name={image}, model id={wifi_result}, Lamp_effect id={ble_result}")
                continue
            if wifi_result and wifi_result.isdigit() and ble_result and wifi_result == image_serial_number and ble_result == str(Lamp_effect[int(wifi_result)]):
                classes[int(wifi_result)] += 1
                log.info(f">>> model result: image name={image}, model id={wifi_result}, Lamp_effect id={ble_result}")
            else:
                log.error(f">>> model result: image name={image}, model id={wifi_result}, Lamp_effect id={ble_result}")
            self.show_img(bg, 500)
            if key == 27:   break

        ser_wifi.close_serial()
        ser_ble.close_serial()
        cv.destroyAllWindows()    # 关闭窗口
        

        



if __name__ == "__main__":
    path_ = "D:\Kahoku\HDMI_Project\pictures"
    TestDeviceModel().run(path_, port="com3")
