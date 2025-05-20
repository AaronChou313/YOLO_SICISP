import os
import shutil
import random

# 数据路径
image_dir = 'mydata/images'
label_dir = 'mydata/labels'

# 输出路径
output_image_train = 'yolodata/images/train'
output_image_val = 'yolodata/images/val'
output_image_test = 'yolodata/images/test'

output_label_train = 'yolodata/labels/train'
output_label_val = 'yolodata/labels/val'
output_label_test = 'yolodata/labels/test'

# 创建输出目录
os.makedirs(output_image_train, exist_ok=True)
os.makedirs(output_image_val, exist_ok=True)
os.makedirs(output_image_test, exist_ok=True)

os.makedirs(output_label_train, exist_ok=True)
os.makedirs(output_label_val, exist_ok=True)
os.makedirs(output_label_test, exist_ok=True)

# 获取所有成对的文件名（不带扩展）
image_files = {os.path.splitext(f)[0] for f in os.listdir(image_dir)}
label_files = {os.path.splitext(f)[0] for f in os.listdir(label_dir)}
common_files = list(image_files.intersection(label_files))

# 打乱顺序
random.seed(42)  # 固定随机种子以便复现
random.shuffle(common_files)

# 分割数据集
total = len(common_files)
train_split = int(total * 0.8)
val_split = int(total * 0.95)

train_files = common_files[:train_split]
val_files = common_files[train_split:val_split]
test_files = common_files[val_split:]

# 复制函数
def copy_pair(base_name, src_image_dir, src_label_dir, dst_image_dir, dst_label_dir):
    image_ext = os.path.splitext([f for f in os.listdir(src_image_dir) if base_name in f][0])[1]
    image_path = os.path.join(src_image_dir, base_name + image_ext)
    label_path = os.path.join(src_label_dir, base_name + '.txt')
    
    shutil.copy(image_path, os.path.join(dst_image_dir, os.path.basename(image_path)))
    shutil.copy(label_path, os.path.join(dst_label_dir, os.path.basename(label_path)))

# 开始复制
for base_name in train_files:
    copy_pair(base_name, image_dir, label_dir, output_image_train, output_label_train)

for base_name in val_files:
    copy_pair(base_name, image_dir, label_dir, output_image_val, output_label_val)

for base_name in test_files:
    copy_pair(base_name, image_dir, label_dir, output_image_test, output_label_test)

# 输出结果
print(f"共处理 {len(common_files)} 对文件：")
print(f"训练集 (train): {len(train_files)} 对")
print(f"验证集 (val): {len(val_files)} 对")
print(f"测试集 (test): {len(test_files)} 对")