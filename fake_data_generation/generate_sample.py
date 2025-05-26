
"""
This script generates synthetic data consisting of labeled images and corresponding YOLO label files.

The script initializes the template image and draws fake information (e.g., ID number, name, surname, birth date) 
on the image, then saves the image and its corresponding YOLO bounding box label file.

Steps:
1. Creates necessary directories for saving images and labels.
2. Iterates over a specified range (from 11 to 30) to generate labeled images and their YOLO labels.
3. For each iteration, it initializes a template image, draws text on it, calculates bounding box coordinates, 
   and saves both the image and label file.

Parameters:
- `base_path`: The root directory where the synthetic data will be stored.
- `img_folder`: Folder to save generated images.
- `txt_folder`: Folder to save YOLO label files.

The resulting dataset will be used for training object detection.
"""

from image_utils import save, initialize_template
import os

if __name__ == "__main__":
    base_path = "fake_data_generation"
    # I first opened those img_folder and txt_folder and after that 
    # I copied them into app/fake_generated_data folder, divided them into train and val sets.
    img_folder = os.path.join(base_path, "synthetic_data", "images")
    txt_folder = os.path.join(base_path, "synthetic_data", "labels")

    os.makedirs(img_folder, exist_ok=True)
    os.makedirs(txt_folder, exist_ok=True)

    # As I created first 10 images and labels myself, I continued with 11-102 to create rest 90 images.
    # You can change range between how many images and labels you want.
    for index in range(11, 101):
        template_image, draw, fill, font, align = initialize_template()
        txt_file_path = os.path.join(txt_folder, f"{index}.txt").replace("\\", "/")
        img_file_path = os.path.join(img_folder, f"{index}.png").replace("\\", "/")

        save(txt_file_path, img_file_path, template_image, draw, fill, font, align)
