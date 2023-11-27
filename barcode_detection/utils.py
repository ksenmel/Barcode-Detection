import cv2
import numpy as np

from barcode_detection.boundingbox.bounding_box import BoundingBox
from pathlib import Path

def get_dir():
    current_file = Path(__file__).resolve()
    barcode_detection_path = current_file.parents[1]
    return barcode_detection_path



def read_img(input_dir: str):
    img = cv2.imread(input_dir)
    return img


def crop_img(input_img: np.ndarray, rect: BoundingBox):
    cropped_image = input_img[
                    rect.y: rect.y + rect.height, rect.x: rect.x + rect.width
                    ]
    return cropped_image
