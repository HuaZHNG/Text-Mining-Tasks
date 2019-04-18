from collections import defaultdict
import random


class RandSentence(object):
    def __init__(self):
        self.prod = defaultdict(list)

    def add_prod(self, lhs, rhs):
        prods = rhs.split('|')
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))

    def gen_random(self, symbol):
        sentence = ''
        # 选择标签中的一个结果
        rand_prod = random.choice(self.prod[symbol])
        for sym in rand_prod:
            # 非终结符继续迭代
            if sym in self.prod:
                sentence += self.gen_random(sym)
            else:
                sentence += sym + ' '
        return sentence
