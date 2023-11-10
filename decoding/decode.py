from pyzbar.pyzbar import decode
from utils import crop_img
from abc import ABC, abstractmethod

class DecodeInterface(ABC):
    @abstractmethod
    def decode_p(self, input_img: str, bounding_boxes):
        pass

class DecodePyzbar(DecodeInterface):
    def decode_p(self, input_img: str, bounding_boxes):
        for i in bounding_boxes:
            cropped = crop_img(input_img, i)
            decoded = decode(cropped)
            print(decoded)
