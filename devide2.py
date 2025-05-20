import os
import random
import shutil
from pathlib import Path

# 设置路径
dataset_dir = Path('mydata_merged/available')
original_images_dir = dataset_dir / 'images'
original_labels_dir = dataset_dir / 'labels'

# 创建输出目录
for folder in ['train', 'valid', 'test']:
    (dataset_dir / folder / 'images').mkdir(parents=True, exist_ok=True)
    (dataset_dir / folder / 'labels').mkdir(parents=True, exist_ok=True)

# 获取所有图像文件名（去除后缀）
image_files = [f.stem for f in original_images_dir.glob('*') if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
random.shuffle(image_files)  # 打乱顺序

# 分割比例
total = len(image_files)
train_split = int(total * 0.8)
val_split = int(total * 0.95)

train_files = image_files[:train_split]
val_files = image_files[train_split:val_split]
test_files = image_files[val_split:]

# 复制函数
def copy_files(files, src_img_dir, src_lbl_dir, dst_img_dir, dst_lbl_dir):
    for stem in files:
        # 自动检测图像后缀
        img_file = next(src_img_dir.glob(f"{stem}.*"))
        label_file = src_lbl_dir / f"{stem}.txt"

        shutil.copy(str(img_file), str(dst_img_dir))
        if label_file.exists():
            shutil.copy(str(label_file), str(dst_lbl_dir))

# 执行复制
copy_files(train_files, original_images_dir, original_labels_dir,
           dataset_dir / 'train' / 'images', dataset_dir / 'train' / 'labels')
copy_files(val_files, original_images_dir, original_labels_dir,
           dataset_dir / 'valid' / 'images', dataset_dir / 'valid' / 'labels')
copy_files(test_files, original_images_dir, original_labels_dir,
           dataset_dir / 'test' / 'images', dataset_dir / 'test' / 'labels')

print(f"Total images: {total}")
print(f"Train: {len(train_files)}, Valid: {len(val_files)}, Test: {len(test_files)}")