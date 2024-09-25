import zxing

from pathlib import Path
from PIL import Image

if __name__ == "__main__":
    images = Path("/workspace/images")
    barcodes = Path("/workspace/barcodes/decoded_barcodes.txt")

    barcodes_unique = {}

    reader = zxing.BarCodeReader()

    with open(barcodes, "w") as file:
        for image in images.iterdir():
            if image.is_file():
                barcode = reader.decode(str(image))
                value = barcode.raw

                if value:
                    if value in barcodes_unique:
                        barcodes_unique[value] += 1
                    else:
                        barcodes_unique[value] = 1

                    file.write(f"{value}\n")
