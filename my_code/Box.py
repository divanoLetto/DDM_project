import cv2
import numpy as np
from numpy.linalg import norm
from my_code.utils import normalize


class Box:
    """Class for the output boxes of EAST algorithm"""
    def __init__(self, x0, x1, x2, x3):
        self.x0 = x0
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.center = self.calc_center()
        self.spine_color = None
        self.text_color = None

    def calc_center(self):
        center = [self.x0[i] + self.x1[i] + self.x2[i] + self.x3[i] for i in range(len(self.x0))]
        center = [c/4 for c in center]
        return center

    def set_spine_color(self, color):
        self.spine_color = color

    def set_text_color(self, color):
        self.text_color = color

    def __lt__(self, other):
        soglia = -2
        if self.calc_center()[1] - other.calc_center()[1] < soglia:
            return self
        elif other.calc_center()[1] - self.calc_center()[1] < soglia:
            return other
        elif self.calc_center()[0] < other.calc_center()[0]:
            return self
        else:
            return other

    def get_long_direction(self):
        d0_1 = np.linalg.norm(self.x0, self.x1)
        d1_2 = np.linalg.norm(self.x1, self.x2)
        if d0_1 > d1_2:
            dir = normalize(np.array(self.x1) - np.array(self.x0))
        else:
            dir = normalize(np.array(self.x2) - np.array(self.x1))
        return dir

    def get_short_direction(self):
        d0_1 = np.linalg.norm(self.x0, self.x1)
        d1_2 = np.linalg.norm(self.x1, self.x2)
        if d0_1 < d1_2:
            dir = normalize(np.array(self.x1) - np.array(self.x0))
        else:
            dir = normalize(np.array(self.x2) - np.array(self.x1))
        return dir

    def rotate_and_warp_text_box(self, image):
        cnt = np.array([
            [self.x0], [self.x1], [self.x2], [self.x3]
        ])
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        width = int(rect[1][0])
        height = int(rect[1][1])
        src_pts = box.astype("float32")
        dst_pts = np.array([[0, height - 1],
                            [0, 0],
                            [width - 1, 0],
                            [width - 1, height - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv2.warpPerspective(image, M, (width, height))

        if norm(np.array(self.x0)-np.array(self.x1)) > norm(np.array(self.x0)-np.array(self.x3)) and width<height:
            warped = cv2.rotate(warped, cv2.cv2.ROTATE_90_CLOCKWISE)

        return warped

    @staticmethod
    def list_boxes_from_txt(text_name):
        boxes = []
        box_txt = open(text_name, 'r')
        lines = box_txt.readlines()
        for line in lines:
            coordinates = line.split(',')
            coordinates = [int(c) for c in coordinates]
            x0 = [coordinates[0], coordinates[1]]
            x1 = [coordinates[2], coordinates[3]]
            x2 = [coordinates[4], coordinates[5]]
            x3 = [coordinates[6], coordinates[7]]
            boxes.append(Box(x0, x1, x2, x3))
        return boxes
