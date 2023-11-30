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

            path_to_img = Path(tmp_dir) / "img"
            path_to_boxes = Path(tmp_dir) / "boxes"

            path_to_img.mkdir()
            path_to_boxes.mkdir()

            file_path = path_to_img / f"img.png"

            cv2.imwrite(str(file_path), input_img)

            client = docker.from_env()
            container = client.containers.run(
                "iyyun_docker",
                volumes={path_to_img: {"bind": "/workspace/img"},
                         path_to_boxes: {"bind": "/workspace/boxes"}},
                detach=True,
            )
            container.wait()
            container.remove()

            with open(path_to_boxes / "boundings.txt", "r") as file:
                contents = file.read()
                lines = contents.splitlines()

                values = []
                for line in lines:
                    values.append(line.split(","))

                bounding_boxes = []
                for value in values:
                    # iyyun method returns x, y, width, height coordinates
                    bounding_box = BoundingBox(
                        int(value[0]), int(value[1]), int(value[2]), int(value[3])
                    )
                    bounding_boxes.append(bounding_box)

                return bounding_boxes
