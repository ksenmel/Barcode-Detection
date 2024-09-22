from abc import ABC, abstractmethod


class Decoder(ABC):
    @abstractmethod
    def decode(
        self, images_dir: str, bounding_boxes_dir: str
    ):
        pass
