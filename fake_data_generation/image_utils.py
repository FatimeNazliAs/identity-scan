from text_utils import load_img, load_text_info, load_texts_top_left_info
from faker_utils import create_fake_info
from bbox_utils import (
    xyxy2xywh,
    normalize_yolo_bbox_coordinates,
)
import numpy as np
from txt_utils import save_yolo_labels_to_txt


def initialize_template():
    """
    Initialize the template image and draw object, as well as text info.

    Returns
    -------
    tuple
        A tuple containing the template image, draw object, fill color, font, and text alignment.
    """
    fill, font, align = load_text_info()
    template_image, draw = load_img()
    return template_image, draw, fill, font, align


def write_text_to_draw(draw, top_left_coordinates, text, fill, font, align):
    """
    Write text on the image using the provided draw object.

    Parameters
    ----------
    draw : ImageDraw.Draw
        The draw object used to draw text on the image.
    top_left_coordinates : tuple
        Coordinates (x, y) for the top-left position of the text.
    text : str
        The text to be written on the image.
    fill : tuple
        The color used to fill the text.
    font : ImageFont
        The font used to display the text.
    align : str
        The alignment of the text.

    Returns
    -------
    ImageDraw.Draw
        The draw object with the text written on the image.
    """

    draw.text(
        top_left_coordinates,
        text,
        fill=fill,
        font=font,
        align=align,
    )

    return draw


def draw_bbox(draw, top_left_coordinates, text, font):
    """
    Draw a bounding box around the text on the image.

    Parameters
    ----------
    draw : ImageDraw.Draw
        The draw object used to draw the bounding box.
    top_left_coordinates : tuple
        Coordinates (x, y) for the top-left position of the text.
    text : str
        The text to be used for bounding box calculation.
    font : ImageFont
        The font used to display the text.

    Returns
    -------
    tuple
        The coordinates of the bounding box (x1, y1, x2, y2).
    """
    bbox = draw.textbbox(top_left_coordinates, text, font=font)
    return bbox


def add_label_to_bbox(bbox_coordinate, label):
    """
    Add a label to the bounding box coordinates.

    Parameters
    ----------
    bbox_coordinate : list
        The bounding box coordinates (x1, y1, x2, y2).
    label : int
        The label to be added to the bounding box.

    Returns
    -------
    list
        The bounding box coordinates with the label added at the start.
    """

    bbox_coordinate = bbox_coordinate.tolist()
    bbox_coordinate.insert(0, label)
    return bbox_coordinate


def generate_labeled_yolo_bbox(
    draw, top_left_coordinates, text, bbox_label, template_image, fill, font, align
):
    """
    Generate YOLO-formatted labeled bounding box with text on the image.

    This function writes the text on the image at the given coordinates, calculates the bounding box
    around the text, converts it to YOLO format, normalizes the coordinates according to the image size,
    and appends the label to the coordinates. The result is a list of coordinates in YOLO format, which
    includes the label at the beginning.

    Parameters
    ----------
    draw : ImageDraw.Draw
        The draw object used to write the text.
    top_left_coordinates : tuple
        Coordinates (x, y) for the top-left position of the text.
    text : str
        The text to be written on the image.
    bbox_label : int
        The label for the bounding box.
    template_image : PIL.Image
        The template image on which the bounding box is drawn.
    fill : tuple
        The color used for the text.
    font : ImageFont
        The font used for the text.
    align : str
        The alignment of the text.

     Returns
    -------
    list
        A list of YOLO-formatted coordinates representing the labeled bounding box. The format is
        `[label, x_center, y_center, width, height]`, where:
            - label: The label for the bounding box (integer).
            - x_center: The x-coordinate of the center of the bounding box (float).
            - y_center: The y-coordinate of the center of the bounding box (float).
            - width: The width of the bounding box (float).
            - height: The height of the bounding box (float).
    """

    text_on_draw = write_text_to_draw(
        draw, top_left_coordinates, text, fill, font, align
    )
    bbox = draw_bbox(
        text_on_draw, top_left_coordinates=top_left_coordinates, info=text, font=font
    )
    yolo_bbox_coordinate = xyxy2xywh(np.array(bbox))
    norm_yolo_bbox_coordinate = normalize_yolo_bbox_coordinates(
        template_image.size, yolo_bbox_coordinate
    )

    labeled_yolo_bbox_coordinate = add_label_to_bbox(
        norm_yolo_bbox_coordinate, bbox_label
    )

    return labeled_yolo_bbox_coordinate


def process_draw(draw, template_image, fill, font, align):
    """
    Process the drawing of text and bounding boxes on the template image.

    This function generates fake personal information (e.g., id_number, surname, name, birth_date)
    using the `create_fake_info` function, and then calculates the corresponding bounding box
    coordinates for each text field. It returns a list of YOLO coordinates with labels that
    can be used for object detection tasks.

    Parameters
    ----------
    draw : ImageDraw.Draw
        The draw object used to draw the text and bounding boxes on the image.
    template_image : PIL.Image
        The image on which the text and bounding boxes will be drawn.
    fill : tuple
        The color used for the text to be written on the image. Typically, a tuple of RGB values.
    font : ImageFont
        The font object to be used for the text.
    align : str
        The text alignment. The available alignment values are usually "left", "center", or "right".

    Returns
    -------
    list
        A list of YOLO-formatted bounding box coordinates with labels. Each entry in the list is a
        list of the format `[label, x_center, y_center, width, height]`, representing a bounding box
        for each text field.
    """

    fake_info_dict = create_fake_info()

    id_number_top_left, surname_top_left, name_top_left, birth_date_top_left = (
        load_texts_top_left_info()
    )

    text_fields = [
        ("id_number", id_number_top_left, 0),
        ("surname", surname_top_left, 1),
        ("name", name_top_left, 2),
        ("birth_date", birth_date_top_left, 3),
    ]

    yolo_coordinates = [
        generate_labeled_yolo_bbox(
            draw,
            coords,
            fake_info_dict[field],
            label,
            template_image,
            fill,
            font,
            align,
        )
        for field, coords, label in text_fields
    ]
    return yolo_coordinates


def save_template_image(template_image, img_file_path):
    """
    Save the template image to the specified file path.

    Parameters
    ----------
    template_image : PIL.Image
        The image to be saved.
    img_file_path : str
        The path where the image will be saved.

    Returns
    -------
    None
    """
    template_image.save(img_file_path)


def save(txt_file_path, img_file_path, template_image, draw, fill, font, align):
    """
    Save the generated template image and corresponding YOLO labels to specified paths.

    This function processes the template image by writing text information and calculating the bounding box
    coordinates for each field. The corresponding YOLO labels are saved to a text file, while the image with
    the drawn text is saved to an image file. The YOLO labels are written in the format expected by object detection models.

    Parameters
    ----------
    txt_file_path : str
        Path to save the YOLO label file containing bounding box coordinates.
    img_file_path : str
        Path to save the image with text and bounding boxes.
    template_image : PIL.Image
        The image on which text and bounding boxes will be drawn.
    draw : ImageDraw.Draw
        The object used to draw text and bounding boxes on the image.
    fill : tuple
        The color for the text.
    font : ImageFont
        The font used for the text.
    align : str
        The text alignment.

    Returns
    -------
    None
        This function does not return any value. It performs the task of saving the modified image and the
        corresponding YOLO label file.
    
    Notes
    -----
    - The function calls `process_draw` to draw the text on the image and to calculate the YOLO bounding box
      coordinates for each piece of text.
    - The YOLO label file is created using `save_yolo_labels_to_txt`, which writes the bounding box coordinates
      to a text file in YOLO format.
    - The template image with text is saved as an image file  at the specified `img_file_path`.
    """
    yolo_coordinates = process_draw(draw, template_image, fill, font, align)
    save_yolo_labels_to_txt(yolo_coordinates, txt_file_path)
    save_template_image(template_image, img_file_path)


if __name__ == "__main__":

    # fill, font, align = load_text_info()
    # template_image, draw = load_img()
    # save(txt_file_path, img_file_path,template_image, draw, fill, font, align)
    pass
