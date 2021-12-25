from abc import ABC
from typing_extensions import runtime
from nltk import parse

from .utils import dep_relation, semm, logical_form_mapping, procedure_semantic_translate
from .object import Procedure, Token, Relation, Pattern


class GrammaticalRelationStructure(ABC):
    # GrammaticalRelationStructure contains some manipulations on list of dependency relation, includes:
    # 1. add_query: get the question of the query, includes some relations: WH-TRAIN, WH-TIME and YN.
    # 2. add_pred: get the PRED relation.
    # 3. add_nsubj: get the NSUBJ relation.
    # 4. add_lobj: get the IOBJ relation.
    # 5. add_source: get the FROM-LOC relation.
    # 6. add_dest: get the TO-LOC relation.
    # 7. add_time: get the AT-TIME relation.

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
                self.query.append(Pattern('WH-RUNTIME', sem[0], sem[1]))
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
        self.lobj = GrammaticalRelationStructure()
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


class LogicalFormStructure(ABC):
    # LogicalFormStructure contains some manipulations on list of logical forms.
    def __init__(self):
        super().__init__()
        self.predicate = []
        self.pred = None
        self.agent = None
        self.subpred = None
        self.theme = None
        self.source = None
        self.dest = None
        self.time = None

    def add_predicate(self, gr):
        self.predicate = [logical_form_mapping(
            q) for q in gr.query] if gr.query else None
        return True if self.predicate else False

    def add_pred(self, gr):
        self.pred = logical_form_mapping(gr.pred) if gr.pred else None
        return True if self.pred else False

    def add_subpred(self, gr):
        if gr.lobj:
            self.subpred = LogicalFormStructure()
            self.subpred.add_pred(gr.lobj) if gr.lobj else None
            self.subpred.add_agent(gr.lobj) if gr.lobj else None
            self.subpred.add_source(gr.lobj) if gr.lobj else None
            self.subpred.add_dest(gr.lobj) if gr.lobj else None
            return True
        return False

    def add_theme(self, gr):
        self.theme = logical_form_mapping(gr.nmod) if gr.nmod else None
        return True if self.theme else False

    def add_agent(self, gr):
        self.agent = logical_form_mapping(gr.lsubj) if gr.lsubj else None
        return True if self.agent else False

    def add_source(self, gr):
        self.source = logical_form_mapping(gr.source) if gr.source else None
        return True if self.source else False

    def add_dest(self, gr):
        self.dest = logical_form_mapping(gr.dest) if gr.dest else None
        return True if self.dest else False

    def add_time(self, gr):
        self.time = logical_form_mapping(gr.time) if gr.time else None
        return True if self.time else False


class ProcedureSematicStructure(ABC):
    # ProcedureSematicStructure contains some manipulations on list of procedure semantics.
    def __init__(self):
        super().__init__()
        self.query = None
        self.train = None
        self.dtime = None
        self.atime = None
        self.rtime = None

    def add_query(self, head, var):
        self.query = Procedure(head, var)

    def add_train(self, var):
        self.train = Procedure('TRAIN', [var])

    def add_dtime(self, var_t, var_source, var_time):
        self.dtime = Procedure('DTIME', [var_t, var_source, var_time])

    def add_atime(self, var_t, var_dest, var_time):
        self.atime = Procedure('ATIME', [var_t, var_dest, var_time])

    def add_rtime(self, var_t, var_source, var_dest, var_time):
        self.rtime = Procedure(
            'RUN-TIME', [var_t, var_source, var_dest, var_time])


class NLP(ABC):
    # NLP contains some manipulation on input text, includes:
    # 1. tokenization: split a text into list of tokens.
    # 2. parse_tree: build a simple parse tree.
    # 3. dependency_relation: analysis dependency parsing of a query sentence in the database. This includes some more smaller manipulation like: leftArc, rightArc, shift and reduce.
    # 4. grammatical_relation: analysis grammatical relation based on dependency relations that have been analysized.
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
        # Return a GrammaticalRelationStructure object
        gr = GrammaticalRelationStructure()
        query = gr.add_query(dp_list)
        pred = gr.add_pred(dp_list)
        lsubj = gr.add_lsubj(dp_list)
        lobj = gr.add_lobj(dp_list)
        source = gr.add_source(dp_list)
        dest = gr.add_dest(dp_list)
        time = gr.add_time(dp_list)
        return gr, query, pred, lsubj, lobj, source, dest, time

    def logical_form(self, gr):
        # Return a LogicalFormStructure object
        lf = LogicalFormStructure()
        lf.add_predicate(gr)
        lf.add_pred(gr)
        lf.add_subpred(gr)
        lf.add_agent(gr)
        lf.add_theme(gr)
        lf.add_source(gr)
        lf.add_dest(gr)
        lf.add_time(gr)
        return lf

    def procedure_semantic(self, lf):
        # Return a ProcedureSematicStructure object
        ps_list = []
        for predicate in lf.predicate:
            ps = ProcedureSematicStructure()
            if not lf.subpred:
                train_var = procedure_semantic_translate(lf.agent, 'var')
                source_var = procedure_semantic_translate(
                    lf.source, 'var') if procedure_semantic_translate(lf.source, 'var') else '?source'
                dest_var = procedure_semantic_translate(
                    lf.dest, 'var') if procedure_semantic_translate(lf.dest, 'var') else '?dest'
                time_var = procedure_semantic_translate(
                    lf.time, 'var') if procedure_semantic_translate(lf.time, 'var') else '?at'
            else:
                train_var = procedure_semantic_translate(
                    lf.subpred.agent, 'var')
                source_var = procedure_semantic_translate(
                    lf.subpred.source, 'var') if procedure_semantic_translate(lf.subpred.source, 'var') else '?source'
                dest_var = procedure_semantic_translate(
                    lf.subpred.dest, 'var') if procedure_semantic_translate(lf.subpred.dest, 'var') else '?dest'
                time_var = procedure_semantic_translate(
                    lf.subpred.time, 'var') if procedure_semantic_translate(lf.subpred.time, 'var') else '?at'
            ps.add_query(procedure_semantic_translate(predicate, 'head'),
                         procedure_semantic_translate(predicate, 'var'))
            ps.add_train(train_var)
            ps.add_dtime(train_var, source_var, '?dt')
            ps.add_atime(train_var, dest_var, time_var)
            ps.add_rtime(train_var, source_var, dest_var, '?rt')
            ps_list.append(ps)
        return ps_list

    def retrieve_result(self, database, ps):
        # Return answers to a query with a given database
        if ps.query.head == 'PRINT-ALL':
            if ps.query.var == '?t':
                # ask for train
                train_list = database['train_list']
                candidate_list = [dtime[0] for dtime in database['dtime_list'] if (
                    ps.dtime.var[1] == '?source' or ps.dtime.var[1] == dtime[1]) and (ps.dtime.var[2] == '?dt' or ps.dtime.var[2] == dtime[2])]
                train_list = list(
                    filter(lambda train: train in train_list, candidate_list))

                candidate_list = [atime[0] for atime in database['atime_list'] if (
                    ps.atime.var[1] == '?dest' or ps.atime.var[1] == atime[1]) and (ps.atime.var[2] == '?at' or ps.atime.var[2] == atime[2])]
                train_list = list(
                    filter(lambda train: train in train_list, candidate_list))

                candidate_list = [rtime[0] for rtime in database['runtime_list'] if (
                    ps.rtime.var[1] == '?source' or ps.rtime.var[1] == rtime[1]) and (ps.rtime.var[2] == '?dest' or ps.rtime.var[2] == rtime[2]) and (ps.rtime.var[3] == '?rt' or ps.rtime.var[3] == rtime[3])]
                train_list = list(
                    filter(lambda train: train in train_list, candidate_list))

                return train_list
            if ps.query.var == '?rt':
                # ask for runtime
                runtime_list = [rtime[3] for rtime in database['runtime_list']]

                candidate_list = [rtime[3] for rtime in database['runtime_list'] if (ps.rtime.var[0] == '?t' or ps.rtime.var[0] == rtime[0]) and (
                    ps.rtime.var[1] == '?source' or ps.rtime.var[1] == rtime[1]) and (ps.rtime.var[2] == '?dest' or ps.rtime.var[2] == rtime[2])]

                return list(filter(lambda rtime: rtime in runtime_list, candidate_list))

            if ps.query.var == '?dt':
                dtime_list = [dtime[2] for dtime in database['dtime_list']]

                candidate_list = [dtime[2] for dtime in database['dtime_list'] if (
                    ps.dtime.var[1] == '?source' or ps.dtime.var[1] == dtime[1]) and (ps.dtime.var[2] == '?dt' or ps.dtime.var[2] == dtime[2])]

                return list(filter(lambda dtime: dtime in dtime_list, candidate_list))

            return []

        if ps.query.head == 'CHECK-ALL-TRUE':
            train_list = database['train_list']
            candidate_list = [dtime[0] for dtime in database['dtime_list'] if (
                ps.dtime.var[1] == '?source' or ps.dtime.var[1] == dtime[1]) and (ps.dtime.var[2] == '?dt' or ps.dtime.var[2] == dtime[2])]
            train_list = list(
                filter(lambda train: train in train_list, candidate_list))

            candidate_list = [atime[0] for atime in database['atime_list'] if (
                ps.atime.var[1] == '?dest' or ps.atime.var[1] == atime[1]) and (ps.atime.var[2] == '?at' or ps.atime.var[2] == atime[2])]
            train_list = list(
                filter(lambda train: train in train_list, candidate_list))

            candidate_list = [rtime[0] for rtime in database['runtime_list'] if (
                ps.rtime.var[1] == '?source' or ps.rtime.var[1] == rtime[1]) and (ps.rtime.var[2] == '?dest' or ps.rtime.var[2] == rtime[2]) and (ps.rtime.var[3] == '?rt' or ps.rtime.var[3] == rtime[3])]
            train_list = list(
                filter(lambda train: train in train_list, candidate_list))

            return ['Có'] if ps.train.var[0] in train_list else ['Không']

        return []
