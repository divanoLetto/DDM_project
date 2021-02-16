import tensorflow as tf
import os
import numpy as np
from my_code.settings import OUTPUT_PATH, PREPROCESSED_PATH, CHECKPOINT_PATH

FLAGS = tf.app.flags.FLAGS


def fix_flags():
    FLAGS.test_data_path = PREPROCESSED_PATH
    FLAGS.checkpoint_path = CHECKPOINT_PATH
    FLAGS.output_dir = OUTPUT_PATH


def remove_tmp_files():
    for file_name in os.listdir(PREPROCESSED_PATH):
        if file_name.split(".")[-1].lower() in {"jpeg", "jpg", "png"}:
            try:
                image_name = PREPROCESSED_PATH + file_name
                os.remove(image_name)
            except:
                pass


def append_id(filename, id):
    name, ext = os.path.splitext(filename)
    return "{name}_{uid}{ext}".format(name=name, uid=id, ext=ext)


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def is_image(image_name):
    if image_name.split(".")[-1].lower() in {"jpeg", "jpg", "png"}:
        return True
    else:
        return False


def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False


def find_in(list, filter):
    for x in list:
        if filter(x):
            return x
    return None


class Collocation:
    def __init__(self, number, author):
        self.number = number
        self.author = author

    def __ge__(self, other):
        if self.number > other.number:
            return True
        elif self.number == other.number and (self.author == other.author or self.author > other.author):
            return True
        return False

    def __le__(self, other):
        if self.number < other.number:
            return True
        elif self.number == other.number and (self.author == other.author or self.author < other.author):
            return True
        return False

    def __gt__(self, other):
        if self.number > other.number:
            return True
        elif self.number == other.number:
            if self.author > other.author:
                return True
        return False

    def __lt__(self, other):
        if self.number < other.number:
            return True
        elif self.number == other.number:
            if self.author < other.author:
                return True
        return False

    def __eq__(self, other):
        if self.number == other.number and self.author == other.author:
            return True
        return False


def get_collocation_from_barcode(df, barcode):
    splt = ((df.loc[df['barcode'] == barcode])["collocation"].values[0]).split()
    if len(splt) >= 2:
        try:
            collocation = Collocation(float(splt[0]), splt[1])
        except:
            collocation = Collocation(float(100000), splt[0])
    else:
        head = float(splt[0].rstrip('0123456789'))
        tail = splt[0][len(head):]
        collocation = Collocation(head, tail)
    return collocation

