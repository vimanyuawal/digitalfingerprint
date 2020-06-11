# This file modifies the text to remove all
# irrelevant features such as whitespace, punctuation, etc.

import os
import string
import re


def cleanUp(text):

    text = ''.join(e for e in text if e.isalnum())
    text = text.lower()
    text = text.strip('\x00')
    text = text.replace('\x00', '')
    return text
