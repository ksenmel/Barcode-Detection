from abc import ABC, abstractmethod

from barcode_detection.core.bounding_box import BoundingBox


class Localizer(ABC):
    """
       Class for Barcode Localization Algorithms
       `get_boundings` method takes as a path to a directory that contains deblurred video frames as an input.
       The output `List[List[BoundingBox]]` contains the coordinates of each detected barcode in each image
       within the directory.

    """

    @abstractmethod
    def get_boundings(self, input_dir: str) -> list[list[BoundingBox]]:
        pass
