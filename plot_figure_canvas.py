from typing import Callable

import numpy as np
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
from matplotlib.backends.backend_qt5agg import FigureCanvas


# TODO: get time diff as milisec
# TODO: call it

class PlotFigureCanvas(anim.FuncAnimation):

    def __init__(self, x_len:int, y_range:list, interval:int,
                 set_cat_count: Callable[[int], None], set_dog_count: Callable[[int], None]) -> None:

        self.canvas = FigureCanvas(mpl_fig.Figure())
        self._x_len_ = x_len
        self._y_range_ = y_range
        self.interval = interval
        self._set_cat_count = set_cat_count
        self._set_dog_count = set_dog_count

        x = list(range(0, x_len))
        y = [0] * x_len

        self._ax_  = self.canvas.figure.subplots()
        
        self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        self._line_, = self._ax_.plot(x, y)

        self.animation = anim.FuncAnimation(self.canvas.figure, self._update_canvas_, fargs=(y,), interval=interval, blit=True)
        return

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        # TODO: Call image process method from here and capture the process time
        # TODO: Think how I will show the detail if use select to show capture summery
        
        new_point = round(get_next_datapoint(), 2)
        
        y.append(new_point)     # Add new datapoint
        y = y[-self._x_len_:]                        # Truncate list _y_
        self._line_.set_ydata(y)
        
        self._set_cat_count(i)
        self._set_dog_count(int(new_point))
        return self._line_,
    


# Data source
# ------------
n = np.linspace(0, 499, 500)
d = 50 + 25 * (np.sin(n / 8.3)) + 10 * (np.sin(n / 7.5)) - 5 * (np.sin(n / 1.5))
i = 0
def get_next_datapoint():
    global i
    i += 1
    if i > 499:
        i = 0
    return d[i]