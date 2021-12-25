from models.database import Database
from models.utils import read_file, write_answer
from models.object import LFPrinter, GRPrinter, PSPrinter
from models.grammar import NLP
import codecs


def main():
    # Loading parser
    try:
        print('Loading grammar...')
        nlp_master = NLP('models/grammar.fcfg')
        print('Loading done!')
    except:
        print('Error: Cannot loading parser!')
        return

    # Read input files
    try:
        print('Reading file...')
        input_file_list = read_file('input/queries/')
        print('Reading done!')
    except:
        print('Error: Cannot read input files!')
        return

    # Dependency parsing analysis
    print('Dependency parsing analysis...')
    dp_list = []
    for file in input_file_list:
        with codecs.open(file[0], encoding='utf-8') as f:
            data = f.read()
            f.close()
        try:
            dp_list.append((nlp_master.dependency_relation(data), file[1]))
        except:
            print(f'Error: Cannot dependency parsing on query{file[1]}')
            return

        # Write results to a file
        with codecs.open('output/output_b.txt', 'w', encoding='utf-8') as out_f:
            for result in dp_list:
                out_f.write(f'Query {result[1]}:\n')
                for relation in result[0]:
                    token_l = relation.getToken('l').getWord()
                    token_r = relation.getToken('r').getWord()
                    out_f.write(
                        f'{relation.getRelation()} ({token_l}, {token_r})\n')
                out_f.write(
                    '-----------------------------------------------\n')
            out_f.close()
    print('Analysis done! See results of dependency parsing analysis in the file "output_b.txt".')

    print('Grammatical Relation analysis...')
    gr_list = []
    with codecs.open('output/output_c.txt', 'w', encoding='utf-8') as out_f:
        for dp in dp_list:
            out_f.write(f'Query {dp[1]}:\n')

            # Grammatical relation analysis
            try:
                gr, query, pred, lsubj, lobj, source, dest, time = nlp_master.grammatical_relation(
                    dp[0])
            except:
                print(
                    f'Error: Cannot grammatical relation analysis on query {dp[1]}')
                return
            gr_list.append((gr, dp[1]))
            printer = GRPrinter(gr)

            # Write results to a file
            out_f.write(printer.print_query()) if query else None
            out_f.write(printer.print_pred()) if pred else None
            out_f.write(printer.print_lsubj()) if lsubj else None
            out_f.write(printer.print_lobj()) if lobj else None
            out_f.write(printer.print_source()) if source else None
            out_f.write(printer.print_dest()) if dest else None
            out_f.write(printer.print_time()) if time else None
            out_f.write('-----------------------------------------------\n')
        out_f.close()

    print('Analysis done! See results of grammatical relation analysis in the file "output_c.txt".')

    lf_list = []

    print('Transfering into Logical Form...')
    with codecs.open('output/output_d.txt', 'w', encoding='utf-8') as out_f:
        for gr in gr_list:
            out_f.write(f'Query {gr[1]}:\n')

            # Translate into Logical Form
            try:
                lf = nlp_master.logical_form(gr[0])
            except:
                print(
                    f'Error: Cannot transfer grammatical relation to logical form on query {gr[1]}')
                return
            lf_list.append((lf, gr[1]))
            printer = LFPrinter(lf)

            # Write results to a file
            out_f.write(printer.print())
            out_f.write('\n-----------------------------------------------\n')
        out_f.close()
    print('Transfering done! See results of grammatical relation analysis in the file "output_d.txt".')

    ps_list = []

    print('Transfering into Procedure Semantics...')
    with codecs.open('output/output_e.txt', 'w', encoding='utf-8') as out_f:
        for lf in lf_list:
            out_f.write(f'Query {lf[1]}:\n')

           # Translate into procedure semantic
            try:
                ps = nlp_master.procedure_semantic(lf[0])
            except:
                print(
                    f'Error: Cannot transfer logical form to procedure semantics on query {lf[1]}')
                return
            ps_list.append((ps, lf[1]))
            for p in ps:
                printer = PSPrinter(p)

                # Write results to a file
                out_f.write(printer.print() + '\n')
            out_f.write('-----------------------------------------------\n')
        out_f.close()
    print('Transfering done! See results of grammatical relation analysis in the file "output_e.txt".')

    database = Database('input/database/data.txt').getData()

    print('Writing answers...')
    with codecs.open('output/output_f.txt', 'w', encoding='utf-8') as out_f:
        for ps in ps_list:
            out_f.write(f'Query {ps[1]}:\n')

            # Retrieve answers
            try:
                result_list = [nlp_master.retrieve_result(
                    database, p) for p in ps[0]]
            except:
                print(f'Error: Cannot retrieve answers on query {ps[1]}')
                return

            for result in result_list:
                out_f.write(write_answer(result) + '\n')
            out_f.write('-----------------------------------------------\n')
        out_f.close()
    print('See results of every query in the file "output_f.txt".')


if __name__ == '__main__':
    main()
