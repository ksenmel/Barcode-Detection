import tempfile
import shutil

from barcode_detection.localization.localize import Localizer
from pathlib import Path


class LocalizeIyyun(Localizer):
    WORKING_DIR = "workspace"
    IMAGES_DIR = "images"
    BOUNDING_BOXES_DIR = "bounding_boxes"

    DOCKER_IMAGE_NAME = "iyyun_docker"
    DOCKER_IMGS_BIND_PATH = "/" + WORKING_DIR + "/" + IMAGES_DIR
    DOCKER_BOUNDING_BOXES_BIND_PATH = "/" + WORKING_DIR + "/" + BOUNDING_BOXES_DIR

    def __init__(self, client):
        self.client = client

    def get_boundings(self, input_dir: str):
        images = Path(
            "barcode_detection/localization/iyyun_method/docker/" + self.IMAGES_DIR
        ).resolve()
        images.mkdir()

        bounding_boxes_path = Path(
            "barcode_detection/localization/iyyun_method/" + self.BOUNDING_BOXES_DIR
        ).resolve()

        if bounding_boxes_path.is_dir():
            shutil.rmtree(bounding_boxes_path)

        bounding_boxes_path.mkdir()

        # have to copy all images because of building dockers previously
        for file in Path(input_dir).glob("*.jpg"):
            shutil.copy(file, images)

        # tmp dir to make paths for docker binding
        with tempfile.TemporaryDirectory() as tmp_dir:
            bounding_boxes = Path(tmp_dir) / self.BOUNDING_BOXES_DIR
            bounding_boxes.mkdir()

            container = self.client.containers.run(
                self.DOCKER_IMAGE_NAME,
                volumes={
                    images: {"bind": self.DOCKER_IMGS_BIND_PATH},
                    bounding_boxes: {"bind": self.DOCKER_BOUNDING_BOXES_BIND_PATH},
                },
                detach=True,
            )
            container.wait()
            container.remove()

            shutil.rmtree(images)

            for file in bounding_boxes.glob("*.txt"):
                shutil.copy(file, bounding_boxes_path)

        return bounding_boxes_path
