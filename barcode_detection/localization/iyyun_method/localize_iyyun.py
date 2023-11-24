import os

import cv2
import docker
import numpy as np
import tempfile

from barcode_detection.boundingbox.bounding_box import BoundingBox
from barcode_detection.localization.localize import Localizer
from barcode_detection.utils import get_dir


class LocalizeIyyun(Localizer):

    def get_boundings(self, input_img: np.ndarray) -> list[BoundingBox]:

        tmp_dir = tempfile.mkdtemp()
        file_path = os.path.join(tmp_dir, f"img.png")
        cv2.imwrite(file_path, input_img)

        root_dir = get_dir()
        docker_dir = os.path.join(root_dir, "barcode_detection/localization/iyyun_method/docker")

        client = docker.from_env()
        client.images.build(path=docker_dir,
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

        lines = output.splitlines()

        values = []
        for line in lines:
            values.append(line.decode('utf-8').split(','))
        print(values[0])

        bounding_boxes = []
        for value in values:
            # iyyun method returns x, y, width, height coordinates
            bounding_box = BoundingBox(int(value[0]), int(value[1]), int(value[2]), int(value[3]))
            bounding_boxes.append(bounding_box)

        return bounding_boxes
