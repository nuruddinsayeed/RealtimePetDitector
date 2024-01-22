import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QLabel, QVBoxLayout, QWidget)
from matplotlib.artist import Artist
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np


class MplCanvas:

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_xlim(0, 2)
        self.axes.set_ylim(-2, 2)
        self.line,  = self.axes.plot([], [], lw=2)
        self.line.set_data([], [])
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.animation = FuncAnimation(
            self.fig, 
            func=self.draw_frame, 
            frames=200,
            interval=20, 
            blit=True, 
            cache_frame_data=False
        )

    def draw_frame(self, frame: int) -> list[Artist]:
        x = np.linspace(0, 5, 1000)
        y = np.sin(2 * np.pi * (x - 0.01 * frame))
        self.line.set_data(x, y)
        return [self.line]


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.text = QLabel("Hello World")
        self.text.setAlignment(Qt.AlignCenter)

        sc = MplCanvas(self, width=5, height=4, dpi=100)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(sc.canvas)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())