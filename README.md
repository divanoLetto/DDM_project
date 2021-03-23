# Data and Document Mining Project

## Overview 

The goal of this project is to create a capable application to validate the correct arrangement of the books on the shelves of the library of the School of Engineering of the University of Florence.
The developed application, which takes in an image containing the spines of books arranged on a shelf, is structured in the following pipeline of work:
- The areas of the image where there is text are detected using the EAST text detection algorithm (https://github.com/argman/EAST).
- A clustering algorithm, DBSCAN, is applied to the identified areas. Each cluster represents a contiguous writing, ie the title and/or the author of a single volume.
- The Google Tesseract text recognition algorithm is applied to each cluster to extract the contained text.
- The texts obtained are used to determine in which section of the library the image was taken through a comparison with the database of the library. Finally, the system attempts to detect the possible presence of books placed incorrectly on the shelf.

#![Alt text](relative/path/to/img.jpg?raw=true "Title")

## How to run the code:

- download the EAST algorithm as described in: "https://github.com/argman/EAST"
- insert this files in the EAST directory
- insert the image you want to input in the images directory
- execute my_code.main.py 