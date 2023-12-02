import cv2
import docker
import numpy as np
import tempfile

from barcode_detection.core.bounding_box import BoundingBox
from barcode_detection.decoding.decode import Decoder
from barcode_detection.utils import crop_img
from pathlib import Path


class DecodePyzbar(Decoder):
    def decode(self, input_img: np.ndarray, bounding_boxes: list[BoundingBox]):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path_to_img = Path(tmp_dir) / "img"
            path_to_boxes = Path(tmp_dir) / "boxes"

            path_to_img.mkdir()
            path_to_boxes.mkdir()

            for box in bounding_boxes:
                cropped = crop_img(input_img, box)
                file_path = path_to_img / f"cropped_{box}.png"

                cv2.imwrite(str(file_path), cropped)

            client = docker.from_env()

            container = client.containers.run(
                "pyzbar_docker",
                volumes={
                    path_to_img: {"bind": "/workspace/img"},
                    path_to_boxes: {"bind": "/workspace/boxes"},
                },
                detach=True,
            )

            container.wait()
            container.remove()

            with open(path_to_boxes / "decoded_barcodes.txt", "r") as file:
                lines = file.readlines()

            codes = []

            values = [line.strip() for line in lines]
            for code in values:
                codes.append(code)

            return codes

