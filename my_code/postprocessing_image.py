import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)

    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


def resize_to_height_30(image):
    height = image.shape[0]
    width = image.shape[0]
    nw = (int(width * 30 / height), 30)
    resized = cv2.resize(image, nw)
    return resized


def color_distance(rgb1, rgb2):
    rm = 0.5*(rgb1[0]+rgb2[0])
    d = sum((2 + rm, 4, 3-rm)*(rgb1-rgb2)**2)**0.5
    return d


def image_from_clusters_color(image, n_clusters):
    tmp_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    tmp_img = tmp_img.reshape((tmp_img.shape[0] * tmp_img.shape[1], 3))
    clt = KMeans(n_clusters=n_clusters)
    clt.fit(tmp_img)
    centers = clt.cluster_centers_
    counts = clt.labels_
    dictionary_counts = Counter(counts)

    best_centroid = dictionary_counts.most_common(1)[0][0]
    for i, _ in enumerate(tmp_img):
        if counts[i] == best_centroid:
            tmp_img[i] = (255, 255, 255)
        else:
            tmp_img[i] = (0, 0, 0)
    new_img = tmp_img.reshape((image.shape[0], image.shape[1], 3))
    return new_img


