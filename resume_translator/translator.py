import PyPDF2
import re
import tika
import fitz
from deep_translator import GoogleTranslator
from deep_translator.exceptions import NotValidPayload


def translate_hebrew_to_english(text: str)-> [str]:

    translator = GoogleTranslator(source='hebrew', target='english')

    return translator.translate(text)


def extract_text_from_pymupdf(pdf_file: str) -> [str]:

    fname = pdf_file
    doc = fitz.open(fname)  # open document
    ret=""
    for page in doc:  # iterate the document pages
        text = make_text(page.get_text("words")) # get plain text (is in UTF-8)
        ret+= text
    return ret


def make_text(words):
    """Return textstring output of get_text("words").
    Word items are sorted for reading sequence right to left,
    top to bottom.
    """
    line_dict = {}  # key: vertical coordinate, value: list of words
    words.sort(key=lambda w: w[0], reverse=True)  # sort by horizontal coordinate from right to left
    for w in words:  # fill the line dictionary
        y1 = round(w[1], 2)  # bottom of a word: don't be too picky!
        word = w[4]  # the text of the word
        line = line_dict.get(y1, [])  # read current line content
        line.append(word)  # append new word
        line_dict[y1] = line  # write back to dict
    lines = list(line_dict.items())
    lines.sort()  # sort vertically
    return "\n".join([" ".join(line[1]) for line in lines])



def notFlip(string):
    pattern = re.compile(r'[\u0590-\u05FF]{2,}')
    return bool(pattern.search(string))


def flipTextWhereNeeded(extracted_text):
    textArr = extracted_text.split("\n")

    for i in range(len(textArr)):
        # textArr[i] = textArr[i][::-1]
        wordArr = textArr[i].split()
        for j in range(len(wordArr)):
            if notFlip(wordArr[j]):
                wordArr[j] = wordArr[j][::-1]
        textArr[i] = " ".join(wordArr)

    return textArr

def main():

    FILENAME = 'cv.pdf'

    extracted_text = extract_text_from_pymupdf(FILENAME)

    textArr = flipTextWhereNeeded(extracted_text)

    for word in textArr:
        # split_message = re.split(r'\s+|[,;?!.-]\s*', text.lower())
        try:
            print(translate_hebrew_to_english(word))
        except NotValidPayload:
            print(word)


if __name__ == '__main__':
    main()