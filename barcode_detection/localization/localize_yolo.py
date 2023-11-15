import cv2
import numpy as np

from barcode_detection.boundingbox.bounding_box import BoundingBox
from barcode_detection.localization.localize import Localizer
from barcode_detection.localization.onnx_yolov7 import OnnxDetector


class LocalizeYolo(Localizer):
    def __init__(self, detector_path):
        self.detector_path = detector_path
        self.sticker_detector = OnnxDetector(self.detector_path)

    def get_boundings(self, input_img: np.ndarray):
        img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)

        stickers = self.sticker_detector(img)

        bounding_boxes = []

        for box in stickers["bboxes"]:
            box = box.round().astype(np.int32).tolist()

            # x, y, width, height
            bounding_box = BoundingBox(box[0], box[1], box[2] - box[0], box[3] - box[1])
            bounding_boxes.append(bounding_box)

        return bounding_boxes
