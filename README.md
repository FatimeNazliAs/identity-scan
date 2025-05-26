# identity scan
 OCR Identity Card Scanner with FastAPI and Gradio


## Project Structure

This project is organized into several key directories and files to manage the application logic, data generation, and machine learning components.

---

### `app/`

This directory contains the core application logic, built with FastAPI and Gradio.

* `crud.py`: Handles **database Create, Read, Update, and Delete (CRUD) operations**.
* `database.py`: Manages **database connection and setup**.
* `gradio_ui.py`: Defines the **Gradio Blocks user interface**.
* `inference.py`: Contains the **model inference logic**.
* `schemas.py`: Defines **data schemas and validation rules**.
* `main.py`: The **main entry point for the FastAPI application**, including Gradio UI mounting.
* `models.py`: Defines the **database models**.

---

### `fake_data_generation/`

This directory houses scripts and utilities for generating synthetic identity card data.

* `bbox_utils.py`: Utilities for **bounding box calculations**.
* `faker_utils.py`: Helper functions utilizing the **Faker library for data generation**.
* `generate_sample.py`: The **main script for generating synthetic identity card images and labels**.
* `image_utils.py`: Utilities for **image manipulation**.
* `text_utils.py`: Helper functions for **text rendering on images**.
* `txt_utils.py`: Utilities for **handling text files**.
* `template.jpg`: The **template image** used for generating synthetic identity cards.
* `Arial.ttf`: The **font file** used for rendering text on the synthetic images.

---

### `fake_generated_data/`

This folder is where the **generated synthetic data (images and labels) are saved** after running `generate_sample.py`.

---

### `images/`

Contains the **dataset images for YOLO training and validation**.

* `train/`: Training images.
* `val/`: Validation images.

---

### `labels/`

Contains the **YOLO format label text files** corresponding to the images in the `images/` directory.

* `train/`: Training labels.
* `val/`: Validation labels.

---

### Root Files

* `classes.txt`: Defines the **object classes** for YOLO model training.
* `requirements.txt`: Lists all **Python dependencies** required for the project.
* `sample.png`: An **example output image** or sample result.

## Synthetic Data Generation

Initially, synthetic identity card images and labels were created manually using `template.jpg` and the Faker library. Roughly 10 examples were labeled with LabelImg, but this method proved too time-consuming.

To automate this process, scripts have been developed and are located in the `fake_data_generation/` folder.

---

### How to Generate Synthetic Data

1.  Run the following script to generate synthetic identity card images and their corresponding YOLO labels:

    ```bash
    python fake_data_generation/generate_sample.py
    ```

    You can modify the number of generated samples by adjusting the `range` parameters within the script.

    This will create a `synthetic_data/` folder inside `fake_data_generation/`, containing:

    * `images/`: synthetic identity card images
    * `labels/`: YOLO-format label text files

---

### After Data Generation

Open `fake_generated_data/` folder in the project root. Inside, open the `images/` and `labels/` folders. Both of these should contain `train/` and `val/` subfolders.

Manually cut and paste the generated images and label files from `fake_data_generation/synthetic_data/` into the appropriate `train/` and `val/` folders under `fake_generated_data/`.

This dataset structure is now ready for training your YOLO model.

---

**Note:** If you prefer not to run the generation script yourself, a sample dataset is already available in the `fake_generated_data/` folder of this repository. You can use it directly for training or testing.