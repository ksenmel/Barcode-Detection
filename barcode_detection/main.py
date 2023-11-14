from decoding.decode_pyzbar import DecodePyzbar
from localization.localize_yolo import LocalizeYolo
from utils import read_img

img = read_img("PXL_20230826_081602262.jpg")
detector_path = "path to yolov7-stickers.onnx"

decoder = DecodePyzbar()
localizer = LocalizeYolo(detector_path)

bounding_boxes = localizer.get_boundings(img)
decoder.decode(img, bounding_boxes)

