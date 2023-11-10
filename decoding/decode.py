from pyzbar.pyzbar import decode
from utils import crop_img


# pyzbar
def decode_pyzbar(input_img: str, bounding_boxes):
    for i in bounding_boxes:
        cropped = crop_img(input_img, i)
        decoded = decode(cropped)

        print(decoded)
