import numpy as np

from pyzbar.pyzbar import decode

from barcode_detection.decoding.decode import Decoder
from barcode_detection.utils import crop_img


class DecodePyzbar(Decoder):

    def decode(self, input_img: np, bounding_boxes):
        codes = []
        for box in bounding_boxes:
            cropped = crop_img(input_img, box)
            decoded = decode(cropped)
            codes.append(decoded if decoded else None)
        return codes
