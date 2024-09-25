import cv2
import numpy as np
import shutil

from barcode_detection.core.bounding_box import BoundingBox
from barcode_detection.localization.localize import Localizer
from barcode_detection.localization.onnx_yolov7 import OnnxDetector
from pathlib import Path


class LocalizeYolo(Localizer):
    def __init__(self, detector_path):
        self.detector_path = detector_path
        self.sticker_detector = OnnxDetector(self.detector_path)

    def get_boundings(self, input_dir: str):

        deblurred_frames_path_dir = Path(input_dir)

        bounding_boxes_dir = Path(
            "barcode_detection/localization/onnx_yolov7/bounding_boxes"
        )

        if bounding_boxes_dir.is_dir():
            shutil.rmtree(bounding_boxes_dir)

        bounding_boxes_dir.mkdir()

        # should rewrite here every N step
        for file in deblurred_frames_path_dir.glob("*.jpg"):
            filename = file.name.split(".")[0]
            output_file_path = bounding_boxes_dir / f"{filename}.txt"

            img = cv2.imread(f"{file}")

            cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            stickers = self.sticker_detector(img)

            bounding_boxes = []

            with open(output_file_path, "w") as f:
                for box in stickers["bboxes"]:
                    box = box.round().astype(np.int32).tolist()

                    bounding_box = BoundingBox(
                        box[0], box[1], box[2] - box[0], box[3] - box[1]
                    )
                    bounding_boxes.append(bounding_box)

                    bounding_box_line = (
                        f"{box[0]},{box[1]},{box[2] - box[0]},{box[3] - box[1]}\n"
                    )
                    f.write(bounding_box_line)
