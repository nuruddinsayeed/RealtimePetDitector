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
            detect_res, frame = self.capture_and_process(image_processor=image_processor)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    def capture_and_process(self, image_processor: Callable):
        try:
            image = self.capture_image()
        except ImageCaptureFailure as e:
            logging.warning(str(e))
            
        detect_res, frame = image_processor(image)
        print(detect_res)
        
        return detect_res, frame
            
 

class CaptureByCv(ImageCapture):
    
    def __init__(self) -> None:
        super().__init__()
        self.capturer = cv2.VideoCapture(0)
        self.capturer.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capturer.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # self.capturer.set(3, 640)
        # self.capturer.set(4, 480)
        
    def capture_image(self):
        is_captured, frame = self.capturer.read()
        
        if not is_captured:
            raise ImageCaptureFailure(f"Camera Capture failure at {datetime.datetime.now()}")
        
        return frame


class ImageCaptureFactory:
    
    @staticmethod
    def caputre_by_cv() -> ImageCapture:
        return CaptureByCv()