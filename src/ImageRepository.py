import pickle

import cv2


image_source = "..\\img\\"


class ImageRepository:
    dump_folder = '../img/dumps/'

    @staticmethod
    def get_set(set_num):
        first = cv2.imread(image_source + str(set_num) + "_left.jpg")
        second = cv2.imread(image_source + str(set_num) + "_right.jpg")
        return first, second

    @staticmethod
    def get_img(img_name):
        img = cv2.imread(image_source + img_name)
        return img

    @staticmethod
    def dump(obj, file):
        with open(ImageRepository.dump_folder + file + '.pkl', "wb") as f:
            pickle.dump(obj, f)

    @staticmethod
    def from_dump(file):
        with open(ImageRepository.dump_folder + file + '.pkl', "rb") as f:
            return pickle.load(f)
