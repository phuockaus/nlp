from abc import ABC
from nltk import parse

from .utils import dep_relation, semm


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


# class LogicalForm(ABC):
#     def __init__(self, role, var, sem):
#         super().__init__()
#         self.role = role
#         self.var = var
#         self.sem = sem

#     def getRole(self):
#         return self.role

#     def getVar(self):
#         return self.var

#     def getSem(self):
#         return self.sem


class GrammaticalRelation(ABC):
    def __init__(self):
        super().__init__()
        self.pred = None
        self.lsubj = None
        self.lobj = None
        self.source = None
        self.dest = None
        self.time = None
        self.query = []
        self.nmod = None
        self.variable = []

    def add_query(self, dp_list):
        wh_list = list(filter(lambda relation: relation.getRelation()
                              == 'det-wh', dp_list))
        if len(wh_list) != 0:
            # Wh question
            wh = wh_list[0]
            if wh.getToken('l').getType() == 'TRAIN-N':
                sem = semm(wh.getToken('l').getType())
                self.query.append(Pattern('WH-TRAIN', sem[0], sem[1]))
            elif wh.getToken('r').getType() == 'TIME-QUERY':
                sem = semm(wh.getToken('r').getType())
                self.query.append(Pattern('WH-TIME', sem[0], sem[1]))
            else:
                return False
        else:
            self.query.append(Pattern('YN', None, None))

        return True

    def add_pred(self, dp_list):
        root = list(filter(lambda relation: relation.getRelation()
                           == 'root', dp_list))[0]
        sem = semm(root.getToken('r').getType())
        self.pred = Pattern('PRED', sem[0], sem[1])
        return True

    def add_lsubj(self, dp_list):
        if not self.pred:
            return False
        nsubj_list = list(filter(lambda relation: relation.getRelation()
                                 == 'nsubj', dp_list))
        main_nsubj = list(filter(lambda relation: semm(relation.getToken(
            'l').getType())[1].getValue() == self.pred.getRight().getValue(), nsubj_list))[0]
        sem = semm(main_nsubj.getToken('r').getType(),
                   train=main_nsubj.getToken('r').getWord())
        self.lsubj = Pattern('LSUBJ', self.pred.getLeft(), sem[0])
        return True

    def add_lobj(self, dp_list):
        if not self.pred or not self.lsubj:
            return False
        nmod_list = list(
            filter(lambda relation: relation.getRelation() == 'nmod', dp_list))
        if len(nmod_list) == 0:
            return False
        nmod = nmod_list[0]
        sem = semm(nmod.getToken('r').getType())
        self.lobj = GrammaticalRelation()
        new_dp_list = list(filter(lambda relation: relation.getRelation(
        ) != 'root' and relation.getRelation() != 'nmod', dp_list))
        new_dp_list.append(
            Relation('root', nmod.getToken('l'), nmod.getToken('r')))
        self.nmod = Pattern('IOBJ', self.pred.getLeft(), sem[0])
        self.lobj.add_pred(new_dp_list)
        self.lobj.add_lsubj(new_dp_list)
        self.lobj.add_dest(new_dp_list)
        self.lobj.add_source(new_dp_list)
        return True

    def add_source(self, dp_list):
        if not self.pred or not self.lsubj:
            return False
        if self.lobj and self.lobj.pred and self.lobj.lsubj and (self.lobj.pred.getRight().getValue() == 'ARRIVE' or self.lobj.pred.getRight().getValue() == 'RUN'):
            return False
        case_list = list(filter(lambda relation: relation.getRelation(
        ) == 'case' and relation.getToken('r').getType() == 'FROM', dp_list))
        if len(case_list) == 0:
            return False
        case = case_list[0]
        sem = semm(case.getToken('l').getType(),
                   city=case.getToken('l').getWord())
        self.source = Pattern(
            'FROM-LOC', self.pred.getLeft(), sem[0])
        return True

    def add_dest(self, dp_list):
        if not self.pred or not self.lsubj:
            return False
        if self.lobj and self.lobj.pred and self.lobj.lsubj and (self.lobj.pred.getRight().getValue() == 'ARRIVE' or self.lobj.pred.getRight().getValue() == 'RUN'):
            return False
        if self.pred.getRight().getValue() == 'ARRIVE':
            pobj = list(filter(lambda relation: relation.getRelation()
                               == 'dobj', dp_list))[0]
            sem = semm(pobj.getToken('r').getType(),
                       city=pobj.getToken('r').getWord())
            self.dest = Pattern(
                'TO-LOC', self.pred.getLeft(), sem[0])
        else:
            case_list = list(filter(lambda relation: relation.getRelation(
            ) == 'case' and relation.getToken('r').getType() == 'TO', dp_list))
            if len(case_list) == 0:
                return False
            case = case_list[0]
            sem = semm(case.getToken('l').getType(),
                       city=case.getToken('l').getWord())
            self.dest = Pattern(
                'TO-LOC', self.pred.getLeft(), sem[0])
        return True

    def add_time(self, dp_list):
        if not self.pred or not self.lsubj:
            return False
        case_list = list(filter(lambda relation: relation.getRelation(
        ) == 'case' and relation.getToken('r').getType() == 'AT', dp_list))
        if len(case_list) == 0:
            return False
        case = case_list[0]
        if case.getToken('l').getType() == 'TIME-QUERY':
            sem = semm(case.getToken('l').getType())
            self.query.append(Pattern('WH-TIME', sem[0], sem[1]))
            self.time = Pattern('AT-TIME', self.pred.getLeft(), sem[0])
        sem = semm(case.getToken('l').getType(),
                   time=case.getToken('l').getWord())
        self.time = Pattern(
            'AT-TIME', self.pred.getLeft(), sem[0])
        return True

    def get(self):
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
            relation = dep_relation(
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
