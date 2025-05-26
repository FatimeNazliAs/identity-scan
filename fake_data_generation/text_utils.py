from PIL import Image, ImageDraw, ImageFont


def load_img():
    """
    Load the template image and initialize the drawing context.

    Opens a predefined image file to serve as the background for placing text 
    and returns an image object along with a drawing object.

    Returns
    -------
    tuple
        A tuple containing:
        - template_image : PIL.Image.Image
            The loaded image used as a template.
        - draw : PIL.ImageDraw.ImageDraw
            The drawing context used to place text on the image.
    """
    template_image = Image.open("fake_data_generation/template.jpg")
    draw = ImageDraw.Draw(template_image)
    return template_image, draw


def load_text_info():
    """
    Load text styling information including font, color, and alignment.

    Prepares the font style, fill color, and alignment for writing text 
    on the image template.

    Returns
    -------
    tuple
        A tuple containing:
        - fill : tuple
            RGB color value for the text (default black).
        - font : PIL.ImageFont.FreeTypeFont
            The font style and size used for rendering text.
        - align : str
            The alignment of the text ('left' by default).
    """
    font = ImageFont.truetype("fake_data_generation/Arial.ttf", 25)
    color = (0, 0, 0)
    fill = color
    align = "left"
    return fill, font, align


def load_texts_top_left_info():
    """
    Provide top-left coordinates for placing identity fields on the image.

    Returns the exact (x, y) pixel positions where the ID number, surname, 
    name, and birth date will be drawn on the template image.

    Returns
    -------
    tuple
        A tuple containing 4 (x, y) coordinate pairs for:
        - id_number
        - surname
        - name
        - birth_date
    """
    id_number_top_left = (30, 200)
    surname_top_left = (300, 250)
    name_top_left = (300, 320)
    birth_date_top_left = (300, 390)
    return id_number_top_left, surname_top_left, name_top_left, birth_date_top_left
