To run the code:

1. Clone the repo
2. Add a folder called data: digitalfingerprint/data
3. Under data have another folder called 'Docs', which contains all your data
4. From the directory (path: ./digitalfingerprint), run "python(3) src/setup.py". This should set up different folders under digitalfingerprint/data/ called Docs_txt, Read and Unreadable. Docs_txt contains all the text extracted from the Docs folder. Read contains all the folders that were successfully read and Unreadable contains the document types that couldn't be read. This is to help analyze what kinds of data is being read and not being read.
5. After that we can run "python(3) src/cleanup.py". This removes all irrelevant features from the text files. Takes away all whitespaces, punctuations and everything that isn't alphanumeric.
