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

for token in tokens:
    if token in keywords:
        if token in special_keywords:
            html += f"<u><b>{token}</b></u>"
        else:
            html += f"<u>{token}</u>"
    else:
        if token == '<-':
            token = '&larr;'
        if token == '->':
            token = '&rarr;'
        if token == '<=':
            token = '&le;'
        if token == '>=':
            token = '&ge;'
        html += token

html += '</pre>\n</body>\n</html>'

with open('output.html', 'w') as output:
    output.write(html)
