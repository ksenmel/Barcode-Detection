from barcode_detection.decoding.decode import Decoder
from pyzbar.pyzbar import decode
from barcode_detection.utils import crop_img
import numpy as np


class DecodePyzbar(Decoder):

    def decode(self, input_img: np, bounding_boxes):
        for i in bounding_boxes:
            cropped = crop_img(input_img, i)
            decoded = decode(cropped)
            print(decoded)
