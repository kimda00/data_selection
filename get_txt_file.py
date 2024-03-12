import os

def save_image_name_from_folder(folder_path, save_file, new_base):
    image_name = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    with open(save_file, 'w') as file:
        for img_name in image_name:
            new_path = os.path.join(new_base, img_name)
            file.write(new_path + '\n')

if __name__ == "__main__":
    # folder_path = "local_path/datasets/trafficlight/val/images"
    folder_path = "val/images"
    save_file = "val.txt"
    new_base = "./"
    save_image_name_from_folder(folder_path, save_file, new_base)
