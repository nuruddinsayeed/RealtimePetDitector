import sys
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

from plot_figure_canvas import PlotFigureCanvas


class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        
    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(1500, 600)
    
    def configure(self):
        self.setWindowTitle('Real Time Pet Monitor')
        self.frame = QtWidgets.QFrame(self)
        self.frame.setStyleSheet('QWidget { background-color: #eeeeec; }')
        
        layout = QtWidgets.QVBoxLayout()
        
        # self.set_button_layout(parent=layout)
        # self.set_summary_layout(parent=layout)
        self._init_header_ui(parent=layout)
        self.frame.setLayout(layout)
        self.setCentralWidget(self.frame)
        
        # Matplotlib Figure
        self.myFig = PlotFigureCanvas(x_len=200, y_range=[0, 600], interval=200, 
                                      set_cat_count=self._update_cat_count, set_dog_count=self._update_dog_count)
        layout.addWidget(self.myFig.canvas)  # TODO: update total detected info from canvas, find out how can you get the data
        
    def _init_header_ui(self, parent: QtWidgets.QLayout):
        group_box = QtWidgets.QGroupBox()
        parent.addWidget(group_box)
        
        group_box_layout = QtWidgets.QHBoxLayout()
        group_box.setLayout(group_box_layout)
        
        heading_layout = QtWidgets.QHBoxLayout()
        group_box_layout.addLayout(heading_layout)
        
        self.set_button_layout(parent=heading_layout)
        self.set_summary_layout(parent=heading_layout)
        
    def set_button_layout(self, parent: QtWidgets.QLayout):
        
        group_box = QtWidgets.QGroupBox()
        parent.addWidget(group_box)
        
        group_box_layout = QtWidgets.QHBoxLayout()
        group_box.setLayout(group_box_layout)
        
        buttons_layout = QtWidgets.QHBoxLayout()
        group_box_layout.addLayout(buttons_layout)
        
        self.start_btn = QtWidgets.QToolButton()
        self.stop_btn = QtWidgets.QToolButton()
        
        self.add_button(parent=buttons_layout, btn=self.start_btn, btn_txt='Start Monitor', btn_connect=lambda: True)
        self.add_button(parent=buttons_layout, btn=self.stop_btn, btn_txt='Stop Monitor', btn_connect=lambda: True)
        self.stop_btn.setEnabled(False)
        
        buttons_layout.setAlignment(QtCore.Qt.AlignLeft)
        
    def set_summary_layout(self, parent: QtWidgets.QLayout):
        group_box = QtWidgets.QGroupBox('Detced Dog and Cat live...')
        parent.addWidget(group_box)
        
        summary_layout = QtWidgets.QVBoxLayout()
        group_box.setLayout(summary_layout)
        
        self.dog_count_label = QtWidgets.QLabel('14', alignment=QtCore.Qt.AlignLeft)
        self.cat_count_label = QtWidgets.QLabel('20', alignment=QtCore.Qt.AlignLeft)
        
        summary_layout.addWidget(self.dog_count_label)
        summary_layout.addWidget(self.cat_count_label)
        
        summary_layout.addStretch()
        
    def _update_cat_count(self, count: int):
        self.cat_count_label.setText(f'Total predicted Cats: {count}')
        
    def _update_dog_count(self, count: int):
        self.dog_count_label.setText(f'Total predicted Dogs: {count}')
        
    @staticmethod
    def add_button(parent: QtWidgets.QLayout, btn: QtWidgets.QToolButton, btn_txt: str, btn_connect: callable):
        btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        parent.addWidget(btn)
        
        btn_action = QtGui.QAction(text=btn_txt)
        btn_action.triggered.connect(btn_connect)
        btn.setDefaultAction(btn_action)

        

if __name__ == '__main__':
    # qapp = QtWidgets.QApplication(sys.argv)
    # main_win = MainWindow()
    # main_win.configure()
    # main_win.show()
    # qapp.exec_()
    
    app = QtWidgets.QApplication(sys.argv)

    main_win = MainWindow()
    main_win.configure()
    main_win.show()

    sys.exit(app.exec())