import numpy as np

from pyzbar.pyzbar import decode

from barcode_detection.boundingbox.bounding_box import BoundingBox
from barcode_detection.decoding.decode import Decoder
from barcode_detection.utils import crop_img


class DecodePyzbar(Decoder):

    def decode(self, input_img: np.ndarray, bounding_boxes: list[BoundingBox]) :
        codes = []
        for box in bounding_boxes:
            cropped = crop_img(input_img, box)
            decoded = decode(cropped)

            data_values = [code.data.decode("utf-8") for code in decoded]
            codes.append(data_values if data_values else None)

        return codes
