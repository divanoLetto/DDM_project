import pandas as pd
""" Script to convert excel database to a standard form"""


barcode_column_name = 'Barcode'
title_column_name = 'title'
collocation_column_name = 'Collocazione'

column_names = ["barcode", "title", "authors", "collocation"]
new_bib = pd.DataFrame(columns = column_names)

xlsx = '/home/lorenzo/Scrivania/DDM/EAST-master/database_manager/new_biblioteca_02022021.xls'
bib = pd.read_excel(xlsx)

for ind in bib.index:
    barcode = bib[barcode_column_name][ind]
    title_authors = bib[title_column_name][ind]
    collocation = bib[collocation_column_name][ind]
    title_author_list = title_authors.split(" / ", 1)
    title = title_author_list[0]
    if len(title_author_list) > 1:
        authors = title_author_list[1]
    else:
        authors = ""
    column_names = ["barcode", "title", "authors", "collocation"]
    new_bib = new_bib.append({'barcode': barcode, 'title': title, 'authors': authors, 'collocation': collocation}, ignore_index=True)
new_bib.to_excel("new_biblioteca_02022021.xls")