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