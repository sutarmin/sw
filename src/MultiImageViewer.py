import numpy as np
import cv2
from screeninfo import get_monitors


class ImageBuilder:
    instance_num = 1

    def __init__(self, winname=""):
        if winname == "":
            winname = "ImageBuilder " + str(ImageBuilder.instance_num)
            ImageBuilder.instance_num += 1

        self.winname = winname

        monitor = get_monitors()[0]
        self.width = monitor.width
        self.height = monitor.height

        self.canvas = np.zeros((self.height, self.width, 3), np.uint8)

    def draw(self, img: np.ndarray, x_parts, y_parts, position):
        if x_parts < 1 or y_parts < 1 or position < 1:
            raise ValueError("x_parts, y_parts and position should be positive")
        if position > x_parts * y_parts:
            raise ValueError("position should not be more then x_parts*y_parts. Given {0}>{1}*{2}"
                             .format(position, x_parts, y_parts))

        _x_pos = (position - 1) % x_parts
        _y_pos = (position - 1) // x_parts
        _width = self.width // x_parts
        _height = self.height // y_parts

        _img = cv2.resize(img, (_width, _height), interpolation=cv2.INTER_CUBIC)

        self.canvas[_y_pos * _height:(_y_pos + 1) * _height, _x_pos * _width:(_x_pos + 1) * _width] = _img

    def show(self, winname=""):
        _name = self.winname if winname == "" else winname

        cv2.namedWindow(_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(_name, 0, 0)
        cv2.resizeWindow(_name, self.width, self.height)
        cv2.imshow(_name, self.canvas)
        cv2.waitKey(0)
        cv2.destroyWindow(_name)

    def get(self):
        return self.canvas

    def save(self, filename=""):
        _filename = filename if filename != "" else self.winname
        cv2.imwrite(_filename, self.canvas)


imagebuilder = ImageBuilder()
