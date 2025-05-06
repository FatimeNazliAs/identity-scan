from PIL import Image, ImageDraw, ImageFont


def load_img():
    template_image = Image.open("fake_data_creation/template.jpg")
    draw = ImageDraw.Draw(template_image)
    return template_image, draw


def load_text_info():
    font = ImageFont.truetype("fake_data_creation/Arial.ttf", 25)
    color = (0, 0, 0)
    fill = color
    align = "left"
    return fill, font, align


def load_texts_top_left_info():
    id_number_top_left = (30, 200)
    surname_top_left = (300, 250)
    name_top_left = (300, 320)
    birth_date_top_left = (300, 390)
    return id_number_top_left, surname_top_left, name_top_left, birth_date_top_left
