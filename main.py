from decoding.decode import DecodePyzbar
from localization.localize import LocalizeYolo

input_img = "dataset/PXL_20230826_081352782.jpg"
det_path = "path to yolov7-stickers.onnx"

decoder = DecodePyzbar()
find_barcodes = LocalizeYolo

bounding_boxes = find_barcodes.yolov7_method(input_img, det_path)
decoder.decode_p(input_img, bounding_boxes)


# save_dir = "/Users/kseniia/Desktop/newtest"
# crop_helper(save_dir, input_img, bounding_boxes)