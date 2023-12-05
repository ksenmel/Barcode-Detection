import cv2
import numpy as np
import tempfile

from barcode_detection.core.bounding_box import BoundingBox
from barcode_detection.localization.localize import Localizer
from pathlib import Path


class LocalizeIyyun(Localizer):
    IMG_DIR = "img"
    BOUNDINGS_DIR = "boxes"
    DOCKER_IMAGE_NAME = "iyyun_docker"
    DOCKER_IMG_BIND_PATH = "/workspace/img"
    DOCKER_BOUNDINGS_BIND_PATH = "/workspace/boxes"
    IMG_FILE_NAME = "img.png"
    BOUNDINGS_FILE_NAME = "boundings.txt"

    def __init__(self, client):
        self.client = client

    def get_boundings(self, input_img: np.ndarray) -> list[BoundingBox]:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path_to_img = Path(tmp_dir) / self.IMG_DIR
            path_to_boxes = Path(tmp_dir) / self.BOUNDINGS_DIR

            path_to_img.mkdir()
            path_to_boxes.mkdir()

            file_path = path_to_img / self.IMG_FILE_NAME

            cv2.imwrite(str(file_path), input_img)

            container = self.client.containers.run(
                self.DOCKER_IMAGE_NAME,
                volumes={
                    path_to_img: {"bind": self.DOCKER_IMG_BIND_PATH},
                    path_to_boxes: {"bind": self.DOCKER_BOUNDINGS_BIND_PATH},
                },
                detach=True,
            )
            container.wait()
            container.remove()

            with open(path_to_boxes / self.BOUNDINGS_FILE_NAME, "r") as file:
                contents = file.read()
                lines = contents.splitlines()

                values = []
                for line in lines:
                    values.append(line.split(","))

                bounding_boxes = []
                for value in values:
                    bounding_box = BoundingBox(
                        # this method returns left corner 'x', 'y' coordinates and
                        # width and height of the bounding box
                        int(value[0]),
                        int(value[1]),
                        int(value[2]),
                        int(value[3]),
                    )
                    bounding_boxes.append(bounding_box)

                return bounding_boxes
