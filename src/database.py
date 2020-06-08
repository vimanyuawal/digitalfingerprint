class Database:
    def __init__(self):
        self.fingerprintToDoc = {}

    def add(self, fingerprints, docpath):
        if fingerprints in self.fingerprintToDoc.keys():
            self.fingerprintToDoc[fingerprints].append(docpath)
        else:
            self.fingerprintToDoc[fingerprints] = [docpath]

    def getDocuments(self, fingerprints):
        docs = []
        for fp in fingerprints:
            if fp in self.fingerprintToDoc:
                docs.append(self.fingerprintToDoc[fp])

        return docs

    def printDB(self):
        print(self.fingerprintToDoc)

    def getNumKeys(self, find=None):
        if find == None:
            return len(self.fingerprintToDoc.keys())
        else:
            counter = 0
            for keys in self.fingerprintToDoc.keys():
                if keys[0] == find:
                    counter += 1
            return counter
