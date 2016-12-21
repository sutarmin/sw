import cv2
import numpy as np
from skimage.segmentation import felzenszwalb, mark_boundaries

from MultiImageViewer import ImageBuilder
from Area import Area
from utils import generate_areas, view, write_area_to_file, draw_contour_on_region


class Image:
    def __init__(self, src: np.ndarray, sigma=0):
        self.src = src
        self.segmap = felzenszwalb(self.src, scale=300, sigma=sigma, min_size=100)
        self.areas = generate_areas(self.segmap)
        if len(np.unique(self.segmap)) != len(self.areas):
            print("Image init fault")
        i = 0
        for area in self.areas.values():
            area.calc_contour(self.segmap)

