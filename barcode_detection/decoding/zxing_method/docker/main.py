import zxing

from pathlib import Path
from PIL import Image

if __name__ == "__main__":
    img_folder = "/workspace/img"
    folder_path = Path(img_folder)
    output_file = "/workspace/barcodes/decoded_barcodes.txt"

    reader = zxing.BarCodeReader()

    with open(output_file, "w") as file:
        codes = []
        for img in folder_path.iterdir():
            if img.is_file():
                barcode = reader.decode(str(img))
                codes.append(str(barcode.raw))

        file.write("\n".join(codes))
