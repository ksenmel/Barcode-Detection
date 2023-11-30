# describes the bounding box coordinates
class BoundingBox:
    """
    Class for storing coordinates of bounding box.
    'x', 'y' coordinates are bottom left corner coordinates,
    'width', 'height' coordinates are top right corner coordinates
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
