from typing import List

import cv2
import os
import numpy as np
from boundingbox.BoundingBox import BoundingBox


def read_img(input_dir: str):
    img = cv2.imread(input_dir)
    return img


def crop_img(input_img: np, rect: BoundingBox):
    cropped_image = input_img[rect.y:rect.y + rect.height, rect.x:rect.x + rect.width]
    return cropped_image


def crop_helper(save_dir: str, input_dir: np, bounding_boxes: List[BoundingBox]):
    for i in range(len(bounding_boxes)):
        cropped = crop_img(input_dir, bounding_boxes[i])
        filename = f"img_{i}.jpg"
        filepath = os.path.join(save_dir, filename)
        cv2.imwrite(filepath, cropped)
