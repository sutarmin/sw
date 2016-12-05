import numpy as np
import cv2
from matplotlib import pyplot as plt
import skimage
from skimage import exposure, morphology, color

from handlers import normalize_hist, quantize, remove_small_areas, get_channel

"""
    Здесь массивы функций - способы обработки изображений
    каждая функция на верхнем уровне должна удовлетворять 2 требованиям:
     1. Принимать изображение и возвращать изображение, которое ожидает принять следующая функция;
     2. Возвращать изображение, которе может быть отображено с помощью utils -> view

    Для вложенных массивов условие 2 необязательно, но условие 1 необходимо выполнять
"""

"""
Попытка 1
1. Квантование
2. Расширение гистограммы (маловажно)
3. Перевод в градации серого
4. Адаптивная бинаризация
5. Удаление мелких объектов и дыр

Вывод: при семешении 3 каналов в градации серого теряется очень много информации
Нужно работать с каждым цветовым каналом отдельно
"""
effort1 = [
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


"""
Попытка 2
1. Квантование
2. Расширение гистограммы (маловажно)
3. Разделение по цветовым каналам
4. Адаптивная бинаризация (для каждого канала)
5. Удаление мелких объектов и дыр (для каждого канала)
"""


def effort2(channel: str):
    return [
        lambda img: quantize(img, 5),
        lambda img: normalize_hist(img),
        lambda img: get_channel(img, channel),
        # lambda img: cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2),
        # lambda img: remove_small_areas(img)
    ]
