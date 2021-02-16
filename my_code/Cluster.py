import numpy as np


class Cluster:
    def __init__(self, cluster_id):
        self.boxes = []
        self.cluster_id = cluster_id
        self.texts = []
        self.best_records_match = []
        self.confidence_value = None
        self.barcode_assigment = None

    def calc_cluster_center(self):
        center = np.array([0.0, 0.0])
        for box in self.boxes:
            b_c = np.array(box.calc_center())
            center += b_c
        center = center / len(self.boxes)
        return center

    def add_box(self, box):
        self.boxes.append(box)

    def get_boxes(self):
        return self.boxes

    def get_cluster_id(self):
        return self.cluster_id

    def add_text(self, text):
        self.texts.append(text)

    def get_texts(self):
        return self.texts

    def get_best_records_match(self):
        return self.best_records_match

    def add_best_record_match(self, record):
        self.best_records_match += [record]

    def get_best_barcodes_match(self):
        barcodes = []
        for r in self.best_records_match:
            barcodes.append(r[0][0])
        return barcodes

    def set_confidence_value(self, conf):
        self.confidence_value = conf

    def get_confidence_value(self):
        return self.confidence_value

    def set_barcode_assigment(self, bar):
        self.barcode_assigment = bar

    def get_barcode_assigment(self):
        return self.barcode_assigment