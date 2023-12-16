# describes the bounding box coordinates
class BoundingBox:
    """
    Class for storing coordinates of bounding box.
    'x1', 'y1' coordinates are bottom left corner coordinates,
    'x2', 'y2' coordinates are top right corner coordinates
    """

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
