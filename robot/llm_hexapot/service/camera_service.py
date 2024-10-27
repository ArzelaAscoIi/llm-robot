from picamera2 import Picamera2
import numpy as np


class CameraService:
    def __init__(self) -> None:
        self.picam2: Picamera2 = Picamera2()

    def capture_image(self) -> np.ndarray:
        self.picam2.start()
        image: np.ndarray = self.picam2.capture_array()
        self.picam2.stop()
        return image

    def capture_and_save_image(self, filename: str = "image.jpg") -> str:
        image: np.ndarray = self.capture_image()
        Picamera2.save_array(filename, image, format="JPEG")
        return filename
