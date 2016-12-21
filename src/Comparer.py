from Image import Image
import numpy as np
import cv2
from random import randint

from utils import draw_contour_on_region


class Comparer:
    def __init__(self, match_shapes_threshold=0.02, sigma=0):
        self.src_list = []
        self.compare_dict = {}
        self.__count = 0
        self.match_shapes_threshold = match_shapes_threshold
        self.sigma = sigma

    def add(self, _new_img: np.ndarray):
        new_img = Image(_new_img, self.sigma)

        if len(self.src_list) == 0:
            self.src_list.append(new_img)
            self.compare_dict[0] = {}
            return

        self.__count += 1
        for i, img in enumerate(self.src_list):
            for area1 in img.areas.values():
                for area2 in new_img.areas.values():
                    diff = 1
                    try:
                        diff = cv2.matchShapes(area1.contour, area2.contour, 1, 0)
                    except:
                        pass
                    if diff < self.match_shapes_threshold:
                        # print("Same!")
                        if self.__count not in self.compare_dict[i].keys():
                            self.compare_dict[i][self.__count] = []
                        if self.__count not in self.compare_dict.keys():
                            self.compare_dict[self.__count] = {}
                        if i not in self.compare_dict[self.__count].keys():
                            self.compare_dict[self.__count][i] = []

                        self.compare_dict[i][self.__count].append((area1.mark, area2.mark))
                        self.compare_dict[self.__count][i].append((area2.mark, area1.mark))
                        # draw_contour_on_region(area1.region, area1.contour, 2)
                        # write_area_to_file(area1.region, filename="area1.txt")

        self.src_list.append(new_img)

    def draw_diff(self, idx1: int, idx2: int):
        if idx1 not in self.compare_dict.keys():
            raise ValueError('index1 is out of bounds. Seems look nothiing to draw')
        if idx2 not in self.compare_dict[idx1].keys():
            raise ValueError('index2 is out of bounds. Seems look nothiing to draw')
        img1 = self.src_list[idx1]
        img2 = self.src_list[idx2]
        copy1 = np.array(img1.src)
        copy2 = np.array(img2.src)
        i = 0
        for contours in self.compare_dict[idx1][idx2]:
            print(cv2.contourArea(img1.areas[contours[0]].contour), img1.areas[contours[0]].contour)
            print(cv2.contourArea(img2.areas[contours[1]].contour), img2.areas[contours[1]].contour)
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
            cv2.drawContours(copy1, [img1.areas[contours[0]].contour], 0, color, thickness=2,
                             offset=tuple(img1.areas[contours[0]].min[::-1]))
            cv2.drawContours(copy2, [img2.areas[contours[1]].contour], 0, color, thickness=2,
                             offset=tuple(img2.areas[contours[1]].min[::-1]))
            i += 1
            if (i > 10):
                break
        cv2.putText(copy1, str(len(self.compare_dict[idx1][idx2])), (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                    thickness=2)
        return copy1, copy2
