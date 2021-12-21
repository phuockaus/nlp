from abc import ABC
from nltk import parse


class Token(ABC):
    # A token contains a word and its category which defined in grammar (view file "grammar.fcfg")
    def __init__(self, word, type):
        super().__init__()
        self.word = word
        self.type = type

    def __str__(self):
        return f'{self.word}({self.type})'

    def __repr__(self):
        return self.__str__()

    def getToken(self):
        return self


class Parser(ABC):
    # Parser contains some manipulation on input text, includes:
    # 1. tokenization: split a text into list of tokens.
    # 2. parse_tree: build a simple parse tree.
    # 3. dependency_relation: analysis dependency parsing of a query sentence in the database. This includes some more smaller manipulation like: leftArc, rightArc, shift and reduce.

    def __init__(self, grammar):
        # Parameter:
        # 1. grammar(Grammar): defined in file "grammar.fcfg", which contains the grammar of the system.
        super().__init__()
        self.grammar = parse.load_parser(grammar, trace=0)

    def tokenize(self, text):
        # Parameter:
        # 1. text(String): a sentence in string
        tree = self.parse_tree(text)
        token_list = []
        for s in tree.subtrees(lambda t: t.height() == 2):
            type = str(s.label())[12: -3]
            word = ' '.join(s.leaves())
            token_list.append(Token(word, type).getToken())
        return token_list

    def parse_tree(self, text):
        # Parameter:
        # 1. text(String): a sentence in string
        return self.grammar.parse_one(text.split())

    def dependency_relation(self, text):
        # Parameter:
        # 1. text(String): a sentence in string
        sigma = [Token('root', 'ROOT').getToken()]
        beta = self.tokenize(text)
        A = []
        while beta != []:
            relation = self.__relation(sigma[-1].type, beta[0].type)
            if relation == None:
                # Reduce
                sigma = sigma[:-1]
            elif relation[0] == 'shift':
                # Shift
                sigma.append(beta[0])
                beta = beta[1:]
            elif relation[0] == 'left':
                # LeftArc
                w1 = sigma[-1].word
                w2 = beta[0].word
                sigma = sigma[:-1]
                A.append(self.__rel(relation[1], w2, w1))
            else:
                # RightArc
                w1 = sigma[-1].word
                w2 = beta[0].word
                sigma.append(beta[0])
                beta = beta[1:]
                A.append(self.__rel(relation[1], w1, w2))
        return A

    @staticmethod
    def __rel(type, w1, w2):
        return f'{type}({w1}, {w2})'

    @classmethod
    def __relation(cls, t1, t2):
        relation = {
            # shift
            ('ROOT', 'TRAIN-N'): ('shift', None),
            ('ROOT', 'TIME-N'): ('shift', None),
            ('TRAIN-V', 'AT'): ('shift', None),
            ('TRAIN-V', 'FROM'): ('shift', None),
            ('TRAIN-V', 'TO'): ('shift', None),
            ('TIME-N', 'TRAIN-N'): ('shift', None),
            ('TRAIN-N', 'YN-BEGIN'): ('shift', None),

            # rightArc
            ('TRAIN-N', 'TRAIN-NAME'): ('right', 'nmod'),
            ('TRAIN-N', 'WHICH-QUERY'): ('right', 'det-wh'),
            ('ROOT', 'TRAIN-V'): ('right', 'root'),
            ('ROOT', 'TIME-V'): ('right', 'root'),
            ('CITY-N', 'CITY-NAME'): ('right', 'nmod'),
            ('TRAIN-V', 'CITY-N'): ('right', 'pobj'),
            ('TRAIN-V', 'CITY-NAME'): ('right', 'pobj'),
            ('TRAIN-V', 'TIME'): ('right', 'nmod'),
            ('TRAIN-V', 'SEMI-PUNCT'): ('right', 'semi'),
            ('TRAIN-V', 'TIME-QUERY'): ('right', 'nmod'),
            ('TRAIN-V', 'QUESTION-PUNCT'): ('right', 'punct'),
            ('TIME-N', 'TRAIN-V'): ('right', 'nmod'),
            ('TIME-V', 'TIME-QUERY'): ('right', 'iobj'),
            ('TIME-V', 'QUESTION-PUNCT'): ('right', 'punct'),
            ('TRAIN-V', 'YN-END'): ('right', 'wh-det'),

            # leftArc
            ('TRAIN-N', 'TRAIN-V'): ('left', 'nsubj'),
            ('TIME-N', 'TIME-V'): ('left', 'nsubj'),
            ('AT', 'TIME'): ('left', 'case'),
            ('AT', 'TIME-QUERY'): ('left', 'case'),
            ('FROM', 'CITY-NAME'): ('left', 'case'),
            ('TO', 'CITY-NAME'): ('left', 'case'),
            ('FROM', 'CITY-N'): ('left', 'case'),
            ('TO', 'CITY-N'): ('left', 'case'),
            ('YN-BEGIN', 'TRAIN-V'): ('left', 'wh-det'),
        }
        return relation.get((t1, t2), None)
