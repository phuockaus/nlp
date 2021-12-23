from abc import ABC
from nltk import parse
from .hierarchy import VAR, PRED, OBJECT


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

    # def getToken(self):
    #     return self

    def getWord(self):
        return self.word

    def getType(self):
        return self.type


class Relation(ABC):
    def __init__(self, relation, token_l, token_r):
        super().__init__()
        self.relation = relation
        self.token_l = token_l
        self.token_r = token_r

    def getRelation(self):
        return self.relation

    def getToken(self, pos='l'):
        if pos == 'l':
            return self.token_l
        return self.token_r


class Pattern(ABC):
    def __init__(self, relation, left, right):
        super().__init__()
        self.relation = relation
        self.left = left
        self.right = right

    def getRelation(self):
        return self.relation

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right


class LogicalForm(ABC):
    def __init__(self, role, var, sem):
        super().__init__()
        self.role = role
        self.var = var
        self.sem = sem

    def getRole(self):
        return self.role

    def getVar(self):
        return self.var

    def getSem(self):
        return self.sem


class GrammaticalRelation(ABC):
    def __init__(self):
        super().__init__()
        self.pred = None
        self.lsubj = None
        self.source = None
        self.dest = None
        self.time = None
        self.query = None
        self.variable = []

    def add_pred(self, dp_list):
        root = list(filter(lambda relation: relation.getRelation()
                           == 'root', dp_list))[0]
        sem = self.__sem(root.getToken('r').getType())
        self.pred = Pattern('PRED', sem[0], sem[1])
        return True

    def add_lsubj(self, dp_list):
        if not self.pred:
            return False
        nsubj_list = list(filter(lambda relation: relation.getRelation()
                                 == 'nsubj', dp_list))
        main_nsubj = list(filter(lambda relation: self.__sem(relation.getToken(
            'l').getType())[1].getValue() == self.pred.getRight().getValue(), nsubj_list))[0]
        sem = self.__sem(main_nsubj.getToken('r').getType())
        self.lsubj = Pattern('LSUBJ', self.pred.getLeft(), sem[0])
        return True

    def add_source(self, dp_list):
        if not self.pred or not self.lsubj:
            return False
        case_list = list(filter(lambda relation: relation.getRelation(
        ) == 'case' and relation.getToken('r').getType() == 'FROM', dp_list))
        if len(case_list) == 0:
            return False
        case = case_list[0]
        sem = self.__sem(case.getToken('l').getType(),
                         city=case.getToken('l').getWord())
        self.source = Pattern(
            'FROM-LOC', self.pred.getLeft(), LogicalForm('CITY-NAME', sem[0], sem[1]))
        return True

    def add_dest(self, dp_list):
        if not self.pred or not self.lsubj:
            return False
        if self.pred.getRight().getValue() == 'ARRIVE':
            pobj = list(filter(lambda relation: relation.getRelation()
                               == 'pobj', dp_list))[0]
            sem = self.__sem(pobj.getToken('r').getType(),
                             city=pobj.getToken('r').getWord())
            self.dest = Pattern(
                'TO-LOC', self.pred.getLeft(), LogicalForm('CITY-NAME', sem[0], sem[1]))
        else:
            case_list = list(filter(lambda relation: relation.getRelation(
            ) == 'case' and relation.getToken('r').getType() == 'TO', dp_list))
            if len(case_list) == 0:
                return False
            case = case_list[0]
            sem = self.__sem(case.getToken('l').getType(),
                             city=case.getToken('l').getWord())
            self.dest = Pattern(
                'TO-LOC', self.pred.getLeft(), LogicalForm('CITY-NAME', sem[0], sem[1]))
            return True

    def add_query(self, dp_list):
        r = list(filter(lambda relation: relation.getRelation()
                        == 'det-wh', dp_list))[0]
        sem = self.__sem(r.getToken('l').getType())
        self.query = Pattern('WH-TRAIN', sem[0], sem[1]) if sem[1].getObject(
        ) == 'TRAIN' else Pattern('WH-TIME', sem[0], sem[1])
        self.variable.append(sem[0])

    def add_time(self, action_v, time):
        self.time = Pattern('AT-TIME', action_v, time)

    def get(self):
        return self

    @staticmethod
    def __sem(type, city=None):
        variant_city = {
            'Huế': (VAR('h1'), OBJECT('HUE')),
            'Đà Nẵng': (VAR('d1'), OBJECT('DANANG')),
            'Hồ Chí Minh': (VAR('h2'), OBJECT('HCM'))
        }
        sematic = {
            'TRAIN-N': (VAR('t1'), OBJECT('TRAIN')),
            'TIME-N': (VAR('t2'), OBJECT('TIME')),
            'ARRIVE-V': (VAR('a1'), PRED('ARRIVE')),
            'TIME-V': (VAR('i1'), PRED('IS')),
            'RUN-V': (VAR('r1'), PRED('RUN')),
            'CITY-NAME': variant_city.get(city, None),
        }
        return sematic.get(type, None)


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
            token_list.append(Token(word, type))
        return token_list

    def parse_tree(self, text):
        # Parameter:
        # 1. text(String): a sentence in string
        return self.grammar.parse_one(text.split())

    def dependency_relation(self, text):
        # Parameter:
        # 1. text(String): a sentence in string
        sigma = [Token('root', 'ROOT')]
        beta = self.tokenize(text)
        A = []
        while beta != []:
            relation = self.__dep_relation(
                sigma[-1].getType(), beta[0].getType())
            if relation == None:
                # Reduce
                sigma = sigma[:-1]
            elif relation[0] == 'shift':
                # Shift
                sigma.append(beta[0])
                beta = beta[1:]
            elif relation[0] == 'left':
                # LeftArc
                w1 = sigma[-1]
                w2 = beta[0]
                sigma = sigma[:-1]
                A.append(Relation(relation[1], w2, w1))
            else:
                # RightArc
                w1 = sigma[-1]
                w2 = beta[0]
                sigma.append(beta[0])
                beta = beta[1:]
                A.append(Relation(relation[1], w1, w2))
        return A

    def grammatical_relation(self, dp_list):
        gr = GrammaticalRelation()
        gr.add_pred(dp_list)
        return gr

    @staticmethod
    def __dep_relation(t1, t2):
        relation = {
            # shift
            ('ROOT', 'TRAIN-N'): ('shift', None),
            ('ROOT', 'TRAIN-NAME'): ('shift', None),
            ('ROOT', 'TIME-N'): ('shift', None),
            ('RUN-V', 'AT'): ('shift', None),
            ('ARRIVE-V', 'AT'): ('shift', None),
            ('RUN-V', 'FROM'): ('shift', None),
            ('RUN-V', 'TO'): ('shift', None),
            ('TIME-N', 'TRAIN-N'): ('shift', None),
            ('TRAIN-NAME', 'YN-BEGIN'): ('shift', None),
            ('ARRIVE-V', 'CITY-N'): ('shift', None),
            ('FROM', 'CITY-N'): ('shift', None),
            ('TO', 'CITY-N'): ('shift', None),
            ('TIME-N', 'TRAIN-NAME'): ('shift', None),
            # ('RUN-V', 'CITY-N'): ('shift', None),

            # rightArc

            ('TRAIN-N', 'WHICH-QUERY'): ('right', 'det-wh'),
            ('ROOT', 'ARRIVE-V'): ('right', 'root'),
            ('ROOT', 'RUN-V'): ('right', 'root'),
            ('ROOT', 'TIME-V'): ('right', 'root'),
            ('ARRIVE-V', 'CITY-NAME'): ('right', 'pobj'),
            ('RUN-V', 'CITY-NAME'): ('right', 'pobj'),
            ('ARRIVE-V', 'TIME'): ('right', 'nmod'),
            ('RUN-V', 'TIME'): ('right', 'nmod'),
            ('RUN-V', 'SEMI-PUNCT'): ('right', 'semi'),
            ('RUN-V', 'TIME-QUERY'): ('right', 'nmod'),
            ('ARRIVE-V', 'QUESTION-PUNCT'): ('right', 'punct'),
            ('RUN-V', 'QUESTION-PUNCT'): ('right', 'punct'),
            ('TIME-N', 'RUN-V'): ('right', 'nmod'),
            ('TIME-V', 'TIME-QUERY'): ('right', 'det-wh'),
            ('TIME-V', 'QUESTION-PUNCT'): ('right', 'punct'),
            ('RUN-V', 'YN-END'): ('right', 'yn-det'),

            # leftArc
            ('TRAIN-N', 'TRAIN-NAME'): ('left', 'amod'),
            ('CITY-N', 'CITY-NAME'): ('left', 'amod'),
            ('TRAIN-N', 'ARRIVE-V'): ('left', 'nsubj'),
            ('TRAIN-N', 'RUN-V'): ('left', 'nsubj'),
            ('TRAIN-NAME', 'ARRIVE-V'): ('left', 'nsubj'),
            ('TRAIN-NAME', 'RUN-V'): ('left', 'nsubj'),
            ('TIME-N', 'TIME-V'): ('left', 'nsubj'),
            ('AT', 'TIME'): ('left', 'case'),
            ('AT', 'TIME-QUERY'): ('left', 'case'),
            ('FROM', 'CITY-NAME'): ('left', 'case'),
            ('TO', 'CITY-NAME'): ('left', 'case'),
            ('YN-BEGIN', 'RUN-V'): ('left', 'yn-det'),
        }
        return relation.get((t1, t2), None)
