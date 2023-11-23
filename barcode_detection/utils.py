import cv2
import os
import numpy as np

from barcode_detection.boundingbox.bounding_box import BoundingBox


def get_dir():
    current_file = os.path.abspath(__file__)
    components = current_file.split(os.path.sep)

    barcode_detection_index = components.index("Barcode-Detection")
    barcode_detection_path = os.path.sep.join(components[:barcode_detection_index + 1])

    return barcode_detection_path


def read_img(input_dir: str):
    img = cv2.imread(input_dir)
    return img


def crop_img(input_img: np.ndarray, rect: BoundingBox):
    cropped_image = input_img[
                    rect.y: rect.y + rect.height, rect.x: rect.x + rect.width
                    ]
    return cropped_image
