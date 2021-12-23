from models.utils import loading_parser, read_file
import codecs


def main():
    # Loading parser
    print('Loading grammar...')
    nlp_parser = loading_parser('models/grammar.fcfg')
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


if __name__ == '__main__':
    main()
