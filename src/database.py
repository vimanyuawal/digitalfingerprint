class Database:
    def __init__(self):
        self.templateToFingerprints = {}

    def add(self, fingerprints, docpath):
        self.templateToFingerprints[docpath] = set(fingerprints)

    def getJaccardScore(self, fingerprints):
        setOfFingerprints = set(fingerprints)
        templateToScore = {}
        for template in self.templateToFingerprints.keys():
            # print(template)
            templateFingerprints = self.templateToFingerprints[template]
            jscore = (len(setOfFingerprints.intersection(
                templateFingerprints))/(len(setOfFingerprints.union(templateFingerprints))))
            templateToScore[template] = jscore

        return templateToScore

    def printDB(self):
        print(self.templateToFingerprints)
