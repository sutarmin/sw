import numpy as np
import cv2

from SementGraph import Segment, SegmentGraph


def decrease_depth(src: np.ndarray, col_number):
    times = 256 / col_number
    res = src.copy()
    shape = src.shape
    width = shape[0]
    height = shape[1]
    for chanel in range(shape[2]):
        for w in range(width):
            for h in range(height):
                val = res.item((w, h, chanel))
                res.itemset((w, h, chanel), (val // times) * times)
    return res


def get_clahe_from_rgb_image(src: np.ndarray):
    clahe_filter = cv2.createCLAHE()
    src_b = src[:, :, 0]
    src_g = src[:, :, 1]
    src_r = src[:, :, 2]
    clahe_src_r = clahe_filter.apply(src_r)
    clahe_src_g = clahe_filter.apply(src_g)
    clahe_src_b = clahe_filter.apply(src_b)
    res = np.stack((clahe_src_b, clahe_src_g, clahe_src_r), axis=2)
    return res


def prepare_img(img):
    res = decrease_depth(img, 5)
    res = get_clahe_from_rgb_image(res)
    return res


def effort1():
    right = cv2.imread('..\\..\\image_lib\\0_right.jpg')
    left = cv2.imread('..\\..\\image_lib\\0_left.jpg')
    cv2.imshow('src right', right)
    cv2.imshow('src left', left)
    right2 = decrease_depth(right, 5)
    left2 = decrease_depth(left, 5)
    clahe_right2 = get_clahe_from_rgb_image(right2)
    cv2.imwrite('res.jpg', clahe_right2)
    cv2.imshow('right2', get_clahe_from_rgb_image(right2))
    cv2.imshow('left2', get_clahe_from_rgb_image(left2))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def segmentation(img: np.ndarray):
    res = prepare_img(img)
    height = res.shape[0]
    width = res.shape[1]
    table = []
    graph = SegmentGraph()
    for i in range(height):
        table.append([])
        for j in range(width):
            s = Segment()
            s.add_point((i, j))
            table[i].append(s)
            graph.add_vertex(s)
    for i in range(height - 1):
        for j in range(width - 1):
            graph.add_edge((table[i][j], table[i + 1][j]))
            graph.add_edge((table[i][j], table[i][j + 1]))


if __name__ == '__main__':
    right = cv2.imread('..\\..\\..\\image_lib\\0_right.jpg')
    segmentation(right)
