from .grammar import Parser


def loading_parser(grammar):
    return Parser(grammar)


def read_file(folder):
    return [(f'{folder}{index}.txt', index) for index in range(1, 7)]
