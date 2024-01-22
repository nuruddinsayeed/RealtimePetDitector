from ultralytics import YOLO
from pathlib import Path

# DEVICE = "cuda" if not torch.cuda.is_available() else "cpu"
DEVICE = "cpu"
MODEL_PATH = Path(__file__).resolve().parent / 'model.pt'

def load_model(trained_model_path=str(MODEL_PATH), device=DEVICE):
        model = YOLO(trained_model_path)
        model.conf = 0.60 # NMS confidence threshold
        model.iou = 0.30  # NMS IoU threshold
        
        model.to(device=device)
        
        return model