from app.pet_detector import AnimalDitector
from ultralytics import YOLO

from app.image_capture import ImageCaptureFactory


# DEVICE = "cuda" if not torch.cuda.is_available() else "cpu"
DEVICE = "cpu"

def load_model(trained_model_path, device=DEVICE):
        model = YOLO(trained_model_path)
        model.conf = 0.60 # NMS confidence threshold
        model.iou = 0.30  # NMS IoU threshold
        
        model.to(device=device)
        
        return model

def detect_from_camera():
    # Configure Detection System
    model = load_model('model.pt')
    pet_detector = AnimalDitector(model=model, cls_names=['Cat', 'Dog'], save=True)
    
    # start Capturing
    ImageCaptureFactory.caputre_by_cv(
        ).start_capturing(image_processor=pet_detector.detect)
    

if __name__ == '__main__':
    detect_from_camera()