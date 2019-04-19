from collections import defaultdict
import random


class RandSentence_revised(object):
    def __init__(self):
        self.prod = defaultdict(list)

    def add_prod(self, lhs, rhs):
        prods = rhs.split('|')
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))

    def gen_random(self, symbol):
        sentence = ''
        rand_prod = random.choice(self.prod[symbol])
        for sym in rand_prod:
            if sym in self.prod:
                sentence += ('[' + sym + ' ')
                sentence += self.gen_random(sym)
            else:
                sentence += sym + ' '
        return sentence
