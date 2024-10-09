import numpy as np

from d3dshot.capture_outputs.numpy_capture_output import NumpyCaptureOutput


class NumpyFloatCaptureOutput(NumpyCaptureOutput):
    def process(self, pointer, pitch, size, width, height, region, rotation):
        image = super().process(pointer, pitch, size, width, height, region, rotation)
        return np.divide(image, 255.0)

        from PIL import Image

        return Image.fromarray(np.array(frame * 255.0, dtype=np.uint8))
