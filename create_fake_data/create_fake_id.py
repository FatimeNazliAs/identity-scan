from PIL import Image, ImageDraw, ImageFont
from faker import Faker


def create_fake_info():
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


if __name__ == "__main__":
    fake_info_dict = create_fake_info()

    id_template = Image.open("create_fake_data/template.jpg")

    id_number_top_left = (30, 200)
    surname_top_left = (300, 250)
    name_top_left = (300, 320)
    birth_date_top_left = (300, 390)

    img = ImageDraw.Draw(id_template)
    font = ImageFont.truetype(r"create_fake_data/Arial.ttf", 25)
    img.text(
        id_number_top_left,
        fake_info_dict["id_number"],
        fill=(0, 0, 0),
        font=font,
        align="left",
    )
    img.text(
        surname_top_left,
        fake_info_dict["surname"],
        fill=(0, 0, 0),
        font=font,
        align="left",
    )
    img.text(
        name_top_left, fake_info_dict["name"], fill=(0, 0, 0), font=font, align="left"
    )
    img.text(
        birth_date_top_left,
        str(fake_info_dict["birth_date"]),
        fill=(0, 0, 0),
        font=font,
        align="left",
    )

    id_template.show()
