import numpy as np
import torch

from d3dshot.capture_outputs.pytorch_gpu_capture_output import PytorchGPUCaptureOutput


class PytorchFloatGPUCaptureOutput(PytorchGPUCaptureOutput):
    def process(self, pointer, pitch, size, width, height, region, rotation):
        image = super().process(pointer, pitch, size, width, height, region, rotation)
        from PIL import Image

        return Image.fromarray(np.array(frame.cpu() * 255.0, dtype=np.uint8))
