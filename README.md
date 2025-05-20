# YOLO_SICISP
Self-trained YOLOv11 model based on traffic graphics on campus for SICISP class in School of Remote Sensing, Wuhan University.


本项目为武汉大学遥感院SICISP课程实习任务二而开发，旨在通过校内交通场景图片训练YOLOv11模型。项目包含数据处理、模型训练与目标跟踪等功能。

## 项目结构

- `clean.py`: 检查数据中是否包含不成对的图片与label文件，并检查label文件中的id号是否合法。
- `devide.py`: 将数据划分为`images`和`labels`目录，每个目录下分别有`train`、`test`、`val`子目录，划分比例为train80%，val15%，test5%。
- [devide2.py](file://c:\本学期学习资料（大三下）\空间智能计算与服务\空间智能计算与服务课程实习\test2\YOLO_SICISP\devide2.py): 数据划分脚本，生成`train`、`test`、`valid`三个目录，每个目录下分别有`images`和`labels`两个子目录，划分比例同上。
- [track.py](file://c:\本学期学习资料（大三下）\空间智能计算与服务\空间智能计算与服务课程实习\test2\YOLO_SICISP\track.py): 实现目标跟踪功能。
- [track_count.py](file://c:\本学期学习资料（大三下）\空间智能计算与服务\空间智能计算与服务课程实习\test2\YOLO_SICISP\track_count.py): 在目标跟踪基础上增加计数功能。
- [track_poly.py](file://c:\本学期学习资料（大三下）\空间智能计算与服务\空间智能计算与服务课程实习\test2\YOLO_SICISP\track_poly.py): 在目标跟踪基础上绘制轨迹。
- `source_data/`: 存放课程提供的原始数据。
- `results/`: 包含训练结果(`train_run`)、目标检测结果(`detect_run`)、目标跟踪结果(`track_run`)。

## 使用说明

### 数据清洗
```bash
python clean.py
```

### 数据划分方式一
```bash
python devide.py
```

### 数据划分方式二
```bash
python devide2.py
```

### 目标跟踪
```bash
python track.py
```

### 目标跟踪+计数
```bash
python track_count.py
```

### 目标跟踪+轨迹绘制
```bash
python track_poly.py
```

## 数据目录结构

### 原始数据
- `source_data/`

### 处理后数据
- `images/`
  - `train/`
  - `test/`
  - `val/`
- `labels/`
  - `train/`
  - `test/`
  - `val/`

### 训练与结果
- `results/train_run/`: 训练结果
- `results/detect_run/`: 目标检测结果
- `results/track_run/`: 目标跟踪结果

## 注意事项
- 确保所有依赖库已安装。
- 根据实际需求调整脚本参数。