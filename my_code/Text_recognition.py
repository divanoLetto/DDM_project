import os
import cv2
import numpy as np
import pytesseract
from my_code.Box import Box
from my_code.Cluster import Cluster
from my_code.Geometric_correction import geometric_area_filtering, geometric_clustering_by_box_intersection, draw_clusters, geometric_clustering_by_circles_intersection
from my_code.clustering_boxes import cluster_boxes
from my_code.postprocessing_image import get_grayscale, thresholding, opening, canny, image_from_clusters_color
from my_code.settings import OUTPUT_PATH, PREPROCESSED_PATH, INPUT_PATH, WEIGHTED_DISTANCE_CLUSTERING, Y_WEIGHT, RADIUS
from my_code.text_filtering import out_string_noise, banished_characters_for_ocr, remove_banish_character, \
    remove_small_ward
from my_code.utils import find_in


def image_2_text(image, show_image_flag, verbose):
    """Get texts from image boxe using Google tesseract"""
    size_threshold = 2
    custom_oem_psm_config = r'--oem 3 --psm 8'
    orginal_str = pytesseract.image_to_string(image, lang="ita+eng", config=custom_oem_psm_config)
    orginal_str = out_string_noise(orginal_str, banished_characters_for_ocr)
    orginal_str = remove_small_ward(orginal_str, size_threshold)
    if len(orginal_str) > 0:
        if verbose:
            print("Tessact on original crop: " + orginal_str)
        if show_image_flag:
            cv2.imshow('Image', image)
            cv2.waitKey(0)
        return orginal_str
    gray = get_grayscale(image)
    gray_str = pytesseract.image_to_string(gray, lang="ita+eng", config=custom_oem_psm_config)
    gray_str = out_string_noise(gray_str, banished_characters_for_ocr)
    gray_str = remove_small_ward(gray_str, size_threshold)
    if len(gray_str) > 0:
        if verbose:
            print("Tessact on grayscale crop: " + gray_str)
        if show_image_flag:
            cv2.imshow('Image', gray)
            cv2.waitKey(0)
        return gray_str
    thresh = thresholding(gray)
    thresh_str = pytesseract.image_to_string(thresh, lang="ita+eng", config=custom_oem_psm_config)
    thresh_str = out_string_noise(thresh_str, banished_characters_for_ocr)
    thresh_str = remove_small_ward(thresh_str, size_threshold)
    if len(thresh_str) > 0:
        if verbose:
            print("Tessact on threasholding crop: " + thresh_str)
        if show_image_flag:
            cv2.imshow('Image', thresh)
            cv2.waitKey(0)
        return thresh_str
    else:
        if verbose:
            print("No method ricognise this box")
        if show_image_flag:
            cv2.imshow('Image', image)
            cv2.waitKey(0)
        return None


def text_recognition(image_name):
    radice_text_name = OUTPUT_PATH + image_name
    text_name = os.path.splitext(radice_text_name)[0] + str(".txt")
    image_path = PREPROCESSED_PATH + image_name
    img = cv2.imread(image_path)

    # get boxex info from txt files
    boxes = Box.list_boxes_from_txt(text_name)
    print("In " + str(image_name) + " are found " + str(len(boxes))+ " boxes")
    boxes.sort()

    # filtering: too small boxes are removed
    ratio_factor = 12  # finetuned value
    boxes = geometric_area_filtering(boxes, ratio_factor)

    # clustering boxex found with EAST
    radius = RADIUS
    if WEIGHTED_DISTANCE_CLUSTERING:
        radius = radius * Y_WEIGHT

    labels_boxes = cluster_boxes(radius, boxes)
    labels_boxes = geometric_clustering_by_box_intersection(boxes, labels_boxes)
    labels_boxes = geometric_clustering_by_circles_intersection(boxes, labels_boxes, radius)
    draw_clusters(img.copy(), image_name, radius, boxes, labels_boxes)

    clusters = []
    for i, box in enumerate(boxes):
        print("Elaborating box " + str(i+1) + "/" + str(len(boxes)))
        warped = box.rotate_and_warp_text_box(img.copy())
        text = image_2_text(warped, show_image_flag=False, verbose=False)
        if text is not None:
            box_cluster_id = labels_boxes[i]
            cluster = find_in(clusters, lambda c: c.get_cluster_id() == box_cluster_id)
            if cluster is None:
                cluster = Cluster(box_cluster_id)
                clusters.append(cluster)
            cluster.add_text(text)
            cluster.add_box(box)
    # remove empty boxes
    to_remove = []
    for clus in clusters:
        if len(clus.get_texts()) == 0:
            to_remove.append(clus)
    for useless_clus in to_remove:
        clusters.remove(useless_clus)

    return clusters


