import datetime
from typing import List, Tuple
from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator
from pathlib import Path
import numpy as np
import time

from pet_detection.app.data_models.detection_models import DetectionResult

SAVE_TO = Path(__file__).resolve().parent.parent / 'predictions'
COLORS = [tuple(255 * np.random.rand(3)) for _ in range(10)]

class AnimalDitector:
    
    def __init__(self, model: YOLO, cls_names: List[str],
                 save: bool = True, return_img: bool = True, save_to: Path = SAVE_TO) -> None:
        self.model = model
        self.detection_classes = cls_names
        self.save_image = save
        self.return_img = return_img
        self.save_to = save_to


    def detect(self, image) -> Tuple[List[DetectionResult], any]:
        
        detected_at = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")

        start_time = time.time()
        results = self.model.predict(source=image, conf=.4, save=False)
        prediction_fps = '{:.1f}'.format(1 / (time.time() - start_time))
        
        img_ploted = self.plot_image(img=image, results=results)
        
        # save is enabled and images has detected
        if self.save_image and any([result.boxes for result in results]) :
            cv2.imwrite(filename=str(self.save_to / f'{datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.png'),
                        img=img_ploted)
            
        # analyzed_data = self.analyze_results(
        #     results=results, detected_at=detected_at, pred_fps=prediction_fps, cls_names=self.detection_classes)
        analyzed_data = self.analyze_result_data(result=results[0], detected_at=detected_at, pred_fps=prediction_fps)

        return analyzed_data, img_ploted
    
    def plot_image(self, img, results):
        for result in results:
            annotator = Annotator(img)
        
            boxes = result.boxes
            for box in boxes:
                
                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls
                annotator.box_label(b, self.model.names[int(c)])
            
        img_ploted = annotator.result() 
        
        return img_ploted


    def analyze_result_data(self, result, detected_at: datetime.datetime, pred_fps: float) -> DetectionResult:
        detected_cls_list = result.boxes.cls
        detection_confidanc_list = result.boxes.conf
        
        detection_result = DetectionResult(detection_fps=pred_fps, detected_at=detected_at)
        for i, detected_cls in enumerate(detected_cls_list):
            cls_name = self.detection_classes[int(detected_cls)]
            confidance = detection_confidanc_list[i]
            
            detection_result.add_new_detection(class_name=cls_name, confidance_ratio=confidance)
        
        return detection_result
        
    def analyze_results(self, results, detected_at, pred_fps: float, cls_names) -> List[DetectionResult]:
        
        analyzed_results = list()
        for result in results:
            analyzed_result = self.analyze_result_data(result=result, detected_at=detected_at, pred_fps=pred_fps,
                                                       cls_names=cls_names)
            analyzed_results.append(analyzed_result)
            
        return analyzed_results
    