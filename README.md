Developer: Vimanyu Awal
email: vimanyu.awal@gmail.com

You can contact me about any problems in the code or any segments you don't understand!

# Digital Fingerprinting:

## Purpose: This project seeks to match input documents with a certain type of template that they belong to or are very similar to, using digital fingerprinting.

Document fingerprints are created with the method of 'winnowing', which is detailed in a paper cited under Sources.

We seek to do this without using Computer Vision as this is a more efficient method that doesn't require training data.

e.g. A tax form can be classified into an appropriate category

## To run the code:

1. Clone the repo
2. Add a folder called data: digitalfingerprint/data
3. Under data have another folder called 'Docs', which contains all your data
4. From the directory (path: ./digitalfingerprint), run "python(3) src/setup.py". This should set up different folders under digitalfingerprint/data/ called Docs_txt, Read and Unreadable. Docs_txt contains all the text extracted from the Docs folder. Read contains all the folders that were successfully read and Unreadable contains the document types that couldn't be read. This is to help analyze what kinds of data is being read and not being read. The .txt files are also cleaned. We remove the irrelevant features such as whitespaces, punctuations and everything that isn't alphanumeric.
5. Then you can run python src/winnowing.py or src/winnowingWithoutPosition.py - the only difference being, winnowing cares about the position of the words and without position doesn't.

## Structure:

The way this code is structured is that you initially add your templates that you want your documents classified into. Those templates are added to the Templates_txt folder when setup is run. When winnowing is run these templates are added to a temporary database created in database.py that maps the fingerprints of a file to the file name. The documents to be classified are then taken one-by-one and for each we compare their fingerprints to the templates and using sets we can find if there is an overlap of fingerprints using a Jaccard score. If the Jaccard Score is above a certain threshold we can classify a document being similar to the template.

## Sources:

1. [The research paper](https://urldefense.com/v3/__https://theory.stanford.edu/*aiken/publications/papers/sigmod03.pdf__;fg!!LIr3w8kk_Xxm!_zxYMGxBG3V77fgt2xvumOwz-ytl_ZZKWaJr3-Thliwj32myivbA2DoMlIS7$)

2. [The implementation for winnowing](https://urldefense.com/v3/__https://github.com/kailashbuki/fingerprint/blob/master/fingerprint/fingerprint.py__;!!LIr3w8kk_Xxm!_zxYMGxBG3V77fgt2xvumOwz-ytl_ZZKWaJr3-Thliwj32myivbA2HDCXtVz$)
