from abc import ABC, abstractmethod
import numpy as np


class Decoder(ABC):
    @abstractmethod
    def decode(self, input_img: np, bounding_boxes):
        pass
