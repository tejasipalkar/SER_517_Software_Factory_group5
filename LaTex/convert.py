import json
import os

TAB = '\t'
BEGIN = r'\begin{itemize}'
Event = r'\event {0}\\hfill{{}}{1}'
END = r'\end{itemize}'

def main(path):
    with open(os.path.join(path, 'my_json_data.json')) as data_file:
        data = json.load(data_file)
    print('\n'.join(convert(data)))

def convert(data):
    stack = [data['event'].__iter__()]
    yield (TAB * (len(stack) - 1)) + BEGIN
    while len(stack) > 0:
        iterator = stack[len(stack) - 1]
       