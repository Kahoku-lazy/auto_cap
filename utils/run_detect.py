import os
import cv2
import time
import shutil
import multiprocessing
from multiprocessing import Manager, Pool, Process

class RunDetect:

    def __init__(self):

        self.video_dir = "../videos"
        self.pics_dir = "../pictures"
        self.class_dir = "../classes"

    def video_cap(self, video_path, out_put, name, captured_videos, capturing_videos):
        os.makedirs(out_put)
        videoCapture = cv2.VideoCapture(video_path)         
        fps = int(videoCapture.get(cv2.CAP_PROP_FPS))       
        frames = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)) 

        # print(f" === 视频名称: {video_path}, 视频帧率: {fps}, 视频帧数: {frames}\r\n")
        if fps > 60 or fps < 20:
            print(f"Error: {video_path} is error!")
            return
        print(f"开始分帧视频 {video_path}")

        (path, filename) = os.path.split(video_path)
        (name, extension) = os.path.splitext(filename)
        name = name.replace(" ", "_")   # 去空格

        cnt = 0
        fps_cnt = fps
        while True:
            ret = videoCapture.grab()       
            if not ret: break

            if (cnt % fps_cnt) == 0:
                ret, frame = videoCapture.retrieve()
                file_name = os.path.join(out_put, f"{name}_{int(cnt / fps_cnt)}.jpg")
                cv2.imwrite(file_name, frame)   
            cnt += 1

        videoCapture.release()
        print(f"视频 {video_path}分帧完成")
        capturing_videos.remove(name)
        captured_videos.append(name)

    def find_new_video(self,video_path, captured_videos, capturing_videos):
        valid_suffix = [".mp4", ".webm"]
        files = os.listdir(video_path)
        for file in files:
            (name, extension) = os.path.splitext(file)
            if extension in valid_suffix:
                if (name not in captured_videos) and (name not in capturing_videos):
                    capturing_videos.append(name)
                    return file
        return None

    def run_cap_video(self, captured_videos, capturing_videos, count=3):
        po = Pool(count)
        while True:
            video = self.find_new_video(self.video_dir, captured_videos, capturing_videos)
            if video:
                video_path = os.path.join(self.video_dir, video)  # video/abc.mp4
                (name, extension) = os.path.splitext(video) # (abc, .mp4)
                pics_output = os.path.join(self.pics_dir, name).replace(" ", "_") # pictures/abc
                
                if os.path.exists(pics_output):
                    shutil.rmtree(pics_output)
                po.apply_async(self.video_cap, (video_path, pics_output, name, captured_videos, capturing_videos))
            
            time.sleep(1)

    def run_detect(self, capturing_videos, detected_videos, model_path):
        cmd = "python yolov5/detect.py"
        while True:
            dirs = os.listdir(self.pics_dir)
            for name in dirs:
                if (name not in detected_videos) and (name not in capturing_videos):
                    
                    pics_output = os.path.join(self.pics_dir, name)
                    class_output = os.path.join(self.class_dir, name)
                    if os.path.exists(class_output):
                        shutil.rmtree(class_output)
                    os.makedirs(class_output)

                    cmd_source = f" --source {pics_output}"
                    cmd_crop = f" --save-crop"
                    cmd_weights = f" --weights {model_path}"
                    cmd = cmd + cmd_source + cmd_crop + " --save-txt" + cmd_weights
                    print(f"模型开始分类{pics_output}文件中的图片")
                    os.system(cmd)      # 运行指令
                    detected_videos.append(name)
                    if os.path.exists(r"./yolov5/runs/detect"):
                        shutil.rmtree(r"./yolov5/runs/detect")

            time.sleep(1)

    def run(self, model_path):
        captured_videos = Manager().list([])
        detected_videos = Manager().list([]) 
        capturing_videos= Manager().list([])

        cap_process = multiprocessing.Process(target = self.run_cap_video, args = (captured_videos, capturing_videos))
        det_process = multiprocessing.Process(target = self.run_detect, args = (capturing_videos, detected_videos, model_path))

        cap_process.start()
        det_process.start()

        while True:
            time.sleep(10)
        # cap_process.join()
        # det_process.join()

    def video_subframe(self):
        captured_videos,capturing_videos = [], []
        self.run_cap_video(captured_videos, capturing_videos)


if __name__ == "__main__":

    RunDetect().run()
    