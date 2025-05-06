import torch
import numpy as np


def empty_like(x):
    """Creates empty torch.Tensor or np.ndarray with same shape as input and float32 dtype."""
    return (
        torch.empty_like(x, dtype=torch.float32)
        if isinstance(x, torch.Tensor)
        else np.empty_like(x, dtype=np.float32)
    )


def xyxy2xywh(x):
    """
    Convert bounding box coordinates from (x1, y1, x2, y2) format to (x, y, width, height) format where (x1, y1) is the
    top-left corner and (x2, y2) is the bottom-right corner.

    Args:
        x (np.ndarray | torch.Tensor): The input bounding box coordinates in (x1, y1, x2, y2) format.

    Returns:
        y (np.ndarray | torch.Tensor): The bounding box coordinates in (x, y, width, height) format.
    """
    assert (
        x.shape[-1] == 4
    ), f"input shape last dimension expected 4 but input shape is {x.shape}"
    y = empty_like(x)  # faster than clone/copy
    y[..., 0] = (x[..., 0] + x[..., 2]) / 2  # x center
    y[..., 1] = (x[..., 1] + x[..., 3]) / 2  # y center
    y[..., 2] = x[..., 2] - x[..., 0]  # width
    y[..., 3] = x[..., 3] - x[..., 1]  # height
    return y


def normalize_yolo_bbox_coordinates(img_size, yolo_box):
    """
    Normalize YOLO bounding box coordinates to be between 0 and 1.

    Parameters
    ----------
    img_size : tuple
        A tuple of (image_width, image_height).
    yolo_box : array-like
        Bounding box in YOLO format as [x_center, y_center, width, height] in pixel units.

    Returns
    -------
    np.ndarray
        Normalized bounding box as [x_center, y_center, width, height],
        where each value is between 0 and 1, rounded to 6 decimal places.

    Notes
    -----
    This function returns a new rounded NumPy array. The input is not modified in-place.
    """
    img_width, img_height = img_size
    yolo_box = np.array(yolo_box, dtype=np.float32)
    yolo_box[0] /= img_width  # x_center
    yolo_box[1] /= img_height  # y_center
    yolo_box[2] /= img_width  # width
    yolo_box[3] /= img_height  # height

    return yolo_box



