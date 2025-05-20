import os
from fastapi import UploadFile
import json
from .models import IdentityCard
from datetime import date, datetime
from .inference import extract_inference


def create_upload_directory():
    """
    Create the upload directory if it does not exist.

    Constructs the path to the upload directory (app/upload_file), creates
    it if necessary, and returns the path.

    Returns
    -------
    str
        Absolute or relative path to the upload directory.
    """
    file_dir = os.path.join("app", "upload_file")
    isExist = os.path.exists(file_dir)
    if not isExist:
        os.makedirs(file_dir, exist_ok=True)
    return file_dir


def delete_existing_png_files(file_dir):
    """
    Delete all PNG files in the specified directory.

    Searches the given directory and removes files with the `.png` extension
    to ensure no conflicting images remain before new uploads.

    Parameters
    ----------
    file_dir : str
        Path to the directory containing uploaded files.

    Returns
    -------
    None
    """

    for filename in os.listdir(file_dir):
        if filename.endswith(".png"):
            os.remove(os.path.join(file_dir, filename))


def save_uploaded_file(file: UploadFile, file_dir):
    """
    Save uploaded file to disk.

    Parameters
    ----------
    file : UploadFile
        The uploaded file from FastAPI.


    Returns
    -------
    str
        The file path where the uploaded file was saved.
    """

    file_path = os.path.join(file_dir, file.filename).replace("\\", "/")

    with open(file_path, "wb") as sample_file:
        sample_file.write(file.file.read())

    return file_path


def get_latest_path(file_type: str = "image", save_dir: str = "app/upload_file") -> str:
    """
    Get the full path of the latest uploaded file based on type.

    Parameters
    ----------
    file_type : str
        Type of file to look for: "image" or "json". Default is "image".
    save_dir : str
        Directory where files are saved.

    Returns
    -------
    str
        Full path to the first matching file.
    """
    ext_map = {"image": ".png", "json": ".json"}

    if file_type not in ext_map:
        raise ValueError("file_type must be either 'image' or 'json'")

    file_extension = ext_map[file_type]
    file = [f for f in os.listdir(save_dir) if f.endswith(file_extension)]

    if not file:
        raise FileNotFoundError(f"No {file_extension} files found in {save_dir}")

    return os.path.join(save_dir, file[0]).replace("\\", "/")


def save_inference_result_to_json(result, json_file_path):
    """
    Save the inference result to a JSON file.

    Parameters
    ----------
    result : dict
        The dictionary containing extracted text.

    """
    # json_file_path = os.path.join(save_dir, "inference_result.json").replace("\\", "/")
    with open(json_file_path, "w+") as f:
        json.dump(result, f)


def load_json_file(json_file_path):
    """
    Load json file to save data into database.

    Parameters
    ----------
    json_file_path : str
        The file path where json file was saved.

    Returns
    -------
    dict
        The dictionary containing inference result data.
    """
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return data


def save_identity_card_from_json():
    """
    Save inference results from a JSON file to an IdentityCard object.

    Loads data from the most recent `inference_result.json` file and converts it
    into an `IdentityCard` ORM object (not yet committed to the database).

    Returns
    -------
    IdentityCard
        A SQLAlchemy IdentityCard object containing the parsed inference result data.
    """
    json_path = get_latest_path(file_type="json")
    data = load_json_file(json_path)

    date_format = "%Y-%m-%d"
    identity_card = IdentityCard(
        identity_number=data["identity_number"],
        surname=data["surname"],
        name=data["name"],
        birth_date=datetime.strptime(data["birth_date"], date_format),
        created_at=date.today(),
    )
    return identity_card


def show_inference_result():
    """
    Run inference on the latest uploaded image and extract identity information.

    Returns
    -------
    dict
        Dictionary containing extracted identity fields:
        'identity_number', 'surname', 'name', and 'birth_date'.
    """
    image_path = get_latest_path(file_type="image")

    crop_output_dir = "identity-scan/crops"
    extracted_texts = extract_inference(image_path, crop_output_dir)

    result = {
        "identity_number": extracted_texts["id_number"],
        "surname": extracted_texts["surname"],
        "name": extracted_texts["name"],
        "birth_date": extracted_texts["birth_date"].replace(".", "-"),
    }
    return result


def create_json_file(save_dir):
    json_file_path = os.path.join(save_dir, "inference_result.json").replace("\\", "/")
    return json_file_path


def delete_content_in_json(json_file_path):
    with open(json_file_path, "r+") as f:
        f.seek(0)
        f.truncate()
