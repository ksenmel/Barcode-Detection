import cv2
import numpy as np
import tempfile

from pathlib import Path

from barcode_detection.core.bounding_box import BoundingBox
from barcode_detection.decoding.decode import Decoder
from barcode_detection.utils import crop_img


class DecodeZxing(Decoder):
    IMG_DIR = "img"
    BARCODES_DIR = "barcodes"
    DOCKER_IMAGE_NAME = "zxing_docker"
    DOCKER_IMG_BIND_PATH = "/workspace/img"
    DOCKER_BARCODES_BIND_PATH = "/workspace/barcodes"

    DECODED_BARCODES_FILE = "decoded_barcodes.txt"

    def __init__(self, client):
        self.client = client

    def decode(self, input_img: np.ndarray, bounding_boxes: list[BoundingBox]):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path_to_img = Path(tmp_dir) / self.IMG_DIR
            path_to_boxes = Path(tmp_dir) / self.BARCODES_DIR

            path_to_img.mkdir()
            path_to_boxes.mkdir()

            for box in bounding_boxes:
                cropped = crop_img(input_img, box)
                file_path = path_to_img / f"cropped_{box}.png"

                cv2.imwrite(str(file_path), cropped)

            container = self.client.containers.run(
                self.DOCKER_IMAGE_NAME,
                volumes={
                    path_to_img: {"bind": self.DOCKER_IMG_BIND_PATH},
                    path_to_boxes: {"bind": self.DOCKER_BARCODES_BIND_PATH},
                },
                detach=True,
            )

            container.wait()
            container.remove()

            with open(path_to_boxes / self.DECODED_BARCODES_FILE, "r") as file:
                lines = file.readlines()

            codes = [line.strip() for line in lines]

            return codes
