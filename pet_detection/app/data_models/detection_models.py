from typing import NamedTuple, List
import dataclasses
import datetime


class DetectedClass(NamedTuple):
    class_name: str
    confidance_ratio: float

@dataclasses.dataclass
class DetectionResult:
    detected_at: datetime.datetime
    confidences: List[DetectedClass] = dataclasses.field(default_factory=list)
    
    def add_new_detection(self, class_name: str, confidance_ratio: float):
        self.confidences.append(DetectedClass(class_name, confidance_ratio))