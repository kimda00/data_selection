import cv2
import numpy as np
import os
import shutil
from tqdm import tqdm

def calculate_image_features(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 밝기 계산
    brightness = np.mean(gray)
    
    # 흐림 정도 계산 (라플라시안 분산)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    return brightness, laplacian_var

def classify_and_save_images(image_paths, base_save_path):
    # 분류 기준치 설정
    brightness_thresholds = (80, 170)  # 밝기: 어두운, 중간, 밝은
    sharpness_thresholds = (100, 500)   # 흐림 정도: 흐린, 중간, 또렷한
    
    # 결과 저장을 위한 딕셔너리 초기화
    classification_results = {}

    for path in tqdm(image_paths):
        brightness, sharpness = calculate_image_features(path)
        
        # 밝기에 따른 분류
        if brightness < brightness_thresholds[0]:
            brightness_group = 'dark'
        elif brightness < brightness_thresholds[1]:
            brightness_group = 'balanced'
        else:
            brightness_group = 'bright'
            
        # 흐림 정도에 따른 분류
        if sharpness < sharpness_thresholds[0]:
            sharpness_group = 'fuzzy'
        elif sharpness < sharpness_thresholds[1]:
            sharpness_group = 'average'
        else:
            sharpness_group = 'sharp'
        
#         # 저장 경로 생성 및 이미지 저장
        save_path = os.path.join(base_save_path, f"{brightness_group}_{sharpness_group}")
        os.makedirs(save_path, exist_ok=True)
        save_file_path = os.path.join(save_path, os.path.basename(path))
        
        shutil.copy(path, save_file_path)
        # print(f"Saved {path} to {save_file_path}")
        # 분류 결과에 따라 딕셔너리에 추가
        classification_key = f"{brightness_group}_{sharpness_group}"
        if classification_key not in classification_results:
            classification_results[classification_key] = []
        classification_results[classification_key].append(path)
    
    # # 분류 결과를 txt 파일로 저장
    # for classification_key, paths in classification_results.items():
    #     save_file_path = os.path.join(base_save_path, f"{classification_key}.txt")
    #     os.makedirs(base_save_path, exist_ok=True)
        
    #     with open(save_file_path, 'w') as file:
    #         for path in paths:
    #             file.write(f"{path}\n")
    #     print(f"Saved classification results to {save_file_path}")

# 이미지 경로 리스트 로드
image_folder_path = "train/images"  # 이미지 폴더 경로 설정
image_paths = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.endswith('.jpg')]

# 분류된 이미지 정보 저장 경로
base_save_path = "10p_test"  # 분류된 이미지 정보를 저장할 기본 경로 설정

# 이미지 분류 및 정보 저장
classify_and_save_images(image_paths, base_save_path)

# # 이미지 경로 리스트 로드
# image_folder_path = "val/images"  # 이미지 폴더 경로 설정
# image_paths = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.endswith('.jpg')]



