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
from cleanup import cleanUp

headers = {
    'X-Tika-PDFextractInlineImages': 'true',
    "X-Tika-OCRLanguage": "eng+nor"
}


def classifyFilesByText(file, text, reciprocalfolder, nonmutualndafolder, unclassified, r, m, n):

    if 'reciprocal' in text:
        type = open(reciprocalfolder +
                    file.partition('.')[0]+'.txt', 'w')
        type.write(text)
        type.close()
        r += 1

    elif 'nonmutual' in text:
        type = open(nonmutualndafolder +
                    file.partition('.')[0]+'.txt', 'w')
        type.write(text)
        type.close()
        m += 1

    else:
        type = open(unclassified+file.partition('.')
                    [0]+'.txt', 'w')
        type.write(text)
        type.close()
        n += 1


def classifyFilesByHeadingAndText(file, text, reciprocalfolder, nonmutualndafolder, unclassified, r, m, n):

    if ('nonmutual' in file.lower()) or ('non-mutual' in file.lower()):
        type = open(nonmutualndafolder +
                    file.partition('.')[0]+'.txt', 'w')
        type.write(text)
        type.close()
        m += 1

    elif ('reciprocal' in file.lower()) or ('mnda' in file.lower()) or ('reciprocal' in text.lower()) or ('mutual nda' in file.lower()) or ('mutualnda' in text.lower()) or ('mutualconf' in text.lower()) or ('mutualnon' in text.lower()):
        type = open(reciprocalfolder +
                    file.partition('.')[0]+'.txt', 'w')
        type.write(text)
        type.close()
        r += 1

    else:
        type = open(unclassified+file.partition('.')
                    [0]+'.txt', 'w')
        type.write(text)
        type.close()
        n += 1


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

    newpath = r'./data/Templates_txt'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        print('Templates_txt folder created...')
    else:
        print('The Templates_txt folder already exists.')

    newpath = r'./data/Reciprocal'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        print('Reciprocal folder created...')
    else:
        print('The Reciprocal folder already exists.')

    newpath = r'./data/NonMutual'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        print('NonMutual folder created...')
    else:
        print('The NonMutual folder already exists.')

    newpath = r'./data/Unclassified'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        print('Unclassified folder created...')
    else:
        print('The Unclassified folder already exists.')


def readFilesToText():
    print('Accessing files from data/Docs...')
    directory = './data/Docs'
    read_path = './data/Read'
    unread_path = './data/Unreadable'
    save_path = './data/Docs_txt'
    unclassified = './data/Unclassified/'
    m = 0
    reciprocalfolder = './data/Reciprocal/'
    r = 0
    nonmutualndafolder = './data/NonMutual/'
    n = 0
    unableToConvert = []
    countpdf = 1
    filenums = len(os.listdir(directory))

    for file in os.listdir(directory):
        if(file not in os.listdir(read_path)):
            if('.pdf' in file):
                countpdf += 1

            data = parser.from_file(directory+'/'+file)
            text = data['content']
            if text != None:
                text = cleanUp(text)
                if len(text) > 0:
                    classifyFilesByText(file, text, reciprocalfolder,
                                        nonmutualndafolder, unclassified, r, m, n)

                    textFile = open(
                        ('./data/Docs_txt/'+file.partition('.')[0]+'.txt'), 'w')
                    textFile.write(text)
                else:
                    textFile.close()
                    continue
                textFile.close()
                # moving to read folder
                shutil.copyfile(directory+'/'+file, read_path+'/'+file)
            else:
                # print('Moving ' + file + " to unreadable.")

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
            pdf_path = unread_path+'/'+file
            try:
                pages = convert_from_path(pdf_path)
                page_counter = 1
                for page in pages:
                    filename = unread_path+'/'+file.partition('.')[0] + \
                        "_page"+str(page_counter)+'.jpg'
                    page.save(filename, 'JPEG')
                    page_counter += 1
                totalpages = page_counter-1
                txtfile = save_path+'/'+file.partition('.')[0]+'.txt'
                textFile = open(txtfile, 'a')

                for i in range(1, totalpages):
                    filename = unread_path+'/' + \
                        file.partition('.')[0]+"_page"+str(i)+'.jpg'
                    text = str(
                        ((pytesseract.image_to_string(Image.open(filename)))))
                    text = cleanUp(text)
                    if len(text) > 0:
                        classifyFilesByText(file, text, reciprocalfolder,
                                            nonmutualndafolder, unclassified, r, m, n)
                        textFile.write(text)
                    else:
                        textFile.close()
                        continue
                textFile.close()
                # moving to read folder
                shutil.move(unread_path+'/'+file, read_path+'/'+file)
            except(ValueError, PDFPageCountError):
                print('The pdf ' + file + ' could not be read')

    filelist = [f for f in os.listdir(unread_path) if f.endswith(".jpg")]
    for f in filelist:
        os.remove(unread_path+'/'+f)

    template_path = './data/Templates/'
    save_path = './data/Templates_txt/'
    for file in os.listdir(template_path):
        data = parser.from_file(template_path+file)
        text = data['content']
        if text != None:
            if len(text) > 0:
                text = cleanUp(text)
                classifyFilesByText(file, text, reciprocalfolder,
                                    nonmutualndafolder, unclassified, r, m, n)

                textFile = open((save_path+file.partition('.')[0]+'.txt'), 'w')
                textFile.write(text)
                # moving to read folder
                shutil.copyfile(template_path+file, read_path+'/'+file)


createFolders()
readFilesToText()
