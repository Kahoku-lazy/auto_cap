''' @author: Kahoku '''
import sys
import argparse
from runner.runner import Runner

class Main:
    def __init__(self):
        self.opt = self.parse_opt()

        self.run_ = Runner(self.opt.game_serial_number)
    
    def parse_opt(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('game_serial_number', type=int, help='游戏代号')
        parser.add_argument("--func", type=str, help='方法名称')
        parser.add_argument("--args", nargs='+', type=str, help='参数')
        return parser.parse_args()
    
    def run(self):
       
        if self.opt.func == "move_":
            self.run_.move_(self.opt.args)

        elif self.opt.func == "count_":
            self.run_.count_(self.opt.args)

        elif self.opt.func == "rename":
            self.run_.rename(self.opt.args)

        elif self.opt.func == "check":
            self.run_.check(self.opt.args)

        elif self.opt.func == "classes_txt_":
            self.run_.classes_txt_(self.opt.args)

        elif self.opt.func == "rm_empty_folder":
            self.run_.rm_empty_folder(self.opt.args)

        elif self.opt.func == "detect_":
            self.run_.detect_()

        elif self.opt.func == "video_cap":
            self.run_.video_cap()

        elif self.opt.func == "labelimg_":
            self.run_.labelimg_()

        elif self.opt.func == "test_01":
            self.run_.test_01(self.opt.args)
        
        elif self.opt.func == "label_amount":
            self.run_.label_amount(self.opt.args)

        elif self.opt.func == "del_repeat_image":
            self.run_.del_repeat_image(self.opt.args)

        elif self.opt.func == "collect_classes_image":
            self.run_.collect_classes_image(self.opt.args)
        
        elif self.opt.func == "collect_picture":
            self.run_.collect_picture(self.opt.args)

        elif self.opt.func == "picture_classify":
            self.run_.picture_classify(self.opt.args)

        elif self.opt.func == "compare_move":
            self.run_.compare_move()


    
if __name__ == "__main__":

    Main().run()

 


