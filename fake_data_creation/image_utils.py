from text_utils import load_img, load_text_info, load_texts_top_left_info
from faker_utils import create_fake_info
from bbox_utils import (
    xyxy2xywh,
    normalize_yolo_bbox_coordinates,
)
import numpy as np
from txt_utils import save_yolo_labels_to_txt


def write_text_to_draw(draw, top_left_coordinates, info, fill, font, align):

    draw.text(
        top_left_coordinates,
        info,
        fill=fill,
        font=font,
        align=align,
    )

    return draw


def initialize_template():
    fill, font, align = load_text_info()
    template_image, draw = load_img()
    return template_image, draw, fill, font, align


def save_template_image(template_image, img_file_path):
    template_image.save(img_file_path)


def draw_bbox(draw, top_left_coordinates, info, font):
    bbox = draw.textbbox(top_left_coordinates, info, font=font)
    return bbox


def add_label_to_bbox(bbox_coordinate, label):
    bbox_coordinate = bbox_coordinate.tolist()
    bbox_coordinate.insert(0, label)
    return bbox_coordinate


def generate_labeled_yolo_bbox(
    draw, top_left_coordinates, text, bbox_label, template_image, fill, font, align
):
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


def save(txt_file_path, img_file_path, template_image, draw, fill, font, align):
    yolo_coordinates = process_draw(draw, template_image, fill, font, align)
    save_yolo_labels_to_txt(yolo_coordinates, txt_file_path)
    save_template_image(template_image, img_file_path)


if __name__ == "__main__":

    # fill, font, align = load_text_info()
    # template_image, draw = load_img()
    # save(txt_file_path, img_file_path,template_image, draw, fill, font, align)
    pass
