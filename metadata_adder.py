import csv
import os
from chardet.universaldetector import UniversalDetector


# Set directory to the inside of folder full of text files that need editing
os.chdir('C:\\Users\\chapman4\\Desktop')


def create_metadata():
    metadata = []
    with open('zuck-metadata.csv', encoding="UTF-8") as csvfile:
        fieldnames = ['record_id', 'participants', 'record_type', 'record_format',\
                      'date', 'source', 'title', 'url', 'description']
        reader = csv.DictReader(csvfile, fieldnames)
        for row in reader:
            record = {}
            for name in fieldnames:
                record[name] = row[name]
            metadata.append(record)
        return metadata


# Creating list of filenames in folder specified when setting directory above
def list_filenames():
    filenames = [name.split(".")[0] for name in os.listdir(".") if name.endswith(".txt")]
    return filenames


def detect_encoding(filename):
    # Detector object for encoding detection
    detector = UniversalDetector()

    # Determining encoding information, adding as a key-value pair to record's metadata dict entry
    with open(filename + '.txt', 'rb') as infile:
        detector.reset()
        for line in infile:
            detector.feed(line)
            if detector.done:   # detection process ends automatically when confidence is high enough
                break
        detector.close()
        return detector.result['encoding']


def grab_text(filename, encoding):
    with open(filename + '.txt', 'r+', encoding = encoding) as infile:
        text = infile.read()
        return text


def write_metadata(filename, row, text):
    with open(filename + '.txt', 'w', encoding = "utf8") as outfile:
        # All this mess could probably be simplified with str.format()
        outfile.write('##title##\n\n')
        outfile.write(row['title'] + '\n\n')
        outfile.write('##date##\n\n')
        outfile.write(row['date'] + '\n\n')
        outfile.write('##id##\n\n')
        outfile.write(row['record_id'] + '\n\n')
        outfile.write('##description##\n\n')
        outfile.write(row['description'] + '\n\n')
        outfile.write('##source##\n\n')
        outfile.write(row['source'] + '\n\n')
        outfile.write('##type##\n\n')
        outfile.write(row['record_type'] + '\n\n')
        outfile.write('##participants##\n\n')
        outfile.write(row['participants'] + '\n\n')
        outfile.write('##format##\n\n')
        outfile.write(row['record_format'] + '\n\n')
        outfile.write('##url##\n\n')
        outfile.write(row['url'] + '\n\n\n')
        outfile.write('##content##\n\n')
        outfile.write(text)
        outfile.close()


def main():
    filenames = list_filenames()

    for row in create_metadata():
        if row['record_id'] in filenames:
            encoding = detect_encoding(row['record_id'])
            text = grab_text(row['record_id'], encoding)
            write_metadata(row['record_id'], row, text)


main()
