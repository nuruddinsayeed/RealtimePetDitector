from typing import Callable, Tuple, Any, List

import cv2
import numpy as np
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
from matplotlib.backends.backend_qt5agg import FigureCanvas

from pet_detection.app.data_models.detection_models import DetectionResult, DetectedClass


class PlotFigureCanvas(anim.FuncAnimation):

    def __init__(self, x_len:int, y_range:list, interval:int,
                 detect_pet: Callable[..., Tuple[DetectionResult, Any]],
                 update_detect_count: Callable[[List[DetectedClass]], None],
                 live_cam: bool = False) -> None:

        plt_fig = mpl_fig.Figure()
        plt_fig.suptitle('Real time image detection update')

        self.canvas = FigureCanvas(plt_fig)
        self._live_cam = live_cam
        self._x_len_ = x_len
        self._y_range_ = y_range
        self.interval = interval
        self._detect_pet = detect_pet
        self._update_detect_count = update_detect_count

        x = list(range(0, x_len))
        y = [0] * x_len

        self._ax_  = self.canvas.figure.subplots()
        self._ax_.set_ylabel('Frame rate / (S)')
        self._ax_.set_xlabel('Porcessed image count')
        
        self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        self._line_, = self._ax_.plot(x, y)

        self.animation = anim.FuncAnimation(self.canvas.figure, self._update_canvas_,
                                            fargs=(y,), interval=interval, blit=True)
        return

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
   
        detect_res, frame = self._detect_pet()
        if self._live_cam:
            cv2.imshow('Camera', frame)
        
        new_point = detect_res.detection_fps
        y.append(int(float(new_point)))     # Add new datapoint
        y = y[-self._x_len_:]
        self._line_.set_ydata(y)
        
        if detect_res.confidences:
            self._update_detect_count(detect_res.confidences)
        return self._line_,
    