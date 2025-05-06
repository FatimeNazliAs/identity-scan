from image_utils import save, initialize_template
import os

if __name__ == "__main__":
    base_path = "fake_data_creation"
    img_folder = os.path.join(base_path, "synthetic_data", "images")
    txt_folder = os.path.join(base_path, "synthetic_data", "labels")

    os.makedirs(img_folder, exist_ok=True)
    os.makedirs(txt_folder, exist_ok=True)

    for index in range(11, 31):
        template_image, draw, fill, font, align = initialize_template()
        txt_file_path = os.path.join(txt_folder, f"{index}.txt").replace("\\", "/")
        img_file_path = os.path.join(img_folder, f"{index}.png").replace("\\", "/")

        save(txt_file_path, img_file_path, template_image, draw, fill, font, align)
