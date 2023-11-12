from abc import ABC, abstractmethod


class Localizer(ABC):
    @abstractmethod
    def localize(self, input_img: str, bounding_boxes):
        pass
