# This file modifies the text to remove all
# irrelevant features such as whitespace, punctuation, etc.

import os
import string
import re


def cleanUp(docs_path):
    for filename in os.listdir(docs_path):
        file = open(docs_path+'/'+filename, 'r+')
        text = file.read()
        file.truncate(0)
        text = ''.join(e for e in text if e.isalnum())
        text = text.lower()
        text = text.strip('\x00')
        text = text.replace('\x00', '')
        if len(text) > 0:
            file.write(text)
            file.close()
        else:
            os.remove(str(docs_path+filename))


cleanUp('./data/Docs_txt/')
cleanUp('./data/Templates_txt/')
