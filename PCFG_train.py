from TreeClass import Tree
from RandSentenceClass_revised import RandSentence_revised
from RandSentenceClass import RandSentence
from collections import defaultdict


counts = defaultdict(int)
base = defaultdict(int)
RandSentence = RandSentence()
RandSentence_revised = RandSentence_revised()

with open('corpus.txt', 'r') as f1:
    with open('corpus_processed.txt', 'w') as f2:
        next(f1)
        flag = 0
        for line in f1:
            line = line.strip()
            words = line.split(" ")
            if words[0] == '(S':
                if flag:
                    f2.write("\n" + "(S ")
                else:
                    f2.write("(S ")
                    flag = 1
            else:
                f2.write(' '.join(words) + " ")

with open('corpus_processed.txt', 'r') as f2:
    with open('PCFG_train_results.txt', 'w') as f3:
        for line in f2:
            line = line.strip()
            line = Tree.parse(line)
            rules = line.getProductions()
            for (lhs, rhs) in rules:
                counts[(lhs, rhs)] += 1
                base[lhs] += 1
        for (lhs, rhs), count in counts.items():
            prob = count / base[lhs]
            RandSentence_revised.add_prod(lhs, rhs)
            RandSentence.add_prod(lhs, rhs)
            str = "%s -> %s # %.4f" % (lhs, rhs, prob)
            f3.write(str + '\n')

with open('PCFG_generate_results.txt', 'w') as f4:
    for i in range(10):
        f4.write(RandSentence.gen_random('S') + '\n')

with open('PCFG_generate_results_revised.txt', 'w') as f5:
    for i in range(10):
        f5.write('[S ' + RandSentence_revised.gen_random('S') + '\n')

