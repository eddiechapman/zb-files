from PyPDF2 import PdfFileMerger
import os

# Set directory# Set di
os.chdir('C:\\Users\\chapman4\\Desktop')


def list_filenames():
# Get Filenames. Assumes cover pdfs name ends with '-cover'. Assumes there is a body for every cover.
    filenames = [name.split("_")[0] for name in os.listdir(".") if name.endswith(".pdf")]
    return filenames


def pdf_merge(filename):
    merger = PdfFileMerger()

    pdf_cover = open(filename + '_cover.pdf', 'rb')
    merger.append(pdf_cover)

    pdf_body = open(filename + '_body.pdf', 'rb')
    merger.append(pdf_body)

    outfile = open(filename + '-transcript.pdf', 'wb')
    merger.write(outfile)

    pdf_cover.close()
    pdf_body.close()
    outfile.close()


def main():
    for filename in list_filenames():
        try:
            pdf_merge(filename)
        except FileNotFoundError:
            print('File Not Found: ' + filename)


main()
