# This file modifies the text to remove all
# irrelevant features such as whitespace, punctuation, etc.

import os
import string
import re


def cleanUp():
    docs_path = './data/Docs_txt'
    for filename in os.listdir(docs_path):
        file = open(docs_path+'/'+filename, 'r+')
        text = file.read()
        file.truncate(0)
        text = ''.join(e for e in text if e.isalnum())
        text = text.lower()
        file.write(text)
        file.close()


cleanUp()
