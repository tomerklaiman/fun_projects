import PyPDF2
import pdfminer.high_level as pdfminer
import re
import tika
import fitz
from tika import parser
tika.initVM()

def extract_text_from_pdf_pypdf(pdf_file: str) -> [str]:
    # Open the PDF file of your choice
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        # no_pages = len(reader.pages)

        for page in reader.pages:
            return(page.extract_text())
    return "hi"

def extract_text_from_pymupdf(pdf_file: str) -> [str]:
    import sys, fitz
    fname = sys.argv[1]  # get document filename
    doc = fitz.open(fname)  # open document
    out = open(fname + ".txt", "wb")  # open text output
    for page in doc:  # iterate the document pages
        text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
        out.write(text)  # write text of page
        out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
    out.close()


def extract_text_from_pdf_pdfminer(pdf_file: str) -> [str]:
    # Open the PDF file of your choice
    text = pdfminer.extract_text(pdf_file)

    return text

def notFlip(string):
    pattern = re.compile(r'[0-9a-zA-Z@]')
    return bool(pattern.search(string))

def extract_text_from_tika(pdf_file:str) -> [str]:
    parsed_pdf = parser.from_file(pdf_file)
    data = parsed_pdf['content']

    return data

def main():
    FILENAME = 'example.pdf'

    #extracted_text = extract_text_from_pdf_pypdf(FILENAME)
    extracted_text = extract_text_from_pdf_pdfminer(FILENAME)
    # extracted_text = extract_text_from_tika(FILENAME)
    textArr = extracted_text.split("\n")

    for i in range(len(textArr)):
            textArr[i]= textArr[i][::-1]
            wordArr = textArr[i].split()
            for j in range(len(wordArr)):
                if notFlip(wordArr[j]):
                    wordArr[j]= wordArr[j][::-1]
            textArr[i]= " ".join(wordArr)


    for word in textArr:
        # split_message = re.split(r'\s+|[,;?!.-]\s*', text.lower())
        print(word)


if __name__ == '__main__':
    main()