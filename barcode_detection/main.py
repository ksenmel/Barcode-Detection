from decoding.decode_pyzbar import DecodePyzbar
from localization.localize_yolo import LocalizeYolo
from pathlib import Path
from utils import read_img

img = read_img("../example/PXL_20230826_081602262.jpg")

# write a path to yolov7 weights here
detector_path = "/Users/kseniia/Desktop/barcode_loc/yolov7-stickers.onnx"

decoder = DecodePyzbar()
localizer = LocalizeYolo(detector_path)

bounding_boxes = localizer.get_boundings(img)
decoder.decode(img, bounding_boxes)

