from tika import parser
import shutil
import os
import subprocess
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from cleanup import cleanUp

headers = {
    'X-Tika-PDFextractInlineImages': 'true',
    "X-Tika-OCRLanguage": "eng+nor"
}

data = parser.from_file(
    '/Users/vimanyuawal/Desktop/digitalfingerprint/data/Templates/f1099msc.pdf')
text = data['content']
if text != None:
    # text = cleanUp(text)
    print(text)
    myarray = text.split("$")
    for line in myarray:
        print(line)
        print("#####  fill number here")

    # from PyPDF2 import PdfFileReader
    # def get_info(path):
    #     with open(path, 'rb') as f:
    #         pdf = PdfFileReader(f)
    #         info = pdf.getDocumentInfo()
    #         number_of_pages = pdf.getNumPages()

    #     print(info)
    #     author = info.author
    #     creator = info.creator
    #     producer = info.producer
    #     subject = info.subject
    #     title = info.title
else:
    print('text was none')
