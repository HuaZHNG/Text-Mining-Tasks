from CYKClass import *


parser = PCFGParser()
with open('PCFG_generate_results.txt', 'r') as f1:
    with open('PCFG_CYK_parse_results.txt', 'w') as f2:
        for line in f1:
            result = parser.parse(line.split())
            f2.write(str(result) + '\n')

with open('PCFG_generate_results_revised.txt', 'r') as f3:
    with open('PCFG_CYK_parse_results_revised.txt', 'w') as f4:
        for line in f3:
            line = line.strip()
            words = line.split(' ')
            newline = ''
            for word in words:
                if str(word)[0] != '[':
                    newline += (word + ' ')
            line = newline
            result = parser.parse(line.split())
            f4.write(str(result) + '\n')