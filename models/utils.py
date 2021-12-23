from .hierarchy import VAR, PRED, OBJECT


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


def semm(type, city=None, time=None):
    variant_city = {
        'Huế': (VAR('h1'), OBJECT('HUE')),
        'Đà Nẵng': (VAR('d1'), OBJECT('DANANG')),
        'Hồ Chí Minh': (VAR('h2'), OBJECT('HCM'))
    }
    variant_time = {
        '0:00HR': (VAR('t3'), OBJECT('0:00HR')),
        '0:30HR': (VAR('t3'), OBJECT('0:30HR')),
        '1:00HR': (VAR('t3'), OBJECT('1:00HR')),
        '1:30HR': (VAR('t3'), OBJECT('1:30HR')),
        '2:00HR': (VAR('t3'), OBJECT('2:00HR')),
        '2:30HR': (VAR('t3'), OBJECT('2:30HR')),
        '3:00HR': (VAR('t3'), OBJECT('3:00HR')),
        '3:30HR': (VAR('t3'), OBJECT('3:30HR')),
        '4:00HR': (VAR('t3'), OBJECT('4:00HR')),
        '4:30HR': (VAR('t3'), OBJECT('4:30HR')),
        '5:00HR': (VAR('t3'), OBJECT('5:00HR')),
        '5:30HR': (VAR('t3'), OBJECT('5:30HR')),
        '6:00HR': (VAR('t3'), OBJECT('6:00HR')),
        '6:30HR': (VAR('t3'), OBJECT('6:30HR')),
        '7:00HR': (VAR('t3'), OBJECT('7:00HR')),
        '7:30HR': (VAR('t3'), OBJECT('7:30HR')),
        '8:00HR': (VAR('t3'), OBJECT('8:00HR')),
        '8:30HR': (VAR('t3'), OBJECT('8:30HR')),
        '9:00HR': (VAR('t3'), OBJECT('9:00HR')),
        '9:30HR': (VAR('t3'), OBJECT('9:30HR')),
        '10:00HR': (VAR('t3'), OBJECT('10:00HR')),
        '10:30HR': (VAR('t3'), OBJECT('10:30HR')),
        '11:00HR': (VAR('t3'), OBJECT('11:00HR')),
        '11:30HR': (VAR('t3'), OBJECT('11:30HR')),
        '12:00HR': (VAR('t3'), OBJECT('12:00HR')),
        '12:30HR': (VAR('t3'), OBJECT('12:30HR')),
        '13:00HR': (VAR('t3'), OBJECT('13:00HR')),
        '13:30HR': (VAR('t3'), OBJECT('13:30HR')),
        '14:00HR': (VAR('t3'), OBJECT('14:00HR')),
        '14:30HR': (VAR('t3'), OBJECT('14:30HR')),
        '15:00HR': (VAR('t3'), OBJECT('15:00HR')),
        '15:30HR': (VAR('t3'), OBJECT('15:30HR')),
        '16:00HR': (VAR('t3'), OBJECT('16:00HR')),
        '16:30HR': (VAR('t3'), OBJECT('16:30HR')),
        '17:00HR': (VAR('t3'), OBJECT('17:00HR')),
        '17:30HR': (VAR('t3'), OBJECT('17:30HR')),
        '18:00HR': (VAR('t3'), OBJECT('18:00HR')),
        '18:30HR': (VAR('t3'), OBJECT('18:30HR')),
        '19:00HR': (VAR('t3'), OBJECT('19:00HR')),
        '19:30HR': (VAR('t3'), OBJECT('19:30HR')),
        '20:00HR': (VAR('t3'), OBJECT('20:00HR')),
        '20:30HR': (VAR('t3'), OBJECT('20:30HR')),
        '21:00HR': (VAR('t3'), OBJECT('21:00HR')),
        '21:30HR': (VAR('t3'), OBJECT('21:30HR')),
        '22:00HR': (VAR('t3'), OBJECT('22:00HR')),
        '22:30HR': (VAR('t3'), OBJECT('22:30HR')),
        '23:00HR': (VAR('t3'), OBJECT('23:00HR')),
        '23:30HR': (VAR('t3'), OBJECT('23:30HR')),
    }
    sematic = {
        'TRAIN-N': (VAR('t1'), OBJECT('TRAIN')),
        'TIME-N': (VAR('t2'), OBJECT('TIME')),
        'ARRIVE-V': (VAR('a1'), PRED('ARRIVE')),
        'TIME-V': (VAR('i1'), PRED('IS')),
        'RUN-V': (VAR('r1'), PRED('RUN')),
        'CITY-NAME': variant_city.get(city, None),
        'TIME': variant_time.get(time, None),
        'TIME-QUERY': (VAR('t2'), OBJECT('TIME'))
    }
    return sematic.get(type, None)
