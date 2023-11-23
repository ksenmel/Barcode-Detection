import os

import cv2
import docker
import numpy as np
import tempfile

from barcode_detection.boundingbox.bounding_box import BoundingBox
from barcode_detection.localization.localize import Localizer


class LocalizeIyyun(Localizer):

    def get_boundings(self, input_img: np.ndarray) -> list[BoundingBox]:

        tmp_dir = tempfile.mkdtemp()
        file_path = os.path.join(tmp_dir, f"img.png")
        cv2.imwrite(file_path, input_img)

        client = docker.from_env()
        client.images.build(path="/Users/kseniia/Barcode-Detection/barcode_detection/localization/iyyun_method/docker",
                            tag="iyyun_docker")
        container = client.containers.run("iyyun_docker",
                                          volumes={tmp_dir: {'bind': '/workspace/tmp_for_img', 'mode': 'rw'}},
                                          detach=True)
        container.wait()

        output = container.logs()

        # delete tmp dir
        for file in os.listdir(tmp_dir):
            file_path = os.path.join(tmp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(tmp_dir)

        container.remove()

        return output