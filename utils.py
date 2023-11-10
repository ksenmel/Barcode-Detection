import cv2
from boundingbox.BoundingBox import BoundingBox
import os


def read_img(input_dir: str):
    img = cv2.imread(input_dir)
    return img


def crop_img(input_dir: str, rect: BoundingBox):
    img = read_img(input_dir)
    cropped_image = img[rect.y:rect.y + rect.height, rect.x:rect.x + rect.width]
    return cropped_image


# def helper

def crop_helper(save_dir: str, input_dir: str, boundng_boxes):
    for i in boundng_boxes:
        cropped = crop_img(input_dir, boundng_boxes)
        filename = f"img_{i}.jpg"
        filepath = os.path.join(save_dir, filename)
        cv2.imwrite(filepath, cropped)
