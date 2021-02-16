from database_manager.TextAnalysis import TextAnalysis
from my_code.settings import EXCEL_FILE
from my_code.Cluster import Cluster


def votation_system(clusters, text_analyser):
    count = 0
    #  è possibile parallelizzare questo codice per farlo andare n volte più veloce
    for cluster in clusters:
        print("Elaborating cluster " + str(count) + "/" + str(len(clusters)-1))
        count += 1
        barcode_dict = {}
        for word in cluster.get_texts():
            records, min_distance = text_analyser.get_closest_elements(word)
            # confidence value for each closest word found
            each_value = max((len(word) - min_distance) / len(word), 0)
            for record in records:
                barcode = record[0][0]
                if barcode in barcode_dict:
                    barcode_dict[barcode] += each_value
                else:
                    barcode_dict[barcode] = each_value

        if len(barcode_dict.keys()) != 0:
            max_value = max(barcode_dict.values())
            max_barcodes = [bar for bar, summ in barcode_dict.items() if summ == max_value]
            for bc in max_barcodes:
                rec = text_analyser.library_manager_tool.get_record_by_barcode(bc)
                cluster.set_confidence_value(max_value)
                cluster.add_best_record_match(rec)


def votation_system_2(all_clusters_2_texts, id_1, id_2):
    excel_file = EXCEL_FILE
    test = TextAnalysis(excel_file)

    list_of_total_barcodes = {}
    count = 0
    for cluster_id, cluster in all_clusters_2_texts.items():
        print("Elaborating cluster " + str(count) + "/" + str(len(all_clusters_2_texts) - 1))
        count += 1
        barcode_dict = {}
        for word in cluster:
            records, min_distance = test.get_closest_elements_in_range(word, id_1, id_2)
            each_value = len(word) - min_distance / len(word)
            for record in records:
                barcode = record[0][0]
                if barcode in barcode_dict:
                    barcode_dict[barcode] += each_value
                else:
                    barcode_dict[barcode] = each_value

        if len(barcode_dict.keys()) != 0:
            max_value = max(barcode_dict.values())
            max_barcodes = [bar for bar, summ in barcode_dict.items() if summ == max_value]
            tmp_list = []
            for bc in max_barcodes:
                # append the barcode to the final list with his confidence value
                tmp_list.append([bc, max_value])
            list_of_total_barcodes[cluster_id] = tmp_list
    return list_of_total_barcodes


