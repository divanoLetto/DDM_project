import numpy


class LevenshteinDistance:
    def compute_distance(self, source, target):
        """  Levenshtein Distance between
                    source string and target string"""
        source = source.lower()
        target = target.lower()
        # create a new empty matrix with (len(source) + 1) rows
        # and (len(target) + 1) columns
        matrix_distances = numpy.zeros((len(source) + 1, len(target) + 1))
        # initialize the first column
        for source_index in range(len(source) + 1):
            matrix_distances[source_index][0] = source_index
        # initialize the first row
        for target_index in range(len(target) + 1):
            matrix_distances[0][target_index] = target_index

        a, b, c = 0, 0, 0
        # compute the levenshtein distance
        for source_index in range(1, len(source) + 1):
            for target_index in range(1, len(target) + 1):
                if source[source_index - 1] == target[target_index - 1]:
                    matrix_distances[source_index][target_index] = matrix_distances[source_index - 1][target_index - 1]
                else:
                    a = matrix_distances[source_index][target_index - 1]
                    b = matrix_distances[source_index - 1][target_index]
                    c = matrix_distances[source_index - 1][target_index - 1]
                    if a <= b and a <= c:
                        matrix_distances[source_index][target_index] = a + 1
                    elif b <= a and b <= c:
                        matrix_distances[source_index][target_index] = b + 1
                    else:
                        matrix_distances[source_index][target_index] = c + 1
        # get levenshtein distance
        return matrix_distances[len(source)][len(target)]
