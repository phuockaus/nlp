from .hierarchy import VAR, PRED, OBJECT
from abc import ABC


def read_file(folder):
    return [(f'{folder}{index}.txt', index) for index in range(1, 7)]


def dep_relation(t1, t2):
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
        ('ARRIVE-V', 'CITY-NAME'): ('right', 'dobj'),
        ('RUN-V', 'CITY-NAME'): ('right', 'dobj'),
        ('ARRIVE-V', 'TIME'): ('right', 'pobj'),
        ('RUN-V', 'TIME'): ('right', 'pobj'),
        ('RUN-V', 'SEMI-PUNCT'): ('right', 'semi'),
        ('RUN-V', 'TIME-QUERY'): ('right', 'pobj'),
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


def semm(type, city=None, time=None, train=None):
    variant_city = {
        'Huế': (LogicalForm('CITY-NAME', VAR('h1'), OBJECT('HUE')), None),
        'Đà Nẵng': (LogicalForm('CITY-NAME', VAR('d1'), OBJECT('DANANG')), None),
        'Hồ Chí Minh': (LogicalForm('CITY-NAME', VAR('h2'), OBJECT('HCM')), None),
        'Hà Nội': (LogicalForm('CITY-NAME', VAR('h3'), OBJECT('HANOI')), None),
        'Nha Trang': (LogicalForm('CITY-NAME', VAR('n1'), OBJECT('NHATRANG')), None)
    }
    variant_time = {
        '0:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('0:00HR')), None),
        '0:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('0:30HR')), None),
        '1:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('1:00HR')), None),
        '1:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('1:30HR')), None),
        '2:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('2:00HR')), None),
        '2:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('2:30HR')), None),
        '3:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('3:00HR')), None),
        '3:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('3:30HR')), None),
        '4:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('4:00HR')), None),
        '4:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('4:30HR')), None),
        '5:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('5:00HR')), None),
        '5:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('5:30HR')), None),
        '6:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('6:00HR')), None),
        '6:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('6:30HR')), None),
        '7:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('7:00HR')), None),
        '7:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('7:30HR')), None),
        '8:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('8:00HR')), None),
        '8:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('8:30HR')), None),
        '9:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('9:00HR')), None),
        '9:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('9:30HR')), None),
        '10:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('10:00HR')), None),
        '10:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('10:30HR')), None),
        '11:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('11:00HR')), None),
        '11:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('11:30HR')), None),
        '12:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('12:00HR')), None),
        '12:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('12:30HR')), None),
        '13:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('13:00HR')), None),
        '13:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('13:30HR')), None),
        '14:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('14:00HR')), None),
        '14:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('14:30HR')), None),
        '15:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('15:00HR')), None),
        '15:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('15:30HR')), None),
        '16:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('16:00HR')), None),
        '16:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('16:30HR')), None),
        '17:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('17:00HR')), None),
        '17:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('17:30HR')), None),
        '18:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('18:00HR')), None),
        '18:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('18:30HR')), None),
        '19:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('19:00HR')), None),
        '19:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('19:30HR')), None),
        '20:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('20:00HR')), None),
        '20:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('20:30HR')), None),
        '21:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('21:00HR')), None),
        '21:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('21:30HR')), None),
        '22:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('22:00HR')), None),
        '22:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('22:30HR')), None),
        '23:00HR': (LogicalForm('TIME', VAR('t3'), OBJECT('23:00HR')), None),
        '23:30HR': (LogicalForm('TIME', VAR('t3'), OBJECT('23:30HR')), None),
    }
    variant_train = {
        'B1': (LogicalForm('TRAIN-NAME', VAR('b1'), OBJECT('B1')), None),
        'B2': (LogicalForm('TRAIN-NAME', VAR('b1'), OBJECT('B2')), None),
        'B3': (LogicalForm('TRAIN-NAME', VAR('b1'), OBJECT('B3')), None),
        'B4': (LogicalForm('TRAIN-NAME', VAR('b1'), OBJECT('B4')), None),
        'B5': (LogicalForm('TRAIN-NAME', VAR('b1'), OBJECT('B5')), None),
    }
    sematic = {
        'TRAIN-N': (VAR('t1'), OBJECT('TRAIN')),
        'TIME-N': (VAR('t2'), OBJECT('TIME')),
        'ARRIVE-V': (VAR('a1'), PRED('ARRIVE')),
        'TIME-V': (VAR('i1'), PRED('IS')),
        'RUN-V': (VAR('r1'), PRED('RUN')),
        'CITY-NAME': variant_city.get(city, None),
        'TIME': variant_time.get(time, None),
        'TIME-QUERY': (VAR('t2'), OBJECT('TIME')),
        'TRAIN-NAME': variant_train.get(train, None),
    }
    return sematic.get(type, None)


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


class GRPrinter(ABC):
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
    def __printLF(object):
        role = object.getRole()
        var = object.getVar().getValue()
        sem = object.getSem().getValue()
        return f'({role} {var} {sem})'

    @ classmethod
    def __printPattern(cls, gr):
        left = gr.getLeft().getValue()
        rel = gr.getRelation()
        right = gr.getRight().getValue() if type(
            gr.getRight()) != LogicalForm else cls.__printLF(gr.getRight())
        return f'({left} {rel} {right})\n'

    @ staticmethod
    def __printYN(gr):
        return f'({gr.getRelation()})\n'
