import cv2
import numpy as np
from skimage.segmentation import felzenszwalb, mark_boundaries

from MultiImageViewer import ImageBuilder
from Area import Area
from utils import generate_areas, view, write_area_to_file


class Image:
    def __init__(self, src: np.ndarray):
        self.src = src
        self.segmap = felzenszwalb(self.src, scale=300, sigma=1.5, min_size=100)
        self.areas = generate_areas(self.segmap)
        if len(np.unique(self.segmap)) != len(self.areas):
            print("Image init fault")
        i = 0
        for area in self.areas.values():
            area.calc_p_grid(self.segmap)
"""
            if area.mark == 227:
                print(area.mark)
                print(area.min, area.max)
                print(area.p_grid)
                print()
                src_roi = self.src[area.min[0]-5:area.max[0] + 6, area.min[1]-5:area.max[1] + 6]
                seg_roi = self.segmap[area.min[0]-5:area.max[0] + 6, area.min[1]-5:area.max[1] + 6] == area.mark
                view(mark_boundaries(src_roi, seg_roi.astype(int)))
                write_area_to_file(self.segmap, area.min, area.max)
"""

