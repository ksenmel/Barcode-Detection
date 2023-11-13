from decoding.decode_pyzbar import DecodePyzbar
from localization.localize_yolo import LocalizeYolo
from utils import read_img, crop_helper

img = read_img("dataset/PXL_20230826_081602262.jpg")

decoder = DecodePyzbar()
localizer = LocalizeYolo()

bounding_boxes = localizer.get_boundings(img)
decoder.decode(img, bounding_boxes)

