from ultralytics import YOLO
import easyocr
import os


def train_model():
    """
    Build and return a YOLO model initialized from a YAML config and pretrained weights.

    Returns
    -------
    YOLO
        A YOLO model ready for training.
    """
    model = YOLO("yolo11n.yaml").load("yolo11n.pt")
    model.train(data="dataset.yaml", epochs=200, device="cuda", augment=True)
    return model


def load_model():
    """
    Load the trained YOLO model from the best weights.

    Returns
    -------
    YOLO
        A YOLO model loaded with trained weights.
    """
    model = YOLO("runs/detect/train/weights/best.pt")
    return model


def detect_image(image_path, model):
    """
    Run YOLO object detection on the input image.

    Parameters
    ----------
    image_path : str
        Path to the input image.
    model : YOLO
        The YOLO model instance to use for detection.

    Returns
    -------
    list
        YOLO detection results.
    """
    results = model(image_path)
    return results


def validate_model(model):
    """
    Run validation on the YOLO model and print mAP metrics.

    Parameters
    ----------
    model : YOLO
        The YOLO model instance to validate.
    """
    metrics = model.val()
    print(metrics.box.maps)


def save_crops(results, output_dir):
    """
    Save cropped images of detected objects to a specified folder.

    Parameters
    ----------
    results : list
        YOLO detection results.
    output_dir : str
        Directory where cropped images will be saved.
    """
    results[0].save_crop(output_dir)


def apply_ocr(crop_dir, delete_after=True):
    """
    Apply EasyOCR to cropped images and extract text from identity fields.

    Parameters
    ----------
    crop_dir : str
        Path to the directory containing cropped image folders (e.g., 'name/im.jpg').
    delete_after : bool, optional
        Whether to delete the cropped image after extracting text. Default is True.

    Returns
    -------
    dict
        A dictionary where keys are field labels (e.g., 'name', 'birth_date') and values are extracted text strings.

    Notes
    -----
    - Uses EasyOCR with Turkish and English language support.
    - Expects each cropped field to be located at `crop_dir/field_label/im.jpg`.
    - If a label image does not exist or OCR fails, assigns an empty string.
    - Optionally deletes the cropped images after OCR to reduce disk usage or protect sensitive data.
    """

    reader = easyocr.Reader(["tr", "en"])
    text_labels = ["birth_date", "id_number", "name", "surname"]
    extracted_texts = {}

    for label in text_labels:
        label_path = os.path.join(crop_dir, label, "im.jpg")
        if os.path.exists(label_path):
            result = reader.readtext(label_path)
            extracted_texts[label] = result[0][1] if result else ""
            if delete_after:
                os.remove(label_path)
        else:
            extracted_texts[label] = ""

    return extracted_texts



def workflow(image_path, crop_output_dir):
    """
    Full pipeline: load model, detect fields, crop, apply OCR, and print results.

    Parameters
    ----------
    image_path : str
        Path to the identity image to process.
    crop_output_dir : str
        Directory to store cropped fields.

    Returns
    -------
    dict
        Final extracted OCR results.
    """
    model = load_model()
    results = detect_image(image_path, model)
    save_crops(results, crop_output_dir)
    extracted_texts = apply_ocr(crop_output_dir)
    print(extracted_texts)
    return extracted_texts


text_labels = ["birth_date", "id_number", "name", "surname"]
workflow("sample.png", "crops")
