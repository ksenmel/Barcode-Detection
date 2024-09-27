import argparse

import docker

from barcode_detection.decoding.pyzbar_method.decode_pyzbar import DecodePyzbar
from barcode_detection.decoding.zxing_method.decode_zxing import DecodeZxing
from barcode_detection.localization.onnx_yolov7.localize_yolo import LocalizeYolo
from barcode_detection.localization.iyyun_method.localize_iyyun import LocalizeIyyun

from barcode_detection.deblurring.deblur_real_esrgan import DeblurRealEsrgan


# returns path with deblurred video frames
def deblur_and_frame(video: str):
    return DeblurRealEsrgan().deblur(path_to_video=video)


# returns path with bounding boxes
def find_barcode(images: str, detector: str, localize_option: str):
    client = docker.from_env()

    if localize_option == "iyyun":
        localizer = LocalizeIyyun(client)
    elif localize_option == "yolov7":
        localizer = LocalizeYolo(detector)
    else:
        raise Exception("Invalid localization option")

    return str(localizer.get_boundings(images))


# return decoded barcodes
def decode_barcode(images: str, bounding_boxes: str, decode_option: str):
    client = docker.from_env()

    if decode_option == "pyzbar":
        decoder = DecodePyzbar(client)
    elif decode_option == "zxing":
        decoder = DecodeZxing(client)
    else:
        raise Exception("Invalid decoding option")

    decoded = decoder.decode(images, bounding_boxes)

    print(decoded)


# full pipeline
def deblur_find_decode(
    video: str, localize_option: str, decode_option: str, detector: str
):
    images = deblur_and_frame(video=video)

    bounding_boxes = find_barcode(
        images=images, detector=detector, localize_option=localize_option
    )

    return decode_barcode(
        images=images, bounding_boxes=bounding_boxes, decode_option=decode_option
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "video",
        help="Path to directory with barcode images",
        default="example/video.mp4",
    )
    parser.add_argument("decode_option", help="Path to the decode option")
    parser.add_argument(
        "localize_option", help="Method of barcode localization (iyyun or yolov7)"
    )
    parser.add_argument("--detector", help="Path to the detector model", required=False)
    parser.add_argument("step", help="Step for video processing", required=False)

    args = parser.parse_args()

    if args.localize_option == "yolov7" and args.detector_path is None:
        parser.error(
            "--detector_path is required when localize_option is set to 'yolov7'"
        )

    deblur_find_decode(
        args.video, args.localize_option, args.decode_option, args.detector
    )
