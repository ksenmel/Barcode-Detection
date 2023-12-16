import numpy as np
import onnxruntime as ort

from barcode_detection.localization.onnx_yolov7.utils import create_letterbox

__all__ = ["OnnxDetector"]


class OnnxDetector:
    def __init__(self, onnx_model_path, model_size=(640, 640)):
        self.model_path = onnx_model_path
        use_gpu = ort.get_device() == "GPUs"
        providers = (
            ["CUDAExecutionProvider", "CPUExecutionProvider"]
            if use_gpu
            else ["CPUExecutionProvider"]
        )
        self.session = ort.InferenceSession(onnx_model_path, providers=providers)
        self.size = model_size

    def __call__(self, image):
        return self.infer(image)

    def infer(self, image):
        output_names = [output.name for output in self.session.get_outputs()]
        input_names = [input_.name for input_ in self.session.get_inputs()]
        image_input_name = input_names[0]
        transformed = image.copy()
        transformed, ratio, dw, dh = create_letterbox(transformed, self.size)
        input_ = {image_input_name: self.__transform_image(transformed)}
        outputs = self.session.run(output_names, input_)[0]
        bboxes_start_index = 1
        bboxes_end_index = 5
        scores_index = 6
        bboxes = outputs[:, bboxes_start_index:bboxes_end_index]
        bboxes -= np.array((dw, dh) * 2)
        bboxes /= ratio
        scores = outputs[:, scores_index]

        return {"bboxes": bboxes, "scores": scores}

    def __transform_image(self, image):
        transformed = image.transpose((2, 0, 1))
        transformed = np.expand_dims(transformed, 0)
        transformed = np.ascontiguousarray(transformed)

        transformed = transformed.astype(np.float32)
        transformed /= 255

        return transformed
