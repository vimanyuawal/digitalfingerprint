# This converts all files of type pdf and docx to .txt files so we
# can use them for further analysis. This file needs to be run just
# once for set up.

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

headers = {
    'X-Tika-PDFextractInlineImages': 'true',
    "X-Tika-OCRLanguage": "eng+nor"
}


def createFolders():
    newpath = r'./data/Docs_txt'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        print('Docs_txt folder created...')
    else:
        print('The Docs_txt folder already exists.')

    newpath = r'./data/Read'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        print('Read folder created...')
    else:
        print('The Read folder already exists.')

    newpath = r'./data/Unreadable'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        print('Unreadable folder created...')
    else:
        print('The Unreadable folder already exists.')


def readFilesToText():
    print('Accessing files from data/Docs...')
    directory = './data/Docs'
    read_path = './data/Read'
    unread_path = './data/Unreadable'
    save_path = './data/Docs_txt'
    counter = 0
    unableToConvert = []
    countpdf = 1
    filenums = len(os.listdir(directory))

    for file in os.listdir(directory):
        if(file not in os.listdir(read_path)):
            if('.pdf' in file):
                countpdf += 1
            print('Converting file ' + str(counter) + '/'
                  + str(filenums) + '...')
            data = parser.from_file(directory+'/'+file)
            text = data['content']
            if text != None:
                textFile = open(('./data/Docs_txt/'+str(counter)+'.txt'), 'w')
                textFile.write(text)
                textFile.close()
                # moving to read folder
                shutil.copyfile(directory+'/'+file, read_path+'/'+file)
                print('Added file.')

                counter += 1
            else:
                print('Moving ' + file + " to unreadable.")

                # this means that the data is a scanned image pdf so we can convert
                #  into an image and use OCR to extract text
                print('Apache Tika returned None for file: ' + str(file))
                # moving to unread folder
                shutil.copyfile(directory+'/'+file, unread_path+'/'+file)
                unableToConvert.append(file)
    print('\n\n The total number of PDFs were: ', countpdf)
    if(len(unableToConvert) == 0):
        print('All files converted to .txt')
        return

    print(str(len(unableToConvert)) +
          ' files were not converted to text. These files are: ' + str(unableToConvert))

    print('Converting the files to JPEG and then trying OCR...')

    for file in os.listdir(unread_path):
        if '.pdf' in file:
            print('Picking up file: ' + str(file))
            pdf_path = unread_path+'/'+file
            try:
                pages = convert_from_path(pdf_path)
                page_counter = 1
                for page in pages:
                    filename = unread_path+'/'+file + \
                        "_page"+str(page_counter)+'.jpg'
                    page.save(filename, 'JPEG')
                    page_counter += 1
                totalpages = page_counter-1
                txtfile = save_path+'/'+str(counter)+'.txt'
                print('Save file to '+str(txtfile))
                textFile = open(txtfile, 'a')

                for i in range(1, totalpages):
                    filename = unread_path+'/'+file+"_page"+str(i)+'.jpg'
                    text = str(
                        ((pytesseract.image_to_string(Image.open(filename)))))
                    textFile.write(text)
                textFile.close()
                # moving to read folder
                shutil.move(unread_path+'/'+file, read_path+'/'+file)
                print('Saved.')
                counter += 1
            except(ValueError, PDFPageCountError):
                print('The pdf ' + file + ' could not be read')

    filelist = [f for f in os.listdir(unread_path) if f.endswith(".jpg")]
    for f in filelist:
        os.remove(unread_path+'/'+f)


createFolders()
readFilesToText()
