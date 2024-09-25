import cv2
import numpy as np
import os

from barcode_detection.core.bounding_box import BoundingBox


def crop(image: np.ndarray, rect: BoundingBox):
    if rect is not None:
        cropped = image[rect.y1: rect.y1 + rect.y2, rect.x1: rect.x1 + rect.x2]
        return cropped
    else:
        return None


def crop_image(save_dir: str, images_dir: str, bounding_boxes_path: str):
    images = os.listdir(images_dir)
    bounding_boxes = os.listdir(bounding_boxes_path)

    if len(images) != len(bounding_boxes):
        raise ValueError("Number of bounding boxes files is not equal to number of images.")

    for i in range(len(images)):
        image = cv2.imread(images_dir + '/' + images[i])
        with open(bounding_boxes_path + '/' + bounding_boxes[i], "r") as f:
            for line in f:
                line = line.strip()
                coordinates = [int(num) for num in line.split(",")]

                if len(coordinates) == 4:
                    bbox = BoundingBox(*coordinates)

                    cropped = crop(image, bbox)

                    s = line.replace(" ", "").replace(",", "")
                    filename = f"{i}_{s}.jpg"

                    filepath = os.path.join(save_dir, filename)
                    cv2.imwrite(filepath, cropped)

                else:
                    raise ValueError(
                        f"Found an error in line: {line}. Four integers expected, instead got {len(coordinates)}.")
