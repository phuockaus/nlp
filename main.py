from models.database import Database
from models.grammar import Parser
import codecs


def main():
    # Loading parser
    print('Loading grammar...')
    nlp_parser = Parser('models/grammar.fcfg')
    print('Loading done!')

    # Read input files
    print('Reading file...')
    input_file_list = [
        (f'input/queries/{index}.txt', index) for index in range(1, 7)]
    print('Reading done!')

    # Dependency parsing analysis
    print('Dependency parsing analysis...')
    result_list = []
    for file in input_file_list:
        with codecs.open(file[0], encoding='utf-8') as f:
            data = f.read()
            f.close()
        result_list.append((nlp_parser.dependency_relation(data), file[1]))

    # Write results to a file
    with codecs.open('output/output_b.txt', 'w', encoding='utf-8') as out_f:
        for result in result_list:
            out_f.write(f'Query {result[1]}:\n')
            for relation in result[0]:
                out_f.write(relation + '\n')
            out_f.write('-----------------------------------------------\n')
        out_f.close()
    print('Analysis done! See results of dependency parsing analysis in the file "output_b.txt".')


if __name__ == '__main__':
    main()
