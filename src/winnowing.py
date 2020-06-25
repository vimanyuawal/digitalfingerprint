
import string
import sys
from collections import defaultdict
import os
from database import Database


__all__ = [
    'Fingerprint',
    'FingerprintException',
]


def guid(x): return ord(x)


class FingerprintException(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Fingerprint(object):
    """
    Generates fingerprints of the input text file or plain string. Please consider taking a look at http://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf for detailed description on how fingerprints are computed.
    Attributes:
        kgram_len (Optional[int]): length of the contiguous substring. Defaults to 50.
        base (Optional[int]): base required for computing the rolling hash function. Defaults to 101.
        modulo (Optional[int]): hash values cannot exceed this value. Defaults to sys.maxint.
        window_len (Optional[len]): length of the windows when computing fingerprints. Defaults to 100.
        kgrams (List(str)): k-grams extracted from the text
        hashes (List(int)): hash values of the k-grams
        fingerprints (List(tuple(int))): selected representative hash values along with their positions.
    """

    def __init__(self, kgram_len=None, base=None, modulo=None, window_len=None):
        self.kgram_len = kgram_len or 50
        self.base = base or 101
        self.modulo = modulo or sys.maxsize
        self.window_len = window_len or 100

    def get_min_with_pos(self, sequence):
        min_val = sys.maxsize
        min_pos = 0
        for pos, val in enumerate(sequence):
            if val <= min_val:
                min_val = val
                min_pos = pos
        return min_val, min_pos

    def normal_hash(self, kgram):
        hash = 0
        for i, c in enumerate(kgram):
            hash += guid(c) * self.base ** (self.kgram_len - 1 - i)
        hash = hash % self.modulo
        return hash

    def rolling_hash(self, old_hash, del_char, new_char):
        # more powerful version of rolling hash
        hash = ((old_hash - guid(del_char) * self.base **
                 self.kgram_len) + guid(new_char)) * self.base
        hash = hash % self.modulo
        return hash

    def prepare_storage(self):
        self.kgrams = []
        self.hashes = []
        self.fingerprints = []
        self.str = ""

    def generate_kgrams(self):
        self.kgrams = [self.str[i:i + self.kgram_len]
                       for i in range(len(self.str) - self.kgram_len + 1)]
        # print('Generating kgrams: ', self.kgrams)

    def hash_kgrams(self):
        prev_kgram = self.kgrams[0]
        prev_hash = self.normal_hash(prev_kgram)
        self.hashes.append(prev_hash)

        for cur_kgram in self.kgrams[1:]:
            prev_hash = self.rolling_hash(
                prev_hash, prev_kgram[0], cur_kgram[-1])
            # if(prev_hash == 0):
            #     print(cur_kgram, prev_kgram)
            self.hashes.append(prev_hash)
            prev_kgram = cur_kgram

        # print("hashes: ", self.hashes)

    def generate_fingerprints(self):
        windows = [self.hashes[i:i + self.window_len]
                   for i in range(len(self.hashes) - self.window_len + 1)]

        cur_min_hash, cur_min_pos = self.get_min_with_pos(windows[0])
        self.fingerprints.append((cur_min_hash, cur_min_pos))

        for i, window in enumerate(windows[1:]):
            min_hash, min_pos = self.get_min_with_pos(window)
            min_pos += i + 1
            if min_hash != cur_min_hash or min_hash == cur_min_hash and min_pos > cur_min_pos:
                cur_min_hash, cur_min_pos = min_hash, min_pos
                self.fingerprints.append((min_hash, min_pos))

        # print('fingerprints: ', self.fingerprints)

    def validate_config(self):
        if len(self.str) < self.window_len:
            raise FingerprintException(
                "Length of the string is smaller than the length of the window.")

    def sanitize(self, str):
        sanitized = ""
        exclude = string.punctuation
        for c in str:
            if c not in exclude and c not in ('\n', '\r', ' '):
                sanitized += c
        return sanitized

    def checkHashing(self):
        print('Checking hashing function...')
        print('The kgrams were hashed into ' + str(len(self.hashes)) + ' hashes. Out of these ' + str(len(self.fingerprints)
                                                                                                      ) + ' were chosen as fingerprints. This means a selection % of ' + str(len(self.fingerprints)/len(self.hashes)) + ' compared to an expected % of ' + str(2/(1+self.window_len)))
        fq = defaultdict(int)
        for hash in self.hashes:
            fq[hash] += 1
            if fq[hash] > 1:
                print('alert')

    def generate(self, str=None, fpath=None):
        """generates fingerprints of the input. Either provide `str` to compute fingerprint directly from your string or `fpath` to compute fingerprint from the text of the file. Make sure to have your text decoded in `utf-8` format if you pass the input string.
        Args:
            str (Optional(str)): string whose fingerprint is to be computed.
            fpath (Optional(str)): absolute path of the text file whose fingerprint is to be computed.
        Returns:
            List(int): fingerprints of the input.
        Raises:
            FingerprintException: If the input string do not meet the requirements of parameters provided for fingerprinting.
        """
        self.prepare_storage()
        self.str = self.load_file(fpath) if fpath else self.sanitize(str)
        self.validate_config()
        self.generate_kgrams()
        self.hash_kgrams()
        self.generate_fingerprints()
        # self.checkHashing()
        return self.fingerprints

    def load_file(self, fpath):
        with open(fpath, 'r') as fp:
            data = fp.read()
        data = data.encode().decode('utf-8')
        data = data.strip('\x00')
        data = data.replace('\x00', '')
        return data


def saveTemplatesToDatabase(f, db):
    template_address = './data/Templates_txt/'
    # we can keep a nested loop here because the documents to be checked will be >> our templates in an average case so it makes sense to arrange our data in a { fingerprint : [doc_addresses] }
    for template in os.listdir(template_address):
        fingerprints = f.generate(fpath=template_address+template)
        db.add(fingerprints, template_address+template)


def checkSimilarity(fingerprints, db):
    docs = db.getDocuments(fingerprints)
    print(docs)


def results(mutual, nonmutual, reciprocal):

    # print('% of documents Reciprocal NDA: ', ((type1/total)*100))
    # print('% of documents Non mutual NDA: ', ((type2/total)*100))
    # print('% of documents Mutual NDA: ',
    #       100*(1 - (type1+type2)/total))

    # print('Accuracy of mutual: ')
    # sorted()

    # print('Accuracy of nonmutual: ')
    print('\n \n \n')

    predictedReciprocal = set(reciprocal)
    actualReciprocal = set(os.listdir('./data/Classification/Reciprocal/'))

    truePositive = predictedReciprocal.intersection(actualReciprocal)
    falsePositive = predictedReciprocal.difference(actualReciprocal)
    trueNegative = set()
    falseNegative = actualReciprocal.difference(predictedReciprocal)

    print('\t \t \t \t Reciprocal (actual) \t \t Not Reciprocal (actual)')
    print('Reciprocal (predicted) \t \t \t' + str(len(truePositive)) +
          ' \t \t \t \t' + str(len(falsePositive)))
    print('NonReciprocal (predicted) \t \t' +
          str(len(falseNegative)) + ' \t \t \t \t' + str(len(trueNegative))+'\n \n')

    print('\n\n The files that we thought were reciprocal but were not in actuality: ' + str(falsePositive))
    print('\n\n The files that we thought were non-reciprocal but were reciprocal in actuality: ' + str(falseNegative))


if __name__ == "__main__":
    window_len = 2
    kgram_len = 1
    f = Fingerprint(kgram_len=kgram_len, window_len=window_len)
    db = Database()
    saveTemplatesToDatabase(f, db)
    filepath = './data/Docs_txt/'
    # print(db.printDB())
    template1a = './data/Templates_txt/Reciprocal NDA.txt'
    template1b = './data/Templates_txt/Mutual NDA.txt'
    template2 = './data/Templates_txt/Non-Mutual NDA.txt'

    type1 = 0
    type2 = 0

    reciprocal = []
    nonmutual = []
    unclassified = []

    total = len(os.listdir(filepath))
    for file in os.listdir(filepath):
        p = open(filepath+file, 'r')
        text = p.read()
        p.close()
        if len(text) >= window_len:
            sample = f.generate(fpath=filepath+file)
            score = db.getJaccardScore(sample)
            # print(score[template1], score[template2])
            if score[template1a] > score[template2] or score[template1b] > score[template2]:
                type1 += 1
                # print('Reciprocal NDA')
                reciprocal.append(file)
            elif score[template2] > score[template1a] and score[template2] > score[template1b]:
                type2 += 1
                # print('Non mutual NDA')
                nonmutual.append(file)
            else:
                # print('Mutual NDA')
                unclassified.append(file)

    # db.printDB()
    results(unclassified, nonmutual, reciprocal)


# does positioning matter? maybe, maybe not
