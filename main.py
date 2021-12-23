from models.utils import read_file
from models.grammar import Parser
import codecs


def main():
    # Loading parser
    print('Loading grammar...')
    nlp_parser = Parser('models/grammar.fcfg')
    print('Loading done!')

    # Read input files
    print('Reading file...')
    input_file_list = read_file('input/queries/')
    print('Reading done!')

    # Dependency parsing analysis
    print('Dependency parsing analysis...')
    dp_list = []
    for file in input_file_list:
        with codecs.open(file[0], encoding='utf-8') as f:
            data = f.read()
            f.close()
        dp_list.append((nlp_parser.dependency_relation(data), file[1]))

    # Write results to a file
    with codecs.open('output/output_b.txt', 'w', encoding='utf-8') as out_f:
        for result in dp_list:
            out_f.write(f'Query {result[1]}:\n')
            for relation in result[0]:
                token_l = relation.getToken('l').getWord()
                token_r = relation.getToken('r').getWord()
                out_f.write(
                    f'{relation.getRelation()} ({token_l}, {token_r})\n')
            out_f.write('-----------------------------------------------\n')
        out_f.close()
    print('Analysis done! See results of dependency parsing analysis in the file "output_b.txt".')

    test_data = dp_list[5][0]
    gr = nlp_parser.grammatical_relation(test_data)
    if gr.add_pred(test_data):
        print(gr.pred.getLeft().getValue() + ' ' +
              gr.pred.getRelation() + ' ' + gr.pred.getRight().getValue())
    if gr.add_lsubj(test_data):
        print(gr.lsubj.getLeft().getValue() + ' ' +
              gr.lsubj.getRelation() + ' ' + gr.lsubj.getRight().getValue())
    if gr.add_source(test_data):
        print(gr.source.getLeft().getValue() + ' ' +
              gr.source.getRelation() + ' (' + gr.source.getRight().getRole() + ' ' + gr.source.getRight().getVar().getValue() + ' ' + gr.source.getRight().getSem().getValue() + ')')
    if gr.add_dest(test_data):
        print(gr.dest.getLeft().getValue() + ' ' +
              gr.dest.getRelation() + ' (' + gr.dest.getRight().getRole() + ' ' + gr.dest.getRight().getVar().getValue() + ' ' + gr.dest.getRight().getSem().getValue() + ')')
    if gr.add_time(test_data):
        print(gr.time.getLeft().getValue() + ' ' +
              gr.time.getRelation() + ' (' + gr.time.getRight().getRole() + ' ' + gr.time.getRight().getVar().getValue() + ' ' + gr.time.getRight().getSem().getValue() + ')')
    if gr.add_query(test_data):
        print(gr.query.getLeft().getValue() + ' ' +
              gr.query.getRelation() + ' ' + gr.query.getRight().getValue())


if __name__ == '__main__':
    main()
