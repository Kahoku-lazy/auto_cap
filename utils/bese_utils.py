''' @author: Kahoku 
    @date: 2023/3/12
'''
import yaml
import collections
import logging
import time
import os
import serial
from configparser import ConfigParser

class GetData:

    def read_text(self, file_path):
        """return: list"""
        values=[]
        with open(file_path, mode="r", encoding='utf8') as f:
            for value in f:
                values.append(value.strip())
        return values
    
    def wirte_text(self, file_path, values):
        with open(file_path, mode="a", encoding='utf8') as f:
            f.truncate(0)
            f.seek(0, 0)
            for value in values:
                f.write(value)
                f.write("\n")

    def read_yaml(self, file_path, mode='r', encoding="utf8"):
        with open(file_path, mode=mode, encoding=encoding) as f:
            yaml_values = yaml.load(f, Loader=yaml.FullLoader)
        return yaml_values

    def read_config(self, file_path, section, option, encoding="utf8", type="str"):
        config = ConfigParser()
        config.read(file_path, encoding=encoding)
        if type == "str":
            value = config.get(section, option)
        elif type == "int":
            value = config.getint(section, option)
        return value
    
    def get_classes_dict(self, list_):
        """ function: 列表 转字典
        return type: dict
        """
        dict_ = collections.OrderedDict()          # 创建有序字典
        for key in list_:
            dict_[key] = 0
        return dict_

class GetLog:
    """ 记录Log日志 """

    def __init__(self, file_path, logger_name="root"):
        """ 构造方法 
        log_name: 日志保存路径。
        logger_name: 
        """
        self.logger = logging.Logger(logger_name)
        self.logger.setLevel(logging.INFO)
        self.fmts = "%(asctime)s-:%(levelname)s: -- %(message)s"   # log输出格式
        self.dmt = "%Y/%m/%d %H:%M:%S"      # log时间格式

        # 修改log生成的文件名，避免日志文件名重复
        timer = time.strftime("_%Y%m%d_%H%M%S", time.localtime()) 
        path, filename = os.path.split(file_path)
        log_name, extension = os.path.splitext(filename)
        self.log_path = os.path.join(path, log_name + timer + extension)    

    def logger_init(self):
        """ 配置 logger """
        self.handler = logging.FileHandler(self.log_path, 'a+')
        formatter = logging.Formatter(self.fmts, self.dmt)
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)

    def info(self, message):
        """ 记录 log 信息 """
        self.logger_init()
        self.logger.info(message)
        self.logger.removeHandler(self.handler)

    def error(self, message):
        """ 记录 error 信息 """
        self.logger_init()
        self.logger.error(message)
        self.logger.removeHandler(self.handler)


class SerialWindows:

    def __init__(self, port, **kwargs):
        """ 构造方法
            串口参数设置
        """
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.apply_settings(kwargs)

    def get_serial_info(self):
        """ 获取串口信息 """
        serial_info = self.ser.get_settings()   
        return serial_info  

    def open_serial(self):
        """ 打开串口 """
        if not self.ser.is_open:
            self.ser.open()

    def close_serial(self):
        """ 关闭串口 """
        if self.ser.is_open:
            self.ser.close()

    def read_serila_data(self):
        """ 读取串口数据 """
        data = self.ser.readline()
        # DEBUG： 转编码会出错
        try:
            data = data.decode().strip()
        except UnicodeDecodeError:
            data = str(self.ser.readline())
        return data

    def get_buffer_data(self):
        """ 读取串口缓冲区的数据 """
        values = []
        while self.ser.in_waiting:
            values.append(self.read_serila_data())
        return values

    def set_buffer_size(self, rx_size = 1024 * 1024, tx_size = 128):
        """ 设置缓冲区大小"""
        self.ser.set_buffer_size(rx_size = rx_size, tx_size = tx_size)      

    def reset_buffer(self):
        """ 清除缓冲区 """
        self.ser.reset_input_buffer() 


if __name__ == "__main__":

    port = "COM6"
    ser = SerialWindows(port, baudrate=921600)
    ser.open_serial()
    while True:
        data = ser.read_serila_data()
        print(type(data))

