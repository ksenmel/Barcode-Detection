from abc import ABC, abstractmethod
import numpy as np


class Localizer(ABC):
    @abstractmethod
    def get_boundings(self, input_img: np):
        pass
