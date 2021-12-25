from abc import ABC


class ROOT(ABC):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def getValue(self):
        return self.value


class VAR(ROOT):
    def __init__(self, var):
        super().__init__(var)


class PRED(ROOT):
    def __init__(self, pred):
        super().__init__(pred)


class OBJECT(ROOT):
    def __init__(self, object):
        super().__init__(object)


class Token(ABC):
    # A token contains a word and its category which defined in grammar (view file "grammar.fcfg")
    # Parameters:
    # 1. Word(string): represent word.
    # 2. Type(string): represent category.
    def __init__(self, word, type):
        super().__init__()
        self.word = word
        self.type = type

    def __str__(self):
        return f'{self.word}({self.type})'

    def __repr__(self):
        return self.__str__()

    def getWord(self):
        return self.word

    def getType(self):
        return self.type


class Relation(ABC):
    # A relation contains a dependency relation of 2 tokens in a query.
    # 1. relation(string): represent relation.
    # 2. token_l(string): represent token 1.
    # 3. token_r(string): represent token 2.
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
    # A relation contains a grammatical relation of 2 objects.
    # 1. relation(string): represent relation.
    # 2. left(string): represent object 1.
    # 3. right(string): represent object 2.
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
    def __init__(self, var, sem):
        super().__init__()
        self.var = var
        self.sem = sem

    def getVar(self):
        return self.var

    def getSem(self):
        return self.sem


class UnaryLogicalForm(LogicalForm):
    def __init__(self, var, sem):
        super().__init__(var, sem)


class BinaryLogicalForm(LogicalForm):
    def __init__(self, var, sem, role):
        super().__init__(var, sem)
        self.role = role

    def getRole(self):
        return self.role


class Predicate(UnaryLogicalForm):
    def __init__(self, var, sem):
        super().__init__(var, sem)


class Procedure(ABC):
    def __init__(self, head, var):
        super().__init__()
        self.head = head
        self.var = var

    def getHead(self):
        return self.head

    def getVar(self):
        return self.var


class ObjectForm(ABC):
    # Define the Object Form of an object.
    def __init__(self, category, var, sem):
        super().__init__()
        self.category = category
        self.var = var
        self.sem = sem

    def getCategory(self):
        return self.category

    def getVar(self):
        return self.var

    def getSem(self):
        return self.sem


class GRPrinter(ABC):
    # GRPrinter helps format the output of grammatical relations.
    def __init__(self, gr):
        super().__init__()
        self.gr = gr

    def print_query(self):
        ql = []
        for q in self.gr.query:
            if q.getRelation() == 'YN':
                ql.append(self.__printYN(q))
            else:
                ql.append(self.__printPattern(q))
        return ''.join(ql)

    def print_pred(self):
        return self.__printPattern(self.gr.pred)

    def print_lsubj(self):
        return self.__printPattern(self.gr.lsubj)

    def print_lobj(self):
        pred = self.__printPattern(self.gr.lobj.pred)
        nmod = self.__printPattern(self.gr.nmod)
        lsubj = self.__printPattern(self.gr.lobj.lsubj)
        source = self.__printPattern(self.gr.lobj.source)
        dest = self.__printPattern(self.gr.lobj.dest)
        return f'{pred}{nmod}{lsubj}{source}{dest}'

    def print_source(self):
        return self.__printPattern(self.gr.source)

    def print_dest(self):
        return self.__printPattern(self.gr.dest)

    def print_time(self):
        return self.__printPattern(self.gr.time)

    @ staticmethod
    def __printOF(object):
        category = object.getCategory()
        var = object.getVar().getValue()
        sem = object.getSem().getValue()
        return f'({category} {var} {sem})'

    @ classmethod
    def __printPattern(cls, gr):
        left = gr.getLeft().getValue()
        rel = gr.getRelation()
        right = gr.getRight().getValue() if type(
            gr.getRight()) != ObjectForm else cls.__printOF(gr.getRight())
        return f'({left} {rel} {right})\n'

    @ staticmethod
    def __printYN(gr):
        return f'({gr.getRelation()})\n'


class LFPrinter(ABC):
    def __init__(self, lf):
        super().__init__()
        self.lf = lf

    def print(self):
        content = []
        sub_printer = LFPrinter(self.lf.subpred) if self.lf.subpred else None
        sub_content = f'({sub_printer.print()})' if sub_printer else ''

        content.append(self.__printUnary(self.lf.pred)
                       ) if self.lf.pred else None
        content.append(self.__printBinary(self.lf.agent)
                       ) if self.lf.agent else None
        content.append(sub_content)
        content.append(self.__printBinary(self.lf.theme)
                       ) if self.lf.theme else None
        content.append(self.__printBinary(self.lf.source)
                       ) if self.lf.source else None
        content.append(self.__printBinary(self.lf.dest)
                       ) if self.lf.dest else None
        content.append(self.__printBinary(self.lf.time)
                       ) if self.lf.time else None

        predicate = [self.__printPredicate(
            lf) for lf in self.lf.predicate] if self.lf.predicate else []

        close_bracket = [')' for _ in range(
            len(predicate))]
        return ' '.join(predicate) + ''.join(content) + ''.join(close_bracket)

    @ staticmethod
    def __printOF(object):
        category = object.getCategory()
        var = object.getVar().getValue()
        sem = object.getSem().getValue()
        return f'({category} {var} {sem})'

    @ staticmethod
    def __printUnary(lf):
        var = lf.getVar().getValue()
        sem = lf.getSem().getValue()
        return f'({sem} {var})'

    @ staticmethod
    def __printPredicate(lf):
        if (lf.getVar() == None):
            return '(YN :'
        var = lf.getVar().getValue()
        sem = lf.getSem()
        return f'({sem} {var}: '

    @ classmethod
    def __printBinary(cls, lf):
        var = lf.getVar().getValue()
        sem = lf.getSem().getValue() if type(
            lf.getSem()) != ObjectForm else cls.__printOF(lf.getSem())
        role = lf.getRole()
        return f'({role} {var} {sem})'

    @ staticmethod
    def __printYN(lf):
        return f'{lf.getRole()}: '
