import pandas as pd
import numpy as np
from my_code.text_filtering import remove_banish_character, banished_characters_for_cell_management

barcode_column_name = 'Barcode'
title_column_name = 'title'
collocation_column_name = 'Collocazione'


class LibraryManagerTool:

    # constructor
    def __init__(self, xlsx):
        self.df = pd.read_excel(xlsx)
        self.rows = self.df.shape[0]
        self.columns = self.df.shape[1]
        data = []
        for id in range(self.rows):
            record = self.df.loc[id]
            data_rec = []
            for i in range(self.columns):
                cell = record[i]
                if isinstance(cell, float):
                    cell = ''
                if i != 0:
                    cell = remove_banish_character(cell, banished_characters_for_cell_management)
                data_rec.append(cell.split())
            data.append(data_rec)
        self.data = np.array([np.array(xi, dtype=object) for xi in data], dtype=object)

    def get_column_name(self):
        return list(self.df.columns)

    def get_number_records(self):
        return self.rows

    def get_numbers_columns(self):
        return self.columns

    def get_record(self, record_number):
        if 0 <= record_number <= self.rows:
            return self.data[record_number]
        else:
            return None

    def get_record_by_barcode(self, barcode):
        result = None
        for rec in self.data:
            bar = rec[0][0]
            if bar == barcode:
                result = rec
                break
        return result.tolist()

    def get_number_by_barcode(self, barcode):
        result = None
        for num, rec in enumerate(self.data):
            bar = rec[0][0]
            if bar == barcode:
                result = num
                break
        return result





