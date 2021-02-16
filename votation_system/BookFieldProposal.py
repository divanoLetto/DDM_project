import math
import random

from database_manager.LevenshteinDistance import LevenshteinDistance
from my_code.utils import find_in


class BookFieldProposal:
    def __init__(self, barcode, text):
        self.barcode = barcode
        self.text = text
        self.cluster = None

    def set_cluster(self, cluster):
        self.cluster = cluster

    def get_cluster(self):
        return self.cluster

    def get_texts(self):
        return self.text

    def get_barcode(self):
        return self.barcode


def match_clusters_kook_proposals(book_filed_proposal, all_book_filed_proposal, clusters):
    # find best BFP for each clusters
    if book_filed_proposal.get_cluster() is not None:
        return
    best_cluster, max_value = get_best_cluster_by_book_field_proposal(book_filed_proposal, clusters)
    # more BFP than clusters
    if best_cluster is None:
        return
    for other_bfp in all_book_filed_proposal:
        # if is not the same BFP
        if other_bfp.get_texts() != book_filed_proposal.get_texts() :
            # if there is a better BFP assign this cluster to it
            other_best_cluster, other_max_value = get_best_cluster_by_book_field_proposal(other_bfp, clusters)
            if other_best_cluster is not None and other_best_cluster.get_cluster_id() == best_cluster.get_cluster_id() and max_value < other_max_value and other_bfp. get_cluster() == None:
                match_clusters_kook_proposals(other_bfp, all_book_filed_proposal, clusters)
                match_clusters_kook_proposals(book_filed_proposal, all_book_filed_proposal, clusters)
                return
    book_filed_proposal.set_cluster(best_cluster)
    best_cluster.set_barcode_assigment(book_filed_proposal.barcode)


def get_best_cluster_by_book_field_proposal(book_filed_proposal, clusters):
    # find the best cluster for a given BFP
    dict_count = {}
    for word_field in book_filed_proposal.get_texts():
        best_assigments, min_distance = get_closest_clusters_by_word(word_field, clusters, book_filed_proposal.get_barcode())
        each_value = max((len(word_field) - min_distance) / len(word_field), 0)
        for clus in best_assigments:
            id = clus.get_cluster_id()
            if id in dict_count.keys():
                dict_count[id] += each_value
            else:
                dict_count[id] = each_value
    if len(dict_count.keys()) != 0:
        max_value = max(dict_count.values())
        max_clusters = [clus_id for clus_id, summ in dict_count.items() if summ == max_value]
        best_rand_cluster_id = max_clusters[random.randint(0, len(max_clusters)-1)]
        best_rand_cluster = find_in(clusters, lambda c: c.get_cluster_id() == best_rand_cluster_id)
        return best_rand_cluster, max_value
    else:
        return None, 0


def get_closest_clusters_by_word(word, clusters, word_barcode):
    # find the best cluster by a given word
    min_distance = math.inf
    lev_distance = LevenshteinDistance()
    best_assigments = []
    for clus in clusters:
        # if it is not already assigned
        if clus.get_barcode_assigment() is None or clus.get_barcode_assigment() == word_barcode:
            for word_clus in clus.get_texts():
                distance = lev_distance.compute_distance(word, word_clus)
                if distance < min_distance:
                    min_distance = distance
                    best_assigments = [clus]
                elif distance == min_distance and all(
                        clus.get_cluster_id() != x.get_cluster_id() for x in best_assigments):
                    best_assigments.append(clus)
    return best_assigments, min_distance







