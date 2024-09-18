import os

import cv2
import numpy as np

from barcode_detection.core.bounding_box import BoundingBox


def read_img(input_dir: str):
    img = cv2.imread(input_dir)
    return img


def crop_img(input_img: np.ndarray, rect: BoundingBox):
    cropped_image = input_img[rect.y1: rect.y1 + rect.y2, rect.x1: rect.x1 + rect.x2]
    return cropped_image


# for testing
def crop_helper(save_dir: str, input_dir: np.ndarray, bounding_boxes_path: str):
    with open(bounding_boxes_path, 'r') as f:
        for line in f:
            line = line.strip()
            coordinates = [int(num) for num in line.split(',')]
            print(coordinates)

            if len(coordinates) == 4:
                bbox = BoundingBox(*coordinates)  #распаковываем список в аргументы
            else:
                print(f"Found an error in line: {line}. Four integers expected, instead got {len(coordinates)}.")

            cropped = crop_img(input_dir, bbox)

            filename = f"{line}.jpg"
            filepath = os.path.join(save_dir, filename)
            cv2.imwrite(filepath, cropped)
