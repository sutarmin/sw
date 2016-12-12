import pickle
import numpy as np
import cv2


class ImageRepository:
    image_source = '../img/'

    @staticmethod
    def get_set(set_num):
        first = cv2.imread(ImageRepository.image_source + str(set_num) + "_left.jpg")
        second = cv2.imread(ImageRepository.image_source + str(set_num) + "_right.jpg")
        return first, second

    @staticmethod
    def get_img(img_name):
        img = cv2.imread(ImageRepository.image_source + img_name)
        return img

    @staticmethod
    def dump(obj: np.ndarray, filename: str):
        if obj.dtype != 'int64':
            raise TypeError('I can only dump results of quickshift segmentation!')

        res = np.zeros((obj.shape[0], obj.shape[1], 3), np.uint8)
        for x in range(obj.shape[0]):
            for y in range(obj.shape[1]):
                val = obj.item((x, y))
                r_val = val // (256 ** 2)
                g_val = (val % (256 ** 2)) // 256
                b_val = (val % (256 ** 2)) % 256
                res.itemset((x, y, 0), r_val)
                res.itemset((x, y, 1), g_val)
                res.itemset((x, y, 2), b_val)

        path = ImageRepository.image_source + filename + '.png'
        cv2.imwrite(path, res)

    @staticmethod
    def from_dump(filename: str):
        dump = cv2.imread(ImageRepository.image_source + filename + '.png')
        res = np.zeros((dump.shape[0], dump.shape[1]), np.int64)
        for x in range(dump.shape[0]):
            for y in range(dump.shape[1]):
                val = dump.item((x, y, 2))
                val += dump.item((x, y, 1)) * 256
                val += dump.item((x, y, 0)) * 256 ** 2
                res.itemset((x, y), val)

        return res
