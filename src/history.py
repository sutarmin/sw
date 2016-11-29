import numpy as np
import cv2
from matplotlib import pyplot as plt
import skimage
from skimage import exposure, morphology, color
from utils import normalize_hist, show_hist_ex, quantize
from ImageRepository import ImageRepository as Repo


def effort1(img):
    """
    Первая попытка подготовки изображений
    1. Квантование
    2. Расширение гистограммы (маловажно)
    3. Перевод в градации серого
    4. Адаптивная бинаризация
    5. Удаление мелких объектов и дыр

    Вывод: при семешении 3 каналов в градации серого теряется очень много информации
    Нужно работать с каждым цветовым каналом отдельно
    """
    img = quantize(img, 5)
    img = normalize_hist(img)

    cv2.namedWindow("tool " + str(effort1.winname), cv2.WINDOW_NORMAL)
    cv2.resizeWindow("tool " + str(effort1.winname), 1800, 1000)

    cv2.imshow("tool " + str(effort1.winname), img)

    img2 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.waitKey(0)
    cv2.imshow("tool " + str(effort1.winname), img2)

    th3 = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.waitKey(0)
    cv2.imshow("tool " + str(effort1.winname), th3)

    img3 = morphology.remove_small_objects(th3.astype(bool))
    img4 = morphology.remove_small_holes(img3)
    cv2.waitKey(0)
    #  cv2.namedWindow("tool2 " + str(prepare.winname), cv2.WINDOW_NORMAL)
    #  cv2.resizeWindow("tool2 " + str(prepare.winname), 1800, 1000)
    #  cv2.imshow("tool2 " + str(prepare.winname), th3 - skimage.img_as_ubyte(img4))
    cv2.imshow("tool " + str(effort1.winname), skimage.img_as_ubyte(img4))

    cv2.waitKey(0)
    effort1.winname += 1


effort1.winname = 0