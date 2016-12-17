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

    def draws(self, img: np.ndarray, short_pos: int):
        if short_pos < 111 or short_pos > 999:
            raise ValueError("short_pos should be between 111 and 999")
        x_parts = short_pos // 100
        y_parts = short_pos % 100 // 10
        position = short_pos % 10
        self.drawo(img, x_parts, y_parts, position)

    def drawo(self, img: np.ndarray, x_parts: int, y_parts: int, order: int):
        if x_parts < 1 or y_parts < 1 or order < 1:
            raise ValueError("x_parts, y_parts and position should be positive")
        if order > x_parts * y_parts:
            raise ValueError("position should not be more then x_parts*y_parts. Given {0}>{1}*{2}"
                             .format(order, x_parts, y_parts))

        _x_pos = (order - 1) % x_parts
        _y_pos = (order - 1) // x_parts
        self.draw(img, (x_parts, y_parts), (_x_pos, _y_pos))

    def draw(self, img: np.ndarray, parts: tuple, position: tuple):
        """
        Добавляет полученное изображение на холст
        :param img: изображение
        :param parts: 2 числа - высота и цширина холста, измеряемые количеством изображений
        :param position: позиция текущего изображения на холсте.
        """
        if len(parts) != 2 or len(position) != 2:
            raise ValueError("lengths error")
        if parts[0] < position[0] or parts[1] < position[1]:
            raise ValueError("values error")

        _x_pos = position[0] - 1
        _y_pos = position[1] - 1
        _width = self.width // parts[0]
        _height = self.height // parts[1]

        _img = cv2.resize(img, (_width, _height), interpolation=cv2.INTER_CUBIC)

        # приводим к единому формату, если получили не-rgb изображение
        if len(_img.shape) != 3:
            _img = cv2.merge((_img, _img, _img))

        self.canvas[_y_pos * _height:(_y_pos + 1) * _height, _x_pos * _width:(_x_pos + 1) * _width] = _img

    def drawnext(self, img):
        pass

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
