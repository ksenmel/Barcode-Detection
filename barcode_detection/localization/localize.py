from abc import ABC, abstractmethod


class Localizer(ABC):
    """
    Class for Barcode Localization Algorithms
    `get_boundings` method takes a directory that contains deblurred video frames as an input.
    """

    @abstractmethod
    def get_boundings(self, images: str):
        pass
