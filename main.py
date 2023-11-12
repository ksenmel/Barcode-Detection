from decoding.decode_pyzbar import DecodePyzbar
from localization.localize_yolo import LocalizeYolo

input_img = "dataset/PXL_20230826_081352782.jpg"
det_path = "path to yolov7-stickers.onnx"

decoder = DecodePyzbar()
find_barcodes = LocalizeYolo

bounding_boxes = find_barcodes.yolov7_method(input_img, det_path)
decoder.decode(input_img, bounding_boxes)
