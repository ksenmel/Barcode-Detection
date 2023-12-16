import cv2
import numpy as np

from barcode_detection.core.bounding_box import BoundingBox


def read_img(input_dir: str):
    img = cv2.imread(input_dir)
    return img


def crop_img(input_img: np.ndarray, rect: BoundingBox):
    cropped_image = input_img[rect.y1 : rect.y1 + rect.y2, rect.x1 : rect.x1 + rect.x2]
    return cropped_image
