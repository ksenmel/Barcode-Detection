from decoding.decode import decode_pyzbar
from localization.localize import yolov7_method
from utils import crop_helper

input_img = "dataset/PXL_20230826_081352782.jpg"
det_path = "localization/onnx_yolov7/yolov7-stickers.onnx"

bounding_boxes = yolov7_method(input_img, det_path)
decode_pyzbar(input_img, bounding_boxes)

# save_dir = "/Users/kseniia/Desktop/newtest"
# crop_helper(save_dir, input_img, bounding_boxes)