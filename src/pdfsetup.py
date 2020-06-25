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
import random

headers = {
    'X-Tika-PDFextractInlineImages': 'true',
    "X-Tika-OCRLanguage": "eng+nor"
}

path = './data/Docs_txt/'


# def makeFolder():
#     os.mkdir(path)


def readData():
    data = parser.from_file(
        './data/Templates/f1099msc.pdf')
    text = data['content']
    if text != None:
        return text
    else:
        return ''


def createSamples(text, n=1):
    for i in range(0, n):
        file = open(path+'sample'+str(i)+'.txt', 'w+')
        amt = random.randint(1, 5000)
        text = text.replace('$', '$'+str(amt))
        text = cleanUp(text)
        file.write(text)


# makeFolder()
text = readData()
createSamples(text, n=5)
