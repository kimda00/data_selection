from skimage.metrics import structural_similarity as compare_ssim
import cv2
import os
from tqdm import tqdm

def compare_images(file1, file2, size=(256, 256)):
    img1 = cv2.imread(file1)
    img2 = cv2.imread(file2)
    img1 = cv2.resize(img1, size)
    img2 = cv2.resize(img2, size)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    score, _ = compare_ssim(gray1, gray2, full=True)
    return score

def process_images(src_folder, dest_folder, deleted_folder, threshold=0.6):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    if not os.path.exists(deleted_folder):
        os.makedirs(deleted_folder)

    filenames = os.listdir(src_folder)
    to_delete = set()

    for i in tqdm(range(len(filenames))):
        if filenames[i] in to_delete:
            continue  # 이미 삭제 목록에 있는 파일은 건너뜀
        img1_path = os.path.join(src_folder, filenames[i])
        for j in range(max(0, i-10), min(len(filenames), i+11)):
            if i != j and filenames[j] not in to_delete:
                img2_path = os.path.join(src_folder, filenames[j])
                score = compare_images(img1_path, img2_path)
                if score > threshold:
                    to_delete.add(filenames[j])

    # 남은 이미지 저장 및 삭제된 이미지 이동
    for filename in tqdm(filenames):
        src_path = os.path.join(src_folder, filename)
        if filename in to_delete:
            dest_path = os.path.join(deleted_folder, filename)
        else:
            dest_path = os.path.join(dest_folder, filename)
        cv2.imwrite(dest_path, cv2.imread(src_path))

src_folder = '/home/da0/Desktop/filter/train/images'
dest_folder = '/home/da0/Desktop/filter/ssid_test'
deleted_folder = '/home/da0/Desktop/filter/selected'
process_images(src_folder, dest_folder, deleted_folder)
