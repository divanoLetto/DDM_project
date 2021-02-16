import random 
import cv2
import shapely as sp
import numpy as np
from shapely.geometry import Polygon, Point
import shapely.affinity
from my_code.settings import CLUSTERED_PATH, WEIGHTED_DISTANCE_CLUSTERING, Y_WEIGHT


def geometric_area_filtering(boxes, divider):
    """filter boxes with a area less than a dinamic threshold based on the biggest box area"""
    correct_boxes = []
    mx = -1
    for box in boxes:
        polygon = Polygon([box.x0, box.x1, box.x2, box.x3])
        if polygon.area > mx:
            mx = polygon.area
    for box in boxes:
        polygon = Polygon([box.x0, box.x1, box.x2, box.x3])
        if polygon.area >= mx / divider:
            correct_boxes.append(box)
    return correct_boxes


def geometric_clustering_by_box_intersection(boxes, labels_boxes):
    """unite to the same cluster boxes that have a intersection != 0"""
    mx = max(labels_boxes)+1
    for id_1, box_1 in enumerate(boxes):
        polygon1 = Polygon([box_1.x0, box_1.x1, box_1.x2, box_1.x3])
        for id_2, box_2 in enumerate(boxes):
            if id_1 != id_2:
                if labels_boxes[id_1] != labels_boxes[id_2] or (labels_boxes[id_1] == -1 and labels_boxes[id_2] == -1):
                    polygon2 = Polygon([box_2.x0, box_2.x1, box_2.x2, box_2.x3])
                    if polygon1.intersects(polygon2):
                        tmp = labels_boxes[id_2]
                        if tmp == -1:
                            labels_boxes[id_1] = mx
                            labels_boxes[id_2] = mx
                            mx += 1
                        else:
                            for label_id, label in enumerate(labels_boxes):
                                if label == tmp:
                                    labels_boxes[label_id] = labels_boxes[id_1]
    return labels_boxes


def geometric_clustering_by_circles_intersection(boxes, labels_boxes, radius):
    mx = max(labels_boxes) + 1
    for id_1, box_1 in enumerate(boxes):
        vertexs = [box_1.x0, box_1.x1, box_1.x2, box_1.x3]
        for v in vertexs:
            circle = Point(v[0], v[1]).buffer(radius)
            if WEIGHTED_DISTANCE_CLUSTERING:
                circle = shapely.affinity.scale(circle, 1, 1/Y_WEIGHT)
            for id_2, box_2 in enumerate(boxes):
                if id_1 != id_2:
                    if labels_boxes[id_1] != labels_boxes[id_2] or (labels_boxes[id_1] == -1 and labels_boxes[id_2] == -1):
                        polygon2 = Polygon([box_2.x0, box_2.x1, box_2.x2, box_2.x3])
                        if circle.intersects(polygon2):
                            tmp = labels_boxes[id_2]
                            if tmp == -1:
                                labels_boxes[id_1] = mx
                                labels_boxes[id_2] = mx
                                mx += 1
                            else:
                                for label_id, label in enumerate(labels_boxes):
                                    if label == tmp:
                                        labels_boxes[label_id] = labels_boxes[id_1]
    return labels_boxes


def draw_clusters(image, image_name,radius,  boxes, labels_boxes):
    colors = []
    for i in range(len(boxes) + 100):
        random_col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        colors.append(random_col)
    red = (0, 0, 255)
    black = (0, 0, 0)
    count = 0
    offset_x = -25
    offset_y = -10
    for idxx, b in enumerate(boxes):
        idx = labels_boxes[idxx]
        col = colors[idx + 1]
        if not WEIGHTED_DISTANCE_CLUSTERING:
            image = cv2.circle(image, tuple(b.x0), radius, color=col, thickness=3)
            image = cv2.circle(image, tuple(b.x1), radius, color=col, thickness=3)
            image = cv2.circle(image, tuple(b.x2), radius, color=col, thickness=3)
            image = cv2.circle(image, tuple(b.x3), radius, color=col, thickness=3)
        else:
            image = cv2.ellipse(image, tuple(b.x0), (radius, int(radius/Y_WEIGHT)),angle = 0,startAngle = 0,endAngle = 360, color=col, thickness=6)
            image = cv2.ellipse(image, tuple(b.x1), (radius, int(radius/Y_WEIGHT)),angle = 0,startAngle = 0,endAngle = 360, color=col, thickness=6)
            image = cv2.ellipse(image, tuple(b.x2), (radius, int(radius/Y_WEIGHT)),angle = 0,startAngle = 0,endAngle = 360,  color=col, thickness=6)
            image = cv2.ellipse(image, tuple(b.x3), (radius, int(radius/Y_WEIGHT)),angle = 0,startAngle = 0,endAngle = 360,  color=col, thickness=6)

        # image = cv2.putText(image, text=str(labels_boxes[idxx]), org=tuple(b.x0), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, color=(36, 255, 12), thickness=2)
        # image = cv2.putText(image, text=str(labels_boxes[idxx]), org=tuple(b.x1), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, color=(36, 255, 12), thickness=2)
        # image = cv2.putText(image, text=str(labels_boxes[idxx]), org=tuple(b.x2), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, color=(36, 255, 12), thickness=2)
        # image = cv2.putText(image, text=str(labels_boxes[idxx]), org=tuple(b.x3), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, color=(36, 255, 12), thickness=2)
        # image = cv2.putText(image, text=str(count), org=tuple([b.x0[0]+offset_x, b.x0[1]+offset_y]), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, color=(0, 0, 0), thickness=2)

        # count += 1
        # image = cv2.putText(image, text=str(count), org=tuple([b.x1[0]+offset_x, b.x1[1]+offset_y]), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6,color=(0, 0, 0), thickness=2)
        # count += 1
        # image = cv2.putText(image, text=str(count), org=tuple([b.x2[0]+offset_x, b.x2[1]+offset_y]), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6,color=(0, 0, 0), thickness=2)
        # count += 1
        # image = cv2.putText(image, text=str(count), org=tuple([b.x3[0]+offset_x, b.x3[1]+offset_y]), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6,color=(0, 0, 0), thickness=2)
        # count += 1

    for id_1, box_1 in enumerate(boxes):
        idx = labels_boxes[id_1]
        col = colors[idx+1]
        pts = np.array([box_1.x0, box_1.x1, box_1.x2, box_1.x3])
        pts = pts.reshape((-1, 1, 2))
        image = cv2.polylines(image, [pts], True, color=col, thickness=7)

        image = cv2.drawMarker(image, tuple(box_1.x0), color=red, thickness=9, markerType=cv2.MARKER_CROSS)
        image = cv2.drawMarker(image, tuple(box_1.x1), color=red, thickness=9, markerType=cv2.MARKER_CROSS)
        image = cv2.drawMarker(image, tuple(box_1.x2), color=red, thickness=9, markerType=cv2.MARKER_CROSS)
        image = cv2.drawMarker(image, tuple(box_1.x3), color=red, thickness=9, markerType=cv2.MARKER_CROSS)

    cv2.imwrite(CLUSTERED_PATH + image_name, image)






