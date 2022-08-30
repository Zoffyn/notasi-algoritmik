import argparse
from os.path import exists

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)

args = parser.parse_args()

path = args.file

tokens = []

keywords = [
    'integer', 'real', 'boolean', 'character',
    'true', 'false', 'and', 'or', 'xor', 'not',
    'div', 'mod', 'abs',
    'type', 'procedure', 'function', 'constant',
    'input', 'output', 'input/output',
    'depend on', 'if', 'then', 'else',
    'repeat', 'times', 'while', 'do', 'until', 'iterate', 'stop', 'traversal',
]

special_keywords = [
    'procedure', 'function', 'constant'
]

headers = [
    'Program', 'KAMUS', 'ALGORITMA'
]

operators = "+-*/%:<=>(),[]"

def get_state(c: str):
    if c.isspace():
        return 'space'
    elif c.isalnum():
        return 'text'
    elif c in operators:
        return 'operator'
    elif c == '{':
        return 'comment'


if exists(path):
    with open(path, 'r') as file:
        state = ''
        for line in file:
            if state != 'comment':
                state = get_state(line[0])
                token = ''
            for i in range(len(line)):
                token += line[i]
                if i == len(line) - 1:
                    if state != 'comment':
                        tokens.append(token)
                else:
                    if line[i+1].isspace() and state != 'space' and state != 'comment':
                        tokens.append(token)
                        token = ''
                        state = 'space'
                    if line[i+1].isalnum() and state != 'text' and state != 'comment':
                        tokens.append(token)
                        token = ''
                        state = 'text'
                    if line[i+1] in operators and state != 'operator' and state != 'comment':
                        tokens.append(token)
                        token = ''
                        state = 'operator'
                    if line[i+1] == '{':
                        state = 'comment'
                        tokens.append(token)
                        token = ''
                    if line[i] == '}':
                        tokens.append(token)
                        token = ''
                        state = get_state(line[i+1])

html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Output</title>
    <style>
        * {
            margin: 0;
            padding: 0;
        }
        body {
            padding: 20px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <pre style='font-size: 1em; line-height: 1.15;'>"""

types = []
procs = []

for i in range(len(tokens)):
    token = tokens[i]
    if token in keywords:
        if token in special_keywords:
            html += f"<u style='color: blue;'><b>{token}</b></u>"
        else:
            html += f"<u style='color: blue;'>{token}</u>"
    elif token == '<-':
        html += '&larr;'
    elif token == '->':
        html += '&rarr;'
    elif token == '<=':
        html += '&le;'
    elif token == '>=':
        html += '&ge;'
    elif token[0] == '{':
        html += f"<span style='color: green;'>{token}</span>"\
                .replace('<-', '&larr;')\
                .replace('->', '&rarr;')\
                .replace('>=', '&ge;')\
                .replace('<=', '&le;')
    elif token in headers:
        html += f"<b>{token}</b>"
    elif token in types:
        html += f"<span style='color: #27819d;'>{token}</span>"
    elif token in procs:
        html += f"<span style='color: #7e6128;'>{token}</span>"
    elif i > 1 and tokens[i - 2] in ['Program', 'type']:
        html += f"<span style='color: #27819d;'>{token}</span>"
        types.append(token)
    elif i > 1 and tokens[i - 2] in ['function', 'procedure']:
        html += f"<span style='color: #7e6128;'>{token}</span>"
        procs.append(token)
    else:
        html += token

html += '</pre>\n</body>\n</html>'

with open('output.html', 'w') as output:
    output.write(html)
