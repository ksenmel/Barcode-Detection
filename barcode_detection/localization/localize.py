import numpy as np

from abc import ABC, abstractmethod
from barcode_detection.boundingbox.bounding_box import BoundingBox


class Localizer(ABC):
    @abstractmethod
    def get_boundings(self, input_img: np.ndarray) -> list[BoundingBox]:
        pass
