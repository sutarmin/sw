import cv2
import numpy as np
from matplotlib import pyplot as plt


def view(img):
    cv2.namedWindow("view", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("view", 1800, 1000)
    cv2.imshow("view", img)
    cv2.waitKey(0)
    cv2.destroyWindow("view")


def process_yield(img, func_arr):
    for obj in func_arr:
        if callable(obj):
            img = obj(img)
        else:
            for child in process_yield(img, obj):
                img = child
        yield img


def process(img, func_arr):
    result = None
    for result in process_yield(img, func_arr):
        pass
    return result


# показывает картинку с гистограммой полученного изображения
def show_hist_ex(img: np.ndarray):
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        # plt.subplot(111)
        plt.plot(histr, color=col)
        plt.xlim([0, 256])

    plt.show()
