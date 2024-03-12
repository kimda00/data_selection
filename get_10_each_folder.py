import os
import numpy as np
import shutil
from math import ceil
from tqdm import tqdm

def select_images_from_folders(base_path, target_percentage=0.1):
    folder_images = {}
    total_images_count = 0
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if images:
                folder_images[folder_name] = images
                total_images_count += len(images)
    total_select_count = int(ceil(total_images_count * target_percentage))
    selected_images = []
    all_images = []
    for folder_name, images in folder_images.items():
        all_images.extend(images)
        folder_image_count = len(images)
        select_count = max(1, int(ceil(folder_image_count / total_images_count * total_select_count)))
        selected = np.random.choice(images, size=select_count, replace=False).tolist()
        selected_images.extend(selected)
    unselected_images = [img for img in all_images if img not in selected_images]
    return selected_images, unselected_images

def save_image_paths(image_paths, file_path):
    with open(file_path, 'w') as file:
        for path in image_paths:
            image_name = os.path.basename(path)
            new_path = os.path.join(temp_path, image_name)
            file.write(new_path + '\n')

def save_selected_images(selected_images, save_directory):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    for img_path in tqdm(selected_images, desc="Copying selected images"):
        basename = os.path.basename(img_path)
        shutil.copy(img_path, os.path.join(save_directory, basename))

base_path = "./10p_test"
save_directory = "./10_percent_images"
temp_path = "local_path/datasets/trafficlight/train/images"
selected_images, unselected_images = select_images_from_folders(base_path, target_percentage=0.1)

save_selected_images(selected_images, save_directory)
save_image_paths(selected_images, 'labeled_images.txt')
save_image_paths(unselected_images, 'unlabeled_images.txt')
