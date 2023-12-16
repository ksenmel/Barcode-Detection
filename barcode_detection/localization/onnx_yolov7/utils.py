import cv2

__all__ = ["create_letterbox"]


def create_letterbox(
    image,
    new_shape=(640, 640),
    padding_color=(114, 114, 114),
    stride=32,
):
    # Resize and pad image while meeting stride-multiple constraints
    shape = image.shape[:2]  # current shape [height, width]

    # Scale ratio (new / old)
    scale_ratio = min(new_shape[0] / shape[0], new_shape[1] / shape[1])

    # Compute padding
    new_unpadded_shape = int(round(shape[1] * scale_ratio)), int(
        round(shape[0] * scale_ratio)
    )
    dw, dh = (
        new_shape[1] - new_unpadded_shape[0],
        new_shape[0] - new_unpadded_shape[1],
    )  # wh padding

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpadded_shape:  # resize
        image = cv2.resize(image, new_unpadded_shape, interpolation=cv2.INTER_LINEAR)
    offset = 0.1
    top, bottom = int(round(dh - offset)), int(round(dh + offset))
    left, right = int(round(dw - offset)), int(round(dw + offset))
    image = cv2.copyMakeBorder(
        image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=padding_color
    )  # add border

    return image, scale_ratio, dw, dh
