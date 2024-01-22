from pet_detection.app.pet_detector import AnimalDitector

from pet_detection.app.image_capture import ImageCaptureFactory
from . import load_model

def detect_from_camera():
    # Configure Detection System
    model = load_model('model.pt')
    pet_detector = AnimalDitector(model=model, cls_names=['Cat', 'Dog'], save=False, return_img=True)
    
    # start Capturing
    ImageCaptureFactory.caputre_by_cv(
        ).start_capturing(image_processor=pet_detector.detect)
    

if __name__ == '__main__':
    detect_from_camera()