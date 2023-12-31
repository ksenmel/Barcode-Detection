import argparse
import docker

from barcode_detection.decoding.pyzbar_method.decode_pyzbar import DecodePyzbar
from barcode_detection.decoding.zxing_method.decode_zxing import DecodeZxing
from barcode_detection.localization.onnx_yolov7.localize_yolo import LocalizeYolo
from barcode_detection.localization.iyyun_method.localize_iyyun import LocalizeIyyun
from barcode_detection.utils import read_img


def find_and_decode(
    input_img: str, decode_option: str, localize_option: str, detector_path: str
):
    img = read_img(input_img)
    client = docker.from_env()

    if decode_option == "pyzbar":
        decoder = DecodePyzbar(client)
    elif decode_option == "zxing":
        decoder = DecodeZxing(client)
    else:
        raise Exception("invalid decoding option")

    if localize_option == "iyyun":
        localizer = LocalizeIyyun(client)
    elif localize_option == "yolov7":
        localizer = LocalizeYolo(detector_path)
    else:
        raise Exception("invalid localization option")

    bounding_boxes = localizer.get_boundings(img)
    decoded = decoder.decode(img, bounding_boxes)

    print(decoded)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find and decode images")
    parser.add_argument(
        "input_img",
        help="Path to the input image",
        default="example/image.jpg",
    )
    parser.add_argument("decode_option", help="Path to the decode option")
    parser.add_argument("localize_option", help="Path to the localize option")
    parser.add_argument(
        "--detector_path", help="Path to the detector model", required=False
    )

    args = parser.parse_args()

    if args.localize_option == "yolov7" and args.detector_path is None:
        parser.error(
            "--detector_path is required when localize_option is set to 'yolov7'"
        )

    find_and_decode(
        args.input_img, args.decode_option, args.localize_option, args.detector_path
    )
