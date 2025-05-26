def save_yolo_labels_to_txt(yolo_coordinates, txt_file_path):
    """
    Save YOLO format coordinates to a text file.

    This function takes a list of YOLO coordinates and writes them to a specified text file. Each line in the
    text file corresponds to one set of YOLO coordinates, where the first value is the label, and the remaining
    values are the normalized coordinates of the bounding box, rounded to six decimal places.

    Parameters
    ----------
    yolo_coordinates : list of list of floats
        A list where each element is a list representing one bounding box in YOLO format. The first element
        is the label (integer), followed by the normalized x_center, y_center, width, and height.

    txt_file_path : str
        The path where the text file containing the YOLO labels will be saved.

    Returns
    -------
    None
        The function writes the labels directly to the specified text file. If the file already exists, it will
        be overwritten.
    """
    with open(txt_file_path, "w") as fp:
        for coordinate in yolo_coordinates:
            # Ensure label (first value) is an integer, and the rest are floats rounded to 6 decimals
            label = int(coordinate[0])  # Convert label to integer
            rounded_coordinates = [
                f"{coor:.6f}" if idx > 0 else str(label)
                for idx, coor in enumerate(coordinate)
            ]

            line = " ".join(
                rounded_coordinates
            )  # Join the values with a space separator
            fp.write(line + "\n")
