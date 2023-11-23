import os
import zxing

from PIL import Image

path = "/workspace/tmp_for_img"

def imgs(folder):
    images = []
    for filename in os.listdir(folder):
        img = Image.open(os.path.join(folder, filename))
        images.append(img)
    return images


images = imgs(path)
reader = zxing.BarCodeReader()


def decode(cropped):
    decoded = []

    for img in cropped:
        barcode = reader.decode(img)
        decoded.append(barcode.raw)

    return decoded


decoded = decode(images)
print(decoded)
