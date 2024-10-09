import numpy as np
import torch

from d3dshot.capture_outputs.pytorch_capture_output import PytorchCaptureOutput


class PytorchGPUCaptureOutput(PytorchCaptureOutput):
    def __init__(self) -> None:
        self.device = torch.device("cuda")
        torch.tensor([0], device=self.device)  # Warm up CUDA

    def process(self, pointer, pitch, size, width, height, region, rotation):
        image = super().process(pointer, pitch, size, width, height, region, rotation)
        return image.to(self.device)

        from PIL import Image

        return Image.fromarray(np.array(frame.cpu()))
