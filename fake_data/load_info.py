from PIL import Image, ImageDraw, ImageFont
from faker import Faker


def load_fake_info():
    fake = Faker()
    fake_info_dict = {
        "id_number": fake.numerify("###########"),
        "surname": fake.name().split()[1],
        "name": fake.name().split()[0],
        "birth_date": str(fake.date_of_birth()).replace("-", "."),
    }

    for key, val in fake_info_dict.items():
        print(key, val)
    return fake_info_dict


def load_img():
    id_template = Image.open("fake_data/template.jpg")
    img = ImageDraw.Draw(id_template)
    return id_template, img


def load_text_info():
    font = ImageFont.truetype(r"fake_data/Arial.ttf", 25)
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
