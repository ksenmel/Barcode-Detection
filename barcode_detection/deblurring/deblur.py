from abc import ABC, abstractmethod


class Deblurrer(ABC):
    @abstractmethod
    def deblur(self, path_to_video: str):
        pass
