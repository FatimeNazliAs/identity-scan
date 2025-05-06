
def save_yolo_labels_to_txt(yolo_coordinates, txt_file_path):
    with open(txt_file_path, "x") as fp:
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
