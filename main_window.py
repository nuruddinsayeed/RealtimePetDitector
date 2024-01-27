import sys
from typing import List
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

from plot_figure_canvas import PlotFigureCanvas
from pet_detection import load_model
from pet_detection.app.pet_detector import AnimalDitector
from pet_detection.app.image_capture import ImageCaptureFactory
from pet_detection.app.data_models.detection_models import DetectedClass


class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, live_cam: bool = False) -> None:
        super().__init__()
        self.myFig = None
        self.detection_classes = ['Cat', 'Dog']
        self._dog_count, self._cat_count = 0, 0
        self._live_cam = live_cam
        
    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(1500, 600)
    
    def configure(self):
        self.setWindowTitle('Real Time Pet Monitor')
        self.frame = QtWidgets.QFrame(self)
        self.frame.setStyleSheet('QWidget { background-color: #eeeeec; }')
        
        self.main_layout = QtWidgets.QVBoxLayout()
        
        self._init_header_ui(parent=self.main_layout)
        self.frame.setLayout(self.main_layout)
        self.setCentralWidget(self.frame)

    def _run_image_detection(self):
        model = load_model()
        pet_detector = AnimalDitector(model=model, cls_names=self.detection_classes, save=False, return_img=True)
        
        # start Capturing
        return ImageCaptureFactory.caputre_by_cv(
            ).capture_and_process(image_processor=pet_detector.detect)
        
    def _init_header_ui(self, parent: QtWidgets.QLayout):
        group_box = QtWidgets.QGroupBox()
        parent.addWidget(group_box)
        
        group_box_layout = QtWidgets.QHBoxLayout()
        group_box.setLayout(group_box_layout)
        
        heading_layout = QtWidgets.QHBoxLayout()
        group_box_layout.addLayout(heading_layout)
        
        self.set_button_layout(parent=heading_layout)
        self.set_summary_layout(parent=heading_layout)
        
    def _init_canvas(self):
        if not self.myFig:
            self.myFig = PlotFigureCanvas(x_len=200, y_range=[0, 25], interval=100, 
                                      detect_pet=self._run_image_detection,
                                      update_detect_count=self._update_count, live_cam=self._live_cam)
            self.main_layout.addWidget(self.myFig.canvas)
        else:
            self.myFig.animation.resume()
        
    def _start_detection(self):
        # Matplotlib Figure
        self.start_btn.setEnabled(False)
        self._init_canvas()
        self.pause_btn.setEnabled(True)
        
    def _pause_detection(self):
        self.pause_btn.setEnabled(False)
        self.myFig.animation.pause()
        self.start_btn.setEnabled(True)
        
    def set_button_layout(self, parent: QtWidgets.QLayout):
        
        group_box = QtWidgets.QGroupBox()
        parent.addWidget(group_box)
        
        group_box_layout = QtWidgets.QHBoxLayout()
        group_box.setLayout(group_box_layout)
        
        buttons_layout = QtWidgets.QHBoxLayout()
        group_box_layout.addLayout(buttons_layout)
        
        self.start_btn = QtWidgets.QToolButton()
        self.pause_btn = QtWidgets.QToolButton()
        
        self.add_button(
            parent=buttons_layout, btn=self.start_btn, btn_txt='Start Monitor', btn_connect=self._start_detection)
        self.add_button(
            parent=buttons_layout, btn=self.pause_btn, btn_txt='Pause Monitor', btn_connect=self._pause_detection)
        self.pause_btn.setEnabled(False)
        
        buttons_layout.setAlignment(QtCore.Qt.AlignLeft)
        
    def set_summary_layout(self, parent: QtWidgets.QLayout):
        group_box = QtWidgets.QGroupBox('Detced Dog and Cat live...')
        parent.addWidget(group_box)
        
        summary_layout = QtWidgets.QVBoxLayout()
        group_box.setLayout(summary_layout)
        
        self.dog_count_label = QtWidgets.QLabel('0', alignment=QtCore.Qt.AlignLeft)
        self.cat_count_label = QtWidgets.QLabel('0', alignment=QtCore.Qt.AlignLeft)
        
        summary_layout.addWidget(self.dog_count_label)
        summary_layout.addWidget(self.cat_count_label)
        
        summary_layout.addStretch()
        
    def _update_count(self, detected_classes: List[DetectedClass]):
        for det_cls in detected_classes:
            if det_cls.class_name == self.detection_classes[0]:
                self._increase_cat_count()
            elif det_cls.class_name == self.detection_classes[1]:
                self._increase_dog_count()
        
    def _increase_cat_count(self):
        self._cat_count += 1
        self.cat_count_label.setText(f'Total predicted Cats: {self._cat_count}')
        
    def _increase_dog_count(self):
        self._dog_count += 1
        self.dog_count_label.setText(f'Total predicted Dogs: {self._dog_count}')
        
    @staticmethod
    def add_button(parent: QtWidgets.QLayout, btn: QtWidgets.QToolButton, btn_txt: str, btn_connect: callable):
        btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        parent.addWidget(btn)
        
        btn_action = QtGui.QAction(text=btn_txt)
        btn_action.triggered.connect(btn_connect)
        btn.setDefaultAction(btn_action)

        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main_win = MainWindow(live_cam=False)
    main_win.configure()
    main_win.show()

    sys.exit(app.exec())