#!/usr/bin/env python


class Tree(object):
    def __init__(self, label, span, wrd=None, subs=None):
        assert (wrd is None) ^ (subs is None), "bad tree %s %s %s" % (label, wrd, subs)
        self.label = label
        self.span = span
        self.word = wrd
        self.subs = subs
        self._str = None
        self._hash = None

    @staticmethod
    def _parse(line, pos=0, wrdidx=0):
        empty = False
        # 找到tree的标签
        space = line.find(" ", pos)         # 标签后的第一个空字符
        label = line[pos + 1 : space]       # 提取标签
        newpos = space + 1                  # 找到标签后第一个字符的位置
        newidx = wrdidx
        if line[newpos] == '(':
            # 非终结符
            subtrees = []            
            while line[newpos] != ')':
                if line[newpos] == " ":
                    newpos += 1
                # 循环_parse同一棵树，起始位置改变
                (newpos, newidx), emp, sub = Tree._parse(line, newpos, newidx)
                if not emp:
                    subtrees.append(sub)
            return (newpos + 1, newidx), subtrees==[], Tree(label, (wrdidx, newidx), subs=subtrees)
        else:
            # 终结符
            finalpos = line.find(")", newpos)
            word = line[newpos : finalpos]      # 找到终结符的单词
            # 返回((终结括号后一位置，终结符数量)，是否为空，(树))
            return (finalpos + 1, wrdidx + 1 if not empty else wrdidx), empty, Tree(label, (wrdidx, wrdidx+1), wrd=word)

    @staticmethod
    def parse(line):
        _, is_empty, tree = Tree._parse(line, 0, 0)
        # 判断开头字符是否S
        if tree.label != "S":
            # create another node
            tree = Tree(label="S", span=tree.span, subs=[tree])
        return tree            

    def getProductions(self):
        prods = []
        # 有子树的情况
        if self.subs is not None:
            # 有2棵子树的情况（非终结符）
            if len(self.subs) == 2:
                child1 = self.subs[0]
                child2 = self.subs[1]
                prod = (self.label, "%s %s" % (child1.label,child2.label))
                prods.append(prod)
            # 有1棵子树的情况（终结符）
            elif len(self.subs) == 1:
                prod = (self.label, self.subs[0].label)
                prods.append( prod )
            # 对每棵子树执行相同操作
            for child in self.subs:
                childProds = child.getProductions()
                prods.extend(childProds)        # 添加返回的序列内容（添加对象则为.append())
        # 无子树的情况
        elif self.word is not None:
            prod = (self.label, self.word)
            prods.append(prod)
        return prods
                

