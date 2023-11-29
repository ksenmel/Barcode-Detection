import cv2
import docker
import numpy as np
import tempfile

from barcode_detection.boundingbox.bounding_box import BoundingBox
from barcode_detection.localization.localize import Localizer
from pathlib import Path


class LocalizeIyyun(Localizer):
    def get_boundings(self, input_img: np.ndarray) -> list[BoundingBox]:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / f"img.png"
            cv2.imwrite(str(file_path), input_img)

            client = docker.from_env()
            container = client.containers.run(
                "iyyun_docker",
                volumes={tmp_dir: {"bind": "/workspace/tmp_for_img", "mode": "rw"}},
                detach=True,
            )
            container.wait()

            output = container.logs()

            container.remove()

        lines = output.splitlines()

        values = []
        for line in lines:
            values.append(line.decode("utf-8").split(","))

        bounding_boxes = []
        for value in values:
            # iyyun method returns x, y, width, height coordinates
            bounding_box = BoundingBox(
                int(value[0]), int(value[1]), int(value[2]), int(value[3])
            )
            bounding_boxes.append(bounding_box)

        return bounding_boxes
