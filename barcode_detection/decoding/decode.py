import numpy as np

from abc import ABC, abstractmethod
from barcode_detection.boundingbox.bounding_box import BoundingBox


class Decoder(ABC):
    @abstractmethod
    def decode(self, input_img: np.ndarray, bounding_boxes: list[BoundingBox]) -> list[list[str] | None]:
        pass
