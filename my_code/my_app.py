import os

import cv2

from database_manager.TextAnalysis import TextAnalysis
from my_code.Performance_results import plot_barcode_histrogramm, draw_assigmente_bfp_outcome, draw_word_in_cluster
from my_code.settings import INPUT_PATH, OUTPUT_PATH, EXCEL_FILE, NUM_BOOKS, REMOVE_CLUSTER_WITH_1_ELEMENT, \
    CLUSTERED_PATH
from my_code.utils import remove_tmp_files, fix_flags, is_image, get_collocation_from_barcode, append_id
from my_code.preprocessing_image import preprocess_image
import eval
from my_code.Text_recognition import text_recognition
from votation_system.collocation_2_color import collocation_2_color
from votation_system.votation import votation_system
import pandas as pd
from votation_system.BookFieldProposal import BookFieldProposal, match_clusters_kook_proposals


def my_main():
    # fix some flags needed for EAST
    fix_flags()
    # rotate image
    for image_name in os.listdir(INPUT_PATH):
        if is_image(image_name):
            preprocess_image(image_name)
    # EAST algorithm
    eval.main()
    # Output texts from EAST boxes
    for image_name in os.listdir(OUTPUT_PATH):
        if is_image(image_name):
            print("image name: " + str(image_name))
            print("Num book: ")
            num_book = int(input())

            # calcolo dei cluster e del testo in loro contenuto
            clusters = text_recognition(image_name)

            # filter cluster with less than one element
            if REMOVE_CLUSTER_WITH_1_ELEMENT:
                to_remove = []
                for clus in clusters:
                    if len(clus.texts) == 1:
                        to_remove.append(clus)
                for r in to_remove:
                    clusters.remove(r)

            # get exel file library database
            excel_file = EXCEL_FILE
            text_analyser = TextAnalysis(excel_file)
            # votation system
            votation_system(clusters, text_analyser)

            # unite all barcodes with their confidence value to decide what set of books are the most probable
            all_barcodes = {i[0]: 0 for i in text_analyser.library_manager_tool.data[:, 0]}
            for cluster in clusters:
                for barcode in cluster.get_best_barcodes_match():
                    all_barcodes[barcode] += cluster.get_confidence_value()

            print("image name: " + str(image_name))
            print("Num book: " + str(num_book))
            # plot the histogramm of all barcodes and their confidence value
            # plot_barcode_histrogramm(all_barcodes)

            # find the most probable start and end barcodes from the histrogramm
            dict_conversion = {}
            count = 0
            for i in all_barcodes.keys():
                dict_conversion[count] = i
                count += 1
            li = list(all_barcodes.values())
            slices = (li[x:x + num_book] for x in range(len(li) - num_book + 1))
            slices = [sum(x) for x in slices]
            mx = max(slices)
            index_of_largest = slices.index(mx)
            start_barcode = dict_conversion[index_of_largest]
            end_barcode = dict_conversion[index_of_largest+num_book-1]
            id_start = index_of_largest
            id_end = index_of_largest + num_book - 1
            print("Most probable start and end barcodes are: " + str(start_barcode) + " | " + str(end_barcode))

            # get all records between estimated start and end barcodes from the database library
            barcodes_in_shelf = []
            records_in_shelf = []
            for i in range(num_book):
                barcodes_in_shelf.append(dict_conversion[index_of_largest+i])
            df = pd.read_excel(EXCEL_FILE)
            for i in barcodes_in_shelf:
                records_in_shelf.append(text_analyser.library_manager_tool.get_record_by_barcode(i))

            # find the medium rappresentative color of the image
            medium_collocation = float(((df.loc[df['barcode'] == dict_conversion[index_of_largest+ int(num_book/2)]])["collocation"].values[0]).split()[0])
            color_code_shelf = collocation_2_color(medium_collocation)
            print("Most probable color is: " + color_code_shelf)

            # try to find book that are out of color bounds
            list_warnings_out_of_ids3 = []
            for clus in clusters:
                if len(clus.get_texts()) > 1:
                    in_range_sum = 0
                    for barcode in clus.get_best_barcodes_match():
                        num = text_analyser.library_manager_tool.get_number_by_barcode(barcode)
                        if id_start < num < id_end:
                            in_range_sum += clus.get_confidence_value()
                    if clus.get_confidence_value() > in_range_sum:
                        list_warnings_out_of_ids3.append(clus)
            # print("These book are probably out of color in the image:")
            # print(list_warnings_out_of_ids3)
            print("Numero di libri probabilmente fuori id : "+ str(len(list_warnings_out_of_ids3)))
            image = cv2.imread(CLUSTERED_PATH+image_name)
            image_name_out_of_ids = append_id(image_name, "out_id")
            cv2.imwrite(CLUSTERED_PATH + image_name_out_of_ids, image.copy())
            for clus in list_warnings_out_of_ids3:
                draw_word_in_cluster(image_name_out_of_ids, clus, "OUT_ID_", offset_x=-500, offset_y=0, color=(0, 0, 255))

            # try to find book that are out of start and end barcodes bounds
            list_warnings_out_of_color3 = []
            for clus in clusters:
                if len(clus.get_texts()) > 1:
                    in_range_sum = 0
                    for barcode in clus.get_best_barcodes_match():
                        collocation = get_collocation_from_barcode(df, barcode).number
                        if collocation_2_color(collocation) == color_code_shelf:
                            in_range_sum += clus.get_confidence_value()
                    if clus.get_confidence_value() > in_range_sum:
                        list_warnings_out_of_color3.append(clus)
            # print("These book are probably out of start/end barcodes bounds:")
            # print(list_warnings_out_of_color3)
            print("Numero di libri probabilmente fuori colore : "+ str(len(list_warnings_out_of_color3)))
            image = cv2.imread(CLUSTERED_PATH + image_name)
            image_name_out_of_col = append_id(image_name, "out_col")
            cv2.imwrite(CLUSTERED_PATH + image_name_out_of_col, image.copy())
            for clus in list_warnings_out_of_color3:
                draw_word_in_cluster(image_name_out_of_col, clus, "OUT_COL", offset_x=-500, offset_y=80, color=(0, 0, 255))

            # create a list of BookFieldProposal from the records in the bounds
            list_book_field_proposal2 = []
            # assign recursevely each BFP to his most probable cluster to have a 1 to 1 match
            for rec in records_in_shelf:
                barcode = rec[0][0]
                tmp_list = []
                for num_col, field in enumerate(rec):
                    if num_col == 1 or num_col == 2:
                        tmp_list += field
                book_field_proposal = BookFieldProposal(barcode, tmp_list)
                list_book_field_proposal2.append(book_field_proposal)
            for book_f in list_book_field_proposal2:
                match_clusters_kook_proposals(book_f, list_book_field_proposal2, clusters)

            draw_assigmente_bfp_outcome(list_book_field_proposal2, image_name, df, specify_name = "V2_" )

            # filter not assigned BFP
            restricted_list_book_field_proposal2 = []
            for i in range(0, len(list_book_field_proposal2)):
                bfp_title_and_author = list_book_field_proposal2[i]
                if bfp_title_and_author.get_cluster() is not None:
                    restricted_list_book_field_proposal2.append(bfp_title_and_author)

            #  find witch book are probably out of order in the image
            order_warning_ = []
            restricted_list_book_field_proposal2.sort(key=lambda x: x.get_cluster().calc_cluster_center()[1], reverse=True)
            # print(restricted_list_book_field_proposal2)
            for bfp_id in range(1, len(restricted_list_book_field_proposal2)-1):
                precedent = restricted_list_book_field_proposal2[bfp_id - 1]
                precedent_collocation = get_collocation_from_barcode(df, precedent.get_barcode())
                current = restricted_list_book_field_proposal2[bfp_id]
                current_collocation = get_collocation_from_barcode(df, current.get_barcode())
                next = restricted_list_book_field_proposal2[bfp_id + 1]
                next_collocation = get_collocation_from_barcode(df, next.get_barcode())
                if precedent_collocation <= current_collocation:
                    if current_collocation > next_collocation:
                        if precedent_collocation <= next_collocation:
                            order_warning_.append(current)
                        else:
                            order_warning_.append(next)
                else:
                    if precedent_collocation <= next_collocation:
                        order_warning_.append(current)
                    else:
                        order_warning_.append(precedent)
            order_warning_ = list(set(order_warning_))
            # print(order_warning_)
            print("Number of order error found: "+str(len(order_warning_)))
            image = cv2.imread(CLUSTERED_PATH + image_name)
            image_name_out_of_order = append_id(image_name, "out_order")
            cv2.imwrite(CLUSTERED_PATH + image_name_out_of_order, image.copy())
            for order_war_bfp in order_warning_:
                clus = order_war_bfp.get_cluster()
                draw_word_in_cluster(image_name_out_of_order, clus, "OUT_ORDER", offset_x=0, offset_y=100, color=(0, 165, 255))

            print("Finished")
    remove_tmp_files()


if __name__ == '__main__':
    my_main()
