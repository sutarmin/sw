import cv2


image_source = "..\\img\\"


class ImageRepository:

    @staticmethod
    def get_set(set_num):
        first = cv2.imread(image_source + str(set_num) + "_left.jpg")
        second = cv2.imread(image_source + str(set_num) + "_right.jpg")
        return first, second

    @staticmethod
    def get_img(img_name):
        img = cv2.imread(image_source + img_name)
        return img
