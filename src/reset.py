import os

mydir = './data/'
for file in os.listdir(mydir):
    if file != mydir+'Docs' and file != mydir+'Templates':
        os.remove(mydir+file)
