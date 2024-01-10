import datetime
from typing import List
from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator
from pathlib import Path

from app.data_models.detection_models import DetectionResult

SAVE_TO = Path(__file__).resolve().parent.parent / 'predictions'

class AnimalDitector:
    
    def __init__(self, model: YOLO, cls_names: List[str], save: bool = True, save_to: Path = SAVE_TO) -> None:
        self.model = model
        self.detection_classes = cls_names
        self.save_image = save
        self.save_to = save_to


    def detect(self, image) -> List[DetectionResult]:
        
        detected_at = datetime.datetime.now()
        # dir_name = detected_at.strftime("%m_%d_%Y_%H_%M_%S")
        print('started prediction')
        # results = self.model.predict(
        #     source=image, conf=.40, save=self.save_image, project = str(self.save_to), name=dir_name)
        results = self.model.predict(source=image, conf=.4, save=False)
        detection_ended_at = datetime.datetime.now()
        print(f"Detection took: {(detection_ended_at - detected_at).seconds} seconds.")
        
        if self.save_image:
            self.save_plot_image(img=image, results=results)
        
        return self.analyze_results(results=results, detected_at=detection_ended_at, cls_names=self.detection_classes)
    
    def save_plot_image(self, img, results):
        for result in results:
            annotator = Annotator(img)
        
            boxes = result.boxes
            for box in boxes:
                
                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls
                annotator.box_label(b, self.model.names[int(c)])
            
        img = annotator.result() 
        cv2.imwrite(filename=str(self.save_to / f'{datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.png'), img=img)


    def analyze_result_data(self, result, detected_at: datetime.datetime, cls_names: List[str]) -> DetectionResult:
        detected_cls_list = result.boxes.cls
        detection_confidanc_list = result.boxes.conf
        
        detection_result = DetectionResult(detected_at=detected_at)
        for i, detected_cls in enumerate(detected_cls_list):
            cls_name = cls_names[int(detected_cls)]
            confidance = detection_confidanc_list[i]
            
            detection_result.add_new_detection(class_name=cls_name, confidance_ratio=confidance)
        
        return detection_result
        
    def analyze_results(self, results, detected_at, cls_names) -> List[DetectionResult]:
        
        analyzed_results = list()
        for result in results:
            analyzed_result = self.analyze_result_data(result=result, detected_at=detected_at, cls_names=cls_names)
            analyzed_results.append(analyzed_result)
            
        return analyzed_results