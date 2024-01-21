from typing import Callable
import time, datetime
import logging
import cv2
import abc


class ImageCaptureFailure(Exception):
    
    def __init__(self, err_msg: str) -> None:
        super().__init__(err_msg)


class ImageCapture(abc.ABC):
    
    @abc.abstractclassmethod
    def capture_image(self): ...
    
    def start_capturing(self, image_processor: Callable):
        
        while True:
            time.sleep(2)
            
            try:
                image = self.capture_image()
            except ImageCaptureFailure as e:
                # logging.warning(f"Camera Capture failure at {datetime.datetime.now()}")
                logging.warning(str(e))
                continue

            # Process captured image
            image_processor(image)
 

class CaptureByCv(ImageCapture):
    
    def __init__(self) -> None:
        super().__init__()
        self.capturer = cv2.VideoCapture(0)
        self.capturer.set(3, 640)
        self.capturer.set(4, 480)
        
    def capture_image(self):
        is_captured, frame = self.capturer.read()
        
        if not is_captured:
            raise ImageCaptureFailure(f"Camera Capture failure at {datetime.datetime.now()}")
        
        return frame


class ImageCaptureFactory:
    
    @staticmethod
    def caputre_by_cv() -> ImageCapture:
        return CaptureByCv()