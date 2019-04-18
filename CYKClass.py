class PCFGParser:
    def __init__(self, rules='PCFG_train_results.txt'):
        self.grammar = self.read_grammar(rules)

    def read_grammar(self, f):
        grammar = {}
        rules = open(f, 'r')
        for rule in rules:
            tmp = rule.split()
            lhs = tmp[0]
            rhs = ' '.join(tmp[2:-2])
            weight = float(tmp[-1])
            if lhs in grammar:
                grammar[lhs][rhs] = weight
            else:
                grammar[lhs] = {rhs: weight}
        rules.close()
        return grammar

    def producers(self, rhs, prob):
        results = []
        for (lhs, d) in self.grammar.items():
            for current_rhs in d:
                if current_rhs == rhs:
                    r = (lhs, prob + d[current_rhs])
                    results.append(r)
        return results

    def to_tree(self, table, pointer, sentence, j, i, k):
        if pointer[j][i]:
            rhs = []
            #rhs1
            nj1 = pointer[j][i][k][0][0]
            ni1 = pointer[j][i][k][0][1]
            nk1 = pointer[j][i][k][0][2]
            rhs.append(self.to_tree(table, pointer, sentence, nj1, ni1, nk1))
            #rhs2
            nj2 = pointer[j][i][k][1][0]
            ni2 = pointer[j][i][k][1][1]
            nk2 = pointer[j][i][k][1][2]
            rhs.append(self.to_tree(table, pointer, sentence, nj2, ni2, nk2))
        else:
            rhs = [sentence[i-1]]
        tree = [table[j][i][k][0]]
        tree.extend(rhs)
        return tree

    def parse(self, sentence):
        # 创建CYK表格
        length = len(sentence)
        table = [None]*length
        for j in range(length):
            table[j] = [None] * (length+1)
            for i in range(length+1):
                table[j][i] = []
        # 创建指针表格
        pointer = [None]*length
        for j in range(length):
            pointer[j] = [None] * (length+1)
            for i in range(length+1):
                pointer[j][i] = []
        # 填入表格中斜对角线的数据
        for k in range(1, length+1):
            table[k-1][k].extend(self.producers(sentence[k-1], 0))
        # 自下而上填入CYK表格中的数据
        for i in range(1, length+1):
            for j in range(i-2, -1, -1):
                for k in range(j+1, i):
                    # 尝试进行组合
                    for l in range(len(table[j][k])):
                        for m in range(len(table[k][i])):
                            prob = table[j][k][l][1] + table[k][i][m][1]
                            rhs = table[j][k][l][0]+' '+table[k][i][m][0]
                            lhs = self.producers(rhs, prob)
                            if lhs:
                                table[j][i].extend(lhs)
                                pointer[j][i].extend([[[j, k, l], [k, i, m]]]*len(lhs))
        # 生成句法树（选取概率最大者）
        if table[0][length]:
            max_prob = table[0][length][0][1]
            max_idx = 0
            for i in range(1, len(table[0][length])):
                prob = table[0][length][i][1]
                if prob > max_prob:
                    max_prob = prob
                    max_idx = i
            return self.to_tree(table, pointer, sentence, 0, length, max_idx)
        else:
            return None

