import cv2
import numpy as np

from localization.onnx_yolov7 import OnnxDetector
from boundingbox.BoundingBox import BoundingBox


def yolov7_method(input_img: str, detector_path: str):
    onnx_sticker_detector_path = detector_path
    sticker_detector = OnnxDetector(onnx_sticker_detector_path)

    img = cv2.imread(input_img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    stickers = sticker_detector(img)

    bounding_boxes = []

    for box in (stickers["bboxes"]):
        box = box.round().astype(np.int32).tolist()
        bounding_box = BoundingBox(box[0], box[1], box[2], box[3])
        bounding_boxes.append(bounding_box)

    return bounding_boxes
