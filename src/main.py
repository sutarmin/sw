import numpy as np
import cv2
from matplotlib import pyplot as plt
from skimage import exposure
from utils import *


def effort1():
    right = cv2.imread('..\\..\\..\\image_lib\\1_right.jpg')
    left = cv2.imread('..\\..\\..\\image_lib\\1_left.jpg')
    cv2.imshow('src right', right)
    cv2.imshow('src left', left)
    right2 = quantize(right, 3)
    left2 = quantize(left, 3)
    # clahe_right2 = get_clahe_from_rgb_image(right2)
    # cv2.imwrite('res.jpg', clahe_right2)
    # cv2.imshow('right2', get_clahe_from_rgb_image(right2))
    # cv2.imshow('left2', get_clahe_from_rgb_image(left2))
    p2, p98 = np.percentile(right2, (2, 98))
    img_rescale = exposure.rescale_intensity(right2, in_range=(p2, p98))
    cv2.imshow('res', img_rescale)
    show_hist_ex(img_rescale)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def segmentation(img: np.ndarray):
    # graph initialization
    res = prepare_img(img)
    height = res.shape[0]
    width = res.shape[1]

    # tmp_table stores relative positions of Segments
    # needed to avoid searching Segments by exhaustive search
    tmp_table = []
    graph = SegmentGraph()
    for i in range(height):
        tmp_table.append([])
        for j in range(width):
            s = Segment()
            s.add_point((i, j))
            tmp_table[i].append(s)
            graph.add_vertex(s)
    for i in range(height - 1):
        for j in range(width - 1):
            graph.add_edge((tmp_table[i][j], tmp_table[i + 1][j]))
            graph.add_edge((tmp_table[i][j], tmp_table[i][j + 1]))

    # graph processing
    border_arr = get_mutal_border()
    for pair in border_arr:
        first = pair[0]
        second = pair[1]
        res.item(first)


def watershed_segmentation(name: str, img: np.ndarray):
    prepared = prepare_img(img)
    gray = cv2.cvtColor(prepared, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imshow(name, thresh)


if __name__ == '__main__':
    effort1()
