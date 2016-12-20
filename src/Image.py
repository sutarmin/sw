import cv2
import numpy as np
from skimage.segmentation import felzenszwalb, mark_boundaries

from MultiImageViewer import ImageBuilder
from Area import Area
from utils import generate_areas, view, write_area_to_file, draw_contour_on_region


class Image:
    def __init__(self, src: np.ndarray):
        self.src = src
        self.segmap = felzenszwalb(self.src, scale=300, sigma=0.1, min_size=100)
        self.areas = generate_areas(self.segmap)
        if len(np.unique(self.segmap)) != len(self.areas):
            print("Image init fault")
        i = 0
        for area in self.areas.values():
            area.calc_contour(self.segmap)


def compare(img1: Image, img2: Image):

    for area1 in img1.areas.values():
        for area2 in img2.areas.values():
            if area1.mark == 0 or area2.mark == 0:
                continue

            diff = cv2.matchShapes(area1.contour, area2.contour, 1, 0)
            print(diff)
            if diff < 0.03:
                print("Same!")
                draw_contour_on_region(area1.region, area1.contour, 2)
                draw_contour_on_region(area2.region, area2.contour, 2)
                write_area_to_file(area1.region, filename="area1.txt")
                write_area_to_file(area2.region, filename="area2.txt")
                break

