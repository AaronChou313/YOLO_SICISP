import os
import shutil

source_dir = 'source_data/'
data_tag = 'merged'
# 定义路径
image_dir = source_dir+'SICISPDataSet_'+data_tag
label_dir = source_dir+'SICISPYoloLabel_'+data_tag
output_available_images = 'mydata_'+data_tag+'/available/images'
output_available_labels = 'mydata_'+data_tag+'/available/labels'
output_unpaired_images = 'mydata_'+data_tag+'/unpair/images'
output_unpaired_labels = 'mydata_'+data_tag+'/unpair/labels'
output_error_images = 'mydata_'+data_tag+'/label_error/images'
output_error_labels = 'mydata_'+data_tag+'/label_error/labels'
# 创建输出目录
os.makedirs(output_available_images, exist_ok=True)
os.makedirs(output_available_labels, exist_ok=True)
os.makedirs(output_unpaired_images, exist_ok=True)
os.makedirs(output_unpaired_labels, exist_ok=True)
os.makedirs(output_error_images, exist_ok=True)
os.makedirs(output_error_labels, exist_ok=True)

# 合法类别ID集合
valid_ids = set(range(4))  # 0, 1, 2, 3

# 获取所有图片和标签文件名（不含扩展）
image_files = {os.path.splitext(f)[0] for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))}
label_files = {os.path.splitext(f)[0] for f in os.listdir(label_dir) if f.lower().endswith('.txt')}

# 找出匹配与未匹配的文件名
common_files = image_files.intersection(label_files)
unpaired_images = image_files - common_files
unpaired_labels = label_files - common_files

# 处理成对文件并进行标签检查
for base_name in common_files:
    # 构建原始路径
    image_ext = os.path.splitext([f for f in os.listdir(image_dir) if base_name in f][0])[1]
    image_path = os.path.join(image_dir, base_name + image_ext)
    label_path = os.path.join(label_dir, base_name + '.txt')

    # 检查标签是否合法
    is_valid = True
    try:
        with open(label_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            class_id = int(parts[0])
            if class_id not in valid_ids:
                is_valid = False
                break
    except Exception as e:
        print(f"[ERROR] Error reading {label_path}: {e}")
        is_valid = False

    # 分类复制
    if is_valid:
        shutil.copy(image_path, os.path.join(output_available_images, os.path.basename(image_path)))
        shutil.copy(label_path, os.path.join(output_available_labels, os.path.basename(label_path)))
        print(f"[INFO] Copied to available: {base_name}")
    else:
        shutil.copy(image_path, os.path.join(output_error_images, os.path.basename(image_path)))
        shutil.copy(label_path, os.path.join(output_error_labels, os.path.basename(label_path)))
        print(f"[ERROR] Invalid label found in {base_name}, copied to error folder.")

# 复制未配对图片
for base_name in unpaired_images:
    image_ext = os.path.splitext([f for f in os.listdir(image_dir) if base_name in f][0])[1]
    image_path = os.path.join(image_dir, base_name + image_ext)
    shutil.copy(image_path, os.path.join(output_unpaired_images, os.path.basename(image_path)))
    print(f"[INFO] Unpaired image: {base_name}")

# 复制未配对标签
for base_name in unpaired_labels:
    label_path = os.path.join(label_dir, base_name + '.txt')
    shutil.copy(label_path, os.path.join(output_unpaired_labels, os.path.basename(label_path)))
    print(f"[INFO] Unpaired label: {base_name}")

# 输出统计信息
print(f"\n✅ 成功处理 {len(common_files)} 对匹配的图片和标签。")
print(f" - 正常数据已保存至：{output_available_images} 和 {output_available_labels}")
print(f" - 异常标签数据已保存至：{output_error_images} 和 {output_error_labels}")
print(f" - 未配对图片数量：{len(unpaired_images)}，已保存至：{output_unpaired_images}")
print(f" - 未配对标签数量：{len(unpaired_labels)}，已保存至：{output_unpaired_labels}")