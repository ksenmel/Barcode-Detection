import cv2
import numpy as np

from boundingbox.BoundingBox import BoundingBox
from localization.localize import Localizer
from localization.onnx_yolov7 import OnnxDetector


class LocalizeYolo(Localizer):

    def get_boundings(self, input_img: np):
        detector = "/Users/kseniia/Desktop/yolov7-stickers.onnx"
        onnx_sticker_detector_path = detector
        sticker_detector = OnnxDetector(onnx_sticker_detector_path)

        img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)

        stickers = sticker_detector(img)

        bounding_boxes = []

        for box in (stickers["bboxes"]):
            box = box.round().astype(np.int32).tolist()
            bounding_box = BoundingBox(box[0], box[1], box[2], box[3])
            bounding_boxes.append(bounding_box)

        return bounding_boxes
