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


def segmentation(img):
    res = prepare_img(img)
    for i in range(100):
        for j in range(100):
            for c in range(3):
                res.itemset((i, j, c), 0)
    cv2.imshow('Segmentation result', res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


seg1 = Segment()
seg1.add_point((0, 0))
seg2 = Segment()
seg2.add_point((0, 1))
seg2.add_point((1, 0))
seg3 = Segment()
seg3.add_point((1, 1))
graph = SegmentGraph()
graph.add_edge((seg1, seg2))
graph.add_edge((seg2, seg3))
# print(graph)

graph.unite_vertices(seg1, seg2)
print(graph)