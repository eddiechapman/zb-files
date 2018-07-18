import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from chardet.universaldetector import UniversalDetector

os.chdir('C:\\Users\\chapman4\\Desktop')

def list_filenames():
    filenames = [name.split(".")[0] for name in os.listdir(".") if name.endswith(".txt")]
    return filenames


def determine_encoding(filename):
    detector = UniversalDetector()
    with open(filename + '.txt', 'rb') as infile:
        detector.reset()
        for line in infile:
            detector.feed(line)
            if detector.done:   # detection process ends automatically when confidence is high enough
                break
        detector.close()
        return detector.result


def create_pdf(filename, detector_result):
    with open(filename + '.txt', 'r', encoding = detector_result['encoding']) as infile:
        doc = SimpleDocTemplate(filename + '_body.pdf', pagesize=letter, rightMargin=80, leftMargin=80,\
                                topMargin=60, bottomMargin=60)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Paragraph', fontName='Helvetica', fontSize=12,  leading=18))
        styles.add(ParagraphStyle(name='Bold', fontName='Helvetica-Bold', fontSize=12))

        content = []

        for line in infile:
            if '##content##' in line:
                for line in infile:
                    if not line.isspace():
                        clean_line = line.strip()
                        if '##' in line:
                            tag_line = clean_line.replace('##', '')
                            uni_tag_line = tag_line.encode('utf-8')
                            content.append(Paragraph(uni_tag_line, styles["Bold"]))
                            content.append(Spacer(1, 12))
                        else:
                            uni_line = clean_line.encode('utf-8')
                            content.append(Paragraph(uni_line, styles["Paragraph"]))
                            content.append(Spacer(1, 12))
        doc.build(content)


def main():
    for filename in list_filenames():
        detector_result = determine_encoding(filename)
        create_pdf(filename, detector_result)


main()
