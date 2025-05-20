from faker import Faker


def create_fake_info():
    """
    Generate a dictionary of fake identity information for testing purposes.

    This function uses the Faker library to produce synthetic personal data 
    resembling identity card fields. The values include a randomly generated 
    Turkish-style ID number, surname, first name, and a birth date formatted 
    with periods instead of hyphens.

    Returns
    -------
    dict
        A dictionary containing the following keys:
        - 'id_number' : str
            A string of 11 digits representing a fake national ID number.
        - 'surname' : str
            A fake surname extracted from a randomly generated full name.
        - 'name' : str
            A fake first name extracted from a randomly generated full name.
        - 'birth_date' : str
            A birth date string in the format 'YYYY.MM.DD'.
    """
    fake = Faker()
    fake_info_dict = {
        "id_number": fake.numerify("###########"),
        "surname": fake.name().split()[1],
        "name": fake.name().split()[0],
        "birth_date": str(fake.date_of_birth()).replace("-", "."),
    }

    # for key, val in fake_info_dict.items():
    #     print(key, val)
    return fake_info_dict