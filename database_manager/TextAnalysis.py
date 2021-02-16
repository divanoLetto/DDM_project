from database_manager.DistanceStrategy import DistanceStrategy
from database_manager.LevenshteinDistance import LevenshteinDistance
from database_manager.LibraryManagerTool import LibraryManagerTool
from collections import defaultdict
import math


class TextAnalysis:

    def __init__(self, library):
        self.library_manager_tool = LibraryManagerTool(library)

    def get_closest_elements(self, string):
        distance_analysis = DistanceStrategy(string)
        distance_analysis.set_strategy(LevenshteinDistance())
        minn = math.inf
        closest_records = []
        for index in range(self.library_manager_tool.get_number_records()):
            record = self.library_manager_tool.get_record(index)
            for col, target in enumerate(record):
                # we don't consider the barcode that is not presente in the book shelf
                if col != 0 and col!= 3:
                    for word in target:
                        distance = distance_analysis.compute_distance(word)
                        if distance < minn:
                            minn = distance
                            closest_records = [record]
                        elif distance == minn and all(record[0][0] != x[0][0] for x in closest_records):
                            closest_records.append(record)
        return closest_records, minn

    def get_closest_elements_in_range(self, string, id1, id2):
        distance_analysis = DistanceStrategy(string)
        distance_analysis.set_strategy(LevenshteinDistance())
        minn = math.inf
        closest_records = []
        for index in range(id1, id2):
            record = self.library_manager_tool.get_record(index)
            for col, target in enumerate(record):
                # we don't consider the barcode that is not presente in the book shelf
                if col != 0:
                    for word in target:
                        distance = distance_analysis.compute_distance(word)
                        if distance < minn:
                            minn = distance
                            closest_records = [record]
                        elif distance == minn:
                            closest_records.append(record)
        return closest_records, minn