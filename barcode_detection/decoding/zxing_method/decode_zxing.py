import cv2
import docker
import numpy as np
import tempfile

from barcode_detection.boundingbox.bounding_box import BoundingBox
from barcode_detection.decoding.decode import Decoder
from barcode_detection.utils import crop_img, get_dir
from pathlib import Path


class DecodeZxing(Decoder):
    def decode(self, input_img: np.ndarray, bounding_boxes: list[BoundingBox]):

        tmp_dir = tempfile.mkdtemp()

        for box in bounding_boxes:
            cropped = crop_img(input_img, box)
            file_path = Path(tmp_dir) / f"cropped_{box}.png"

            cv2.imwrite(str(file_path), cropped)

        client = docker.from_env()
        container = client.containers.run("zxing_docker",
                                          volumes={tmp_dir: {'bind': '/workspace/tmp_for_img', 'mode': 'rw'}},
                                          detach=True)
        container.wait()

        output = container.logs()

        # delete tmp dir
        tmp_path = Path(tmp_dir)
        for file in tmp_path.iterdir():
            if file.is_file():
                file.unlink()
            else:
                file.rmdir()
        tmp_path.rmdir()

        container.remove()

        decoded_string = output.decode('utf-8')
        output_list = eval(decoded_string)

        return output_list
