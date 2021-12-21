from nltk import parse
from models.database import Database
from models.grammar import Parser
import codecs


def main():
    # Loading parser
    nlp_parser = Parser('models/grammar.fcfg')

    # Read input files
    input_file_list = [
        (f'input/queries/{index}.txt', index) for index in range(1, 7)]

    # Dependency parsing analysis
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


if __name__ == '__main__':
    main()