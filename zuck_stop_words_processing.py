"""
Zuckerberg Files Stop Words Processing
Eddie Chapman
2018

Drops common words and punctuation from Zuckerberg transcripts for use as a full text index on
the Zuckerberg Files WordPress.

This program reads a folder of Zuckerberg Files transcripts in .txt format. It attempts to open
them using the correct character encoding. Text content is split into individual words.
Punctuation is removed. Words in the desiganated stop list (common words) are removed.
The remaining words are merged into a single paragraph. A CSV file is created with a row for each
file. One column lists the filename. One column contains the file's processed text.
"""

import csv
import os
import re
from chardet.universaldetector import UniversalDetector
import codecs


os.chdir('C:\\Users\\chapman4\\Downloads\\zuck-text-ready-test\\text\\text-new')


def list_filenames():
    """
    Open the working directory. Store the names of all text files in a list. Do not store '.txt'.
    """
    filenames = [name.split(".")[0] for name in os.listdir(".") if name.endswith(".txt")]
    return filenames


def list_stopwords():
    """
    Open a text file called 'stopwords.txt'. Store each line as an entry in a list. Remove any
    whitespace that is left on the end of a line.
    """
    with open('stopwords.txt', 'r') as infile:
        stopwords = [line.strip() for line in infile]
        return stopwords


def detect_encoding(filename):
    """
    Determine the character encoding of each text file.

    Create a detector object from the chardet library. Use the filename list to open all text files
    in the working directory. For each file, have the detector object inspect each line until it is
    confident of the encoding. When it is confident, return the encoding results and close the file.
    """
    detector = UniversalDetector()
    with open(filename + '.txt', 'rb') as infile:
        for line in infile:
            detector.feed(line)
            if detector.done:   # detection process ends automatically when confidence is high enough
                break
        detector.close()
        return detector.result['encoding']


def grab_text(filenames, stopwords):
    """
    For each text file, remove stop words and puntuation from contents and store them in a dictionary
    along with the filename. Dictionaries are stored in a list.

    Rows is a list of dictionaries. Loop through each text file as specified in the filenames list.
    Call the detect_encoding function to determine the character encoding. Use the results to properly
    open the file.

    For each file, create an empty dictionary. Create a 'text' object containing the contents of the
    file. Use a regular expression to split the text content into individual words. Punctuation is
    dropped unless it is inside the word (such as conjunctions). Change each word to lowercase. Remove
    words that found in the stopwords list. Put the remaining words back together, seperated by spaces.
    Store the processed text content in the file's dictionary under 'full_text' and store the filename
    under 'record_id'. The resulting dictionary is added to the 'rows' list. This continues until all
    text files in 'filenames' have been processed.
    """
    rows = []
    for filename in filenames:
        encoding = detect_encoding(filename)
        with codecs.open(filename + '.txt', 'r', encoding) as infile:
            row = {}
            text = infile.read()
            tokens_nonnormal = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", text)
            tokens_normal = [t.lower() for t in tokens_nonnormal]
            tokens_minus_stop = [t for t in tokens_normal if t not in stopwords]
            tokens = ' '.join(tokens_minus_stop)
            row['record_id'] = filename
            row['full_text'] = tokens
            rows.append(row)
    return rows


def write_csv(rows):
    """
    Export the processed text content and filenames in a CSV file.

    Open a new CSV file called 'zuck_full_text.csv'. Refer to it internally as 'csv_file'.
    For the names of the CSV column names, look at the first dictionary stored in the 'rows' list
    and use the key-names as column names. Create a writer object using the CSV library. Use the
    writer object to write the header. Use the writer object and the 'rows' list to fill in the
    rest of the values.
    """
    with open(zuck_full_text.csv, 'w', encoding='utf-8') as csv_file:
        col_names = rows[0].keys()
        writer = csv.DictWriter(csv_file, col_names)
        writer.writeheader()
        writer.writerows(rows)


def main():
    filenames = list_filenames()
    stopwords = list_stopwords()
    rows = grab_text(filenames, stopwords)
    write_csv(rows)
