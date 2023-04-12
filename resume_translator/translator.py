import textwrap
import xml.etree.ElementTree as ET
from xhtml2pdf import pisa
import PyPDF2
import re
import tika
import fitz
import os, openai
from deep_translator import GoogleTranslator
from deep_translator.exceptions import NotValidPayload
from reportlab.pdfgen import canvas
import numpy as np
from resume_translator.ResumeLine import ResumeLine
from fpdf import FPDF
from reportlab.lib.pagesizes import letter

from resume_translator.resume import resume


def translate_hebrew_to_english(text: str)-> [str]:

    translator = GoogleTranslator(source='hebrew', target='english')

    retString = translator.translate(text)

    if(retString is None):
        return text
    else:
        return retString


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
    lines_unique_dict = {}
    words.sort(key=lambda w: w[0], reverse=True)  # sort by horizontal coordinate from right to left
    for w in words:
        x0 = round(w[0],2)
        x1 = round(w[2])
        y0 = round(w[1], 2)
        y1 = round(w[3], 2)
        word = w[4]  # the text of the word
        line = line_dict.get(y1, line_dict.get(y0,ResumeLine()))
        if(line.isEmpty()):
            lines_unique_dict[y1]=line
        line.addData(word,x0,x1,y0,y1)  # append new word
        line_dict[y1] = line
        line_dict[y0] = line
    lines = list(lines_unique_dict.items())
    lines.sort()  # sort vertically
    return "\n".join(["".join(line[1].getText()) for line in lines])



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

def makePDF(text):
    c = canvas.Canvas("output.pdf")

    # Split the text into lines
    lines = text.split('\n')

    # Set the starting y-coordinate for the first line
    y = 780

    # Set the maximum width of a line in the PDF
    max_width = 90

    # Loop through each line and add it to the PDF
    for line in lines:
        # Split long lines into multiple shorter lines
        wrapped_lines = textwrap.wrap(line, width=max_width)

        # Loop through each wrapped line and add it to the PDF
        for wrapped_line in wrapped_lines:
            c.drawString(70, y, wrapped_line)
            y -= 15  # Move to the next line

    # Save the PDF
    c.save()
    print("PDF file created!")


def xml_to_pdf(xml_string, output_filename):
    # parse the XML string into an ElementTree object
        # Parse the XML string into an ElementTree object
        text = "<?xml"+ xml_string.split("<?xml")[1]
        root = ET.fromstring(text)

        # Create a canvas to draw the PDF on
        c = canvas.Canvas(output_filename, pagesize=letter)

        # Set the font size and leading for the text
        font_size = 12
        leading = 14

        # Write the header information
        name = root.find('header/name').text
        email = root.find('header/email').text
        phone = root.find('header/phone').text
        id = root.find('header/id').text
        c.setFont("Helvetica-Bold", font_size)
        c.drawString(100, 750, name)
        c.setFont("Helvetica", font_size)
        c.drawString(100, 730, f'Email: {email}')
        c.drawString(100, 710, f'Phone: {phone}')
        c.drawString(100, 690, f'ID: {id}')

        # Write the summary
        summary = root.find('summary').text
        c.setFont("Helvetica", font_size)
        c.drawString(100, 650, "Summary")
        c.drawString(100, 630, summary)

        # Write the work experience
        c.setFont("Helvetica-Bold", font_size)
        c.drawString(100, 590, "Work Experience")
        y = 570
        for job in root.findall('work-experience/job'):
            title = job.find('title').text
            company = job.find('company').text
            location = job.find('location').text
            startdate = job.find('startdate').text
            enddate = job.find('enddate').text
            description = job.find('description').text
            c.setFont("Helvetica", font_size)
            c.drawString(100, y, title)
            c.drawString(300, y, f'{startdate} - {enddate}')
            c.drawString(100, y - 20, company)
            c.drawString(300, y - 20, location)
            y -= 40
            c.setFont("Helvetica-Oblique", font_size)
            c.drawString(100, y, description)
            y -= leading

        # Write the education
        c.setFont("Helvetica-Bold", font_size)
        c.drawString(100, y, "Education")
        y -= 20
        for degree in root.findall('education/degree'):
            name = degree.find('name').text
            institution = degree.find('institution').text
            location = degree.find('location').text
            startdate = degree.find('startdate').text
            enddate = degree.find('enddate').text
            description = degree.find('description').text
            c.setFont("Helvetica", font_size)
            c.drawString(100, y, name)
            c.drawString(300, y, f'{startdate} - {enddate}')
            c.drawString(100, y - 20, institution)
            c.drawString(300, y - 20, location)
            y -= 40
            c.setFont("Helvetica-Oblique", font_size)
            c.drawString(100, y, description)
            y -= leading

        # Write the military service


        military = root.find('military-service').text
        c.setFont("Helvetica-Bold", font_size)
        c.drawString(100, y, "Military Service")
        c.drawString(100, 630, military)

        c.save()
        print("MADE IT!")
def main():
    FILENAME = 'cv.pdf'

    extracted_text = extract_text_from_pymupdf(FILENAME)

    textArr = flipTextWhereNeeded(extracted_text)

    englishText = ""
    for line in textArr:
        # split_message = re.split(r'\s+|[,;?!.-]\s*', text.lower())
        try:
            englishText+= translate_hebrew_to_english(line)+'\n'
        except (NotValidPayload, AttributeError):
            englishText+= line+'\n'

    openai.api_key = ""  #FILL IN!!!

    xml_template = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <resume>
      <header>
        <name></name>
        <email></email>
        <phone></phone>
        <id></id>	
      </header>
      <summary></summary>
      <work-experience>
        <job>
          <title></title>
          <company></company>
          <location></location>
          <startdate></startdate>
          <enddate></enddate>
          <description></description>
        </job>
      </work-experience>
      <education>
        <degree>
          <name></name>
          <institution></institution>
          <location></location>
          <startdate></startdate>
          <enddate></enddate>
          <description></description>
        </degree>
      </education>
    	<military-service>
        <branch></branch>
        <rank></rank>
        <startdate></startdate>
        <enddate></enddate>
        <description></description>
      	</military-service>
      <skills>
        <skill></skill>
      </skills>
    </resume> '''

    gpt_prompt = xml_template+". \n Use this format to complete a resume with the following information:: " + englishText;




    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=gpt_prompt,
        max_tokens=1000,
    )

    # makePDF(response.choices[0].text)
    xml_to_pdf(response.choices[0].text, "xmloutput.pdf")


if __name__ == '__main__':
    main()