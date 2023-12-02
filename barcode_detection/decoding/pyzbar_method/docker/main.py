import cv2
from pyzbar.pyzbar import decode
from pathlib import Path

if __name__ == "__main__":
    img_folder = "/workspace/img"
    folder_path = Path(img_folder)
    output_file = "/workspace/boxes/decoded_barcodes.txt"

    with open(output_file, "w") as file:
        codes = []
        for img in folder_path.iterdir():
            if img.is_file():
                np_image = cv2.imread(str(img))
                decoded = decode(np_image)

                data_values = [code.data.decode("utf-8") for code in decoded]
                codes.append(str(data_values if data_values else None))

        file.write("\n".join(codes))
