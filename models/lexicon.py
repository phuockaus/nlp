from abc import ABC
from functools import reduce
import codecs


class Lexicon(ABC):
    def __init__(self, file):
        super().__init__()
        with codecs.open(file, encoding='utf-8') as f:
            self.data = [row for row in f]
            f.close()

    def getData(self):
        return self.data
