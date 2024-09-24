import cv2

from pathlib import Path
from pyzbar.pyzbar import decode

if __name__ == "__main__":
    images = Path("/workspace/images")
    barcodes = Path("/workspace/barcodes/decoded_barcodes.txt")

    barcodes_unique = {}

    with open(barcodes, "w") as file:
        for image in images.iterdir():
            if image.is_file():
                np_image = cv2.imread(str(image))
                decoded = decode(np_image)

                for code in decoded:
                    value = code.data.decode("utf-8")

                    if value:
                        if value in barcodes_unique:
                            barcodes_unique[value] += 1
                        else:
                            barcodes_unique[value] = 1

                        file.write(f"{value}\n")


