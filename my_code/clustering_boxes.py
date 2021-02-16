import cv2
from sklearn.cluster import DBSCAN
import numpy as np
import random
from my_code.settings import CLUSTERED_PATH, WEIGHTED_DISTANCE_CLUSTERING, Y_WEIGHT


def weightedL2(a, b):
    w = np.array([1, Y_WEIGHT])
    q = a - b
    return np.sqrt((w * q * q).sum())


def cluster_boxes(radius, boxes):
    """Cluster box by DBSCAN algorithm with weighted euclidean distance"""
    vertex = []
    for b in boxes:
        vertex.append(b.x0)
        vertex.append(b.x1)
        vertex.append(b.x2)
        vertex.append(b.x3)
    if WEIGHTED_DISTANCE_CLUSTERING:
        clustering = DBSCAN(eps=radius, min_samples=2, metric='wminkowski', p=2, metric_params={'w': np.array([1, Y_WEIGHT])}, algorithm='auto').fit(vertex)
    else:
        clustering = DBSCAN(eps=radius, min_samples=2, metric='euclidean', metric_params=None, algorithm='auto').fit(vertex)
    labels = clustering.labels_
    # change the outlayer's labels=-1 to a normal cluster of one point
    max_lab = max(labels) + 1
    for lab_id, lab in enumerate(labels):
        if lab == -1:
            labels[lab_id] = max_lab
            max_lab += 1
    # uniform the points of clusters that belong to the same box
    for i in range(0, len(labels), 4):
        current_label = labels[i]
        for j in range(1, 4):
            uniform_labels_cascade(labels, current_label, i + j)
    labels_boxes = []
    for i in range(0, len(labels), 4):
        labels_boxes.append(labels[i])
    return labels_boxes


def uniform_labels_cascade(labels, lab, j):
    """uniform all boxes labels that belongs to the same box"""
    if labels[j] == lab:
        return
    tmp = labels[j]
    labels[j] = lab

    for l in range(len(labels)):
        if labels[l] == tmp and labels[l] != -1:
            uniform_labels_cascade(labels, lab, l)

    rest = j % 4
    start = (j - rest)
    for i in range(4):
        uniform_labels_cascade(labels, lab, start + i)


def draw_image_with_clusters(image, boxes, vertex, labels, no_clusters, radius, name):
    # draw the results boxes with circles and lines
    colors = []
    for i in range(no_clusters + 1):
        random_col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        colors.append(random_col)
    red = (255, 0, 0)
    for i, v in enumerate(vertex):
        image = cv2.circle(image, tuple(v), radius, color=red, thickness=3)
        image = cv2.putText(image, text=str(labels[i]), org=(v[0]+5, v[1]-5), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, color=(36, 255, 12), thickness=2)
        image = cv2.putText(image, text=str(i), org=(v[0]-25, v[1]-10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, color=(0, 0, 0), thickness=2)
    for i in range(len(boxes)):
        box = boxes[i]
        if labels[i * 4] != -1:
            color = colors[labels[i * 4]]
        else:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pts = np.array([box.x0, box.x1, box.x2, box.x3])
        pts = pts.reshape((-1, 1, 2))
        image = cv2.polylines(image, [pts], True, color=color, thickness=3)
    cv2.imwrite(CLUSTERED_PATH + name, image)







