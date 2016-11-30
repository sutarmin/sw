import numpy as np
import cv2
from matplotlib import pyplot as plt
import skimage
from skimage import exposure, morphology, color
from handlers import normalize_hist, show_hist_ex, quantize
from ImageRepository import ImageRepository as Repo


def view(img):
    cv2.namedWindow("view", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("view", 1800, 1000)
    cv2.imshow("view", img)
    cv2.waitKey(0)
    cv2.destroyWindow("view")


def process(img, func_arr):
    for obj in func_arr:
        if callable(obj):
            img = obj(img)
        else:
            for child in process(img, obj):
                img = child
        yield img


def prepare(img):
    """
    Первая попытка подготовки изображений
    1. Квантование
    2. Расширение гистограммы (маловажно)
    3. Выделение каждого канала
    4. Адаптивная бинаризация
    5. Удаление мелких объектов и дыр

    Вывод: при семешении 3 каналов в градации серого теряется очень много информации
    Нужно работать с каждым цветовым каналом отдельно
    """

    cv2.namedWindow("tool " + str(prepare.winname), cv2.WINDOW_NORMAL)
    cv2.resizeWindow("tool " + str(prepare.winname), 1800, 1000)

    cv2.imshow("tool " + str(prepare.winname), img)

    img = quantize(img, 5)
    cv2.waitKey(0)
    cv2.imshow("tool " + str(prepare.winname), img)

    img = normalize_hist(img)

    cv2.waitKey(0)
    cv2.imshow("tool " + str(prepare.winname), img)

    img2 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.waitKey(0)
    cv2.imshow("tool " + str(prepare.winname), img2)

    th3 = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.waitKey(0)
    cv2.imshow("tool " + str(prepare.winname), th3)

    img3 = morphology.remove_small_objects(th3.astype(bool))
    img4 = morphology.remove_small_holes(img3)
    cv2.waitKey(0)
    #  cv2.namedWindow("tool2 " + str(prepare.winname), cv2.WINDOW_NORMAL)
    #  cv2.resizeWindow("tool2 " + str(prepare.winname), 1800, 1000)
    #  cv2.imshow("tool2 " + str(prepare.winname), th3 - skimage.img_as_ubyte(img4))
    cv2.imshow("tool " + str(prepare.winname), skimage.img_as_ubyte(img4))

    cv2.waitKey(0)
    prepare.winname += 1


prepare.winname = 0

if __name__ == '__main__':
    first, second = Repo.get_set(0)
    func_arr = [
        lambda img: quantize(img, 5),
        lambda img: normalize_hist(img),
        lambda img: cv2.cvtColor(img, cv2.COLOR_RGB2GRAY),
        lambda img: cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2),
        [
            lambda img: morphology.remove_small_objects(img.astype(bool)),
            lambda img: morphology.remove_small_holes(img),
            lambda img: skimage.img_as_ubyte(img)
        ]
    ]

    # prepare(first)
    # prepare(second)

    for img in process(second, func_arr):
        view(img)

    cv2.destroyAllWindows()
    # show_hist_ex(img3)
