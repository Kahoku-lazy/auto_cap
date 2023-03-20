# auto_cap

### 一、环境配置

1.  **python环境包安装**

   ```bash
   # 安装运行环境指令
   pip install -r packages.txt
   
   # 导出环境安装包
   pip freeze > packages.txt
   ```

   

2. **运行目录检查**

   - 下载模型后，请检查一下目录

     ```bash
     |-- auto_cap  		# 主程序目录
     	|-- config		# 主配置目录
     	|-- labelImg	# 标注工具（GitHub上项目）
     	|-- report
     		|-- excel 
     		|-- html	
     		|-- logs
     	|-- runner
     		|-- classes		# yolo、labelImg 标签文件
     		|-- images
     		|-- model 		# yolo 模型文件
     	|-- test
     	|-- utils
     	|-- yolov5		# YOLO 模型
     |-- classes
     |-- Model_Result
         |-- images
         |-- labels
     |-- pictures
     |-- videos
     ```

     

   - 模型训练指令

     ```bash
     # 原本训练指令
     python train.py --batch-size 4 --epochs 200 --data .\test\data.yaml --weights yolov5n6.pt
     ```

     

   - 模型推理指令

     ```bash
     # 原本推理指令
     python detect.py --weights "模型文件" --conf-thres 0.8 --save-crop --source "输入图片路径"
     
     # 脚本推理指令
     python main.py 3("模型代号") --func detect_
     ```