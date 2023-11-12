from decoding.decode import Decoder
from pyzbar.pyzbar import decode
from utils import crop_img


class DecodePyzbar(Decoder):
    def decode(self, input_img: str, bounding_boxes):
        for i in bounding_boxes:
            cropped = crop_img(input_img, i)
            decoded = decode(cropped)
            print(decoded)
