import PyPDF2
import pdfminer.high_level as pdfminer
import re
import tika
import fitz
from tika import parser
tika.initVM()


def extract_text_from_pymupdf(pdf_file: str) -> [str]:

    fname = pdf_file
    doc = fitz.open(fname)  # open document
    ret=""
    for page in doc:  # iterate the document pages
        text = page.get_text(sort=True) # get plain text (is in UTF-8)
        ret+= text
    return ret




def notFlip(string):
    pattern = re.compile(r'[0-9a-zA-Z@]')
    return bool(pattern.search(string))


def main():
    FILENAME = 'example.pdf'

    extracted_text = extract_text_from_pymupdf(FILENAME)

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