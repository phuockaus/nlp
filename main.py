from models.utils import GRPrinter, read_file
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

    print('Grammatical Relation analysis...')
    gr_list = []
    with codecs.open('output/output_c.txt', 'w', encoding='utf-8') as out_f:
        for dp in dp_list:
            out_f.write(f'Query {dp[1]}:\n')

            # Grammatical relation analysis
            gr, query, pred, lsubj, lobj, source, dest, time = nlp_parser.grammatical_relation(
                dp[0])
            gr_list.append(gr)
            printer = GRPrinter(gr)

            # Write results to a file
            if query:
                out_f.write(printer.print_query())
            if pred:
                out_f.write(printer.print_pred())
            if lsubj:
                out_f.write(printer.print_lsubj())
            if lobj:
                out_f.write(printer.print_lobj())
            if source:
                out_f.write(printer.print_source())
            if dest:
                out_f.write(printer.print_dest())
            if time:
                out_f.write(printer.print_time())

            out_f.write('-----------------------------------------------\n')
        out_f.close()

    print('Analysis done! See results of grammatical relation analysis in the file "output_c.txt".')


if __name__ == '__main__':
    main()
