import tempfile

from barcode_detection.decoding.decode import Decoder
from barcode_detection.utils import crop_image
from pathlib import Path


class DecodeZxing(Decoder):
    IMGS_DIR = "images"
    BARCODES_DIR = "barcodes"
    WORKING_DIR = "workspace"
    DOCKER_IMAGE_NAME = "zxing_docker"

    DOCKER_IMG_BIND_PATH = "/" + WORKING_DIR + "/" + IMGS_DIR
    DOCKER_BARCODES_BIND_PATH = "/" + WORKING_DIR + "/" + BARCODES_DIR

    DECODED_BARCODES_FILE = "decoded_barcodes.txt"

    def __init__(self, client):
        self.client = client

    def decode(self, images_dir: str, bounding_boxes_dir: str):
        # tmp dir to make paths for docker binding
        with tempfile.TemporaryDirectory() as tmp_dir:
            images = Path(tmp_dir) / self.IMGS_DIR
            images.mkdir()

            barcodes = Path(tmp_dir) / self.BARCODES_DIR
            barcodes.mkdir()

            # crop image by its bounding box
            crop_image(
                save_dir=str(images),
                images_dir=images_dir,
                bounding_boxes_path=bounding_boxes_dir,
            )

            container = self.client.containers.run(
                self.DOCKER_IMAGE_NAME,
                volumes={
                    images: {"bind": self.DOCKER_IMG_BIND_PATH},
                    barcodes: {"bind": self.DOCKER_BARCODES_BIND_PATH},
                },
                detach=True,
            )

            container.wait()
            container.remove()

            with open(barcodes / self.DECODED_BARCODES_FILE, "r") as file:
                lines = file.readlines()

            codes = [line.strip() for line in lines]

            return codes
