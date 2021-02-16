from my_code.settings import INPUT_PATH, PREPROCESSED_PATH
from PIL import Image


def rotate_img(img_path, rt_degr):
                img = Image.open(img_path)
                return img.rotate(rt_degr, expand=1)


def rotate_images(image_name):
            image_path = INPUT_PATH + image_name
            img_rt_90 = rotate_img(image_path, 90)
            image_path_to_save = PREPROCESSED_PATH + image_name
            img_rt_90.save(image_path_to_save)


def preprocess_image(image_name):
    rotate_images(image_name)