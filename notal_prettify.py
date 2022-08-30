import argparse
from os.path import exists

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)

args = parser.parse_args()

path = args.file

tokens = []

keywords = [
    'Program',
    'integer', 'real', 'boolean', 'character',
    'true', 'false', 'and', 'or', 'xor', 'not',
    'div', 'mod', 'abs',
    'type', 'procedure', 'function', 'constant',
    'input', 'output', 'input/output',
    'depend on', 'if', 'then', 'else',
    'repeat', 'times', 'while', 'do', 'until', 'iterate', 'stop', 'traversal',
]

special_keywords = [
    'Program', 'procedure', 'function', 'constant'
]

operators = "+-*/%:<=>(),"

if exists(path):
    with open(path, 'r') as file:
        for line in file:
            if line[0].isspace():
                state = 'space'
            elif line[0].isalnum():
                state = 'text'
            elif line[0] in operators:
                state = 'operator'
            token = ''
            for i in range(len(line)):
                token += line[i]
                if i == len(line) - 1:
                    tokens.append(token)
                else:
                    if line[i+1].isspace() and (state == 'text' or state == 'operator'):
                        tokens.append(token)
                        token = ''
                        state = 'space'
                    if line[i+1].isalnum() and (state == 'space' or state == 'operator'):
                        tokens.append(token)
                        token = ''
                        state = 'text'
                    if line[i+1] in operators and (state == 'space' or state == 'text'):
                        tokens.append(token)
                        token = ''
                        state = 'operator'

print(tokens)

