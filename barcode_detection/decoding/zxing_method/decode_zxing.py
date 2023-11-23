import cv2
import docker
import numpy as np
import os
import tempfile

from barcode_detection.boundingbox.bounding_box import BoundingBox
from barcode_detection.decoding.decode import Decoder
from barcode_detection.utils import crop_img, get_dir


class DecodeZxing(Decoder):
    def decode(self, input_img: np.ndarray, bounding_boxes: list[BoundingBox]):

        tmp_dir = tempfile.mkdtemp()

        for box in bounding_boxes:
            cropped = crop_img(input_img, box)

            file_path = os.path.join(tmp_dir, f"cropped_{box}.png")
            cv2.imwrite(file_path, cropped)

        root_dir = get_dir()
        docker_dir = os.path.join(root_dir, "barcode_detection/decoding/zxing_method/docker")

        client = docker.from_env()
        client.images.build(path=docker_dir,
                            tag="zxing_docker")
        container = client.containers.run("zxing_docker", volumes={tmp_dir: {'bind': '/workspace/tmp_for_img', 'mode': 'rw'}},
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

        decoded_string = output.decode('utf-8')
        output_list = eval(decoded_string)

        return output_list
