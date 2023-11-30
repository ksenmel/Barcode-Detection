import cv2
import numpy as np

from barcode_detection.core.bounding_box import BoundingBox


def read_img(input_dir: str):
    img = cv2.imread(input_dir)
    return img


def crop_img(input_img: np.ndarray, rect: BoundingBox):
    cropped_image = input_img[
        rect.y : rect.y + rect.height, rect.x : rect.x + rect.width
    ]
    return cropped_image
