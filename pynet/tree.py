from lxml import etree
from StringIO import StringIO
import numpy as np
import json


class tree(object):

    def __init__(self):
        pass

    def get_depth(self, root):
        if len(root) == 0:
            return 0
        return max(self.get_depth(child) + 1 for child in root.getchildren())

    def get_size(self, root):
        if len(root) == 0:
            return 0
        return sum(1 + self.get_size(child) for child in root.getchildren())

    def tree_match(self, t1, t2, matched):
        # Computes the Simple Tree Matching distance between trees and
        # stores the matching(in pairs of form (element1, element2) in "matched" list passed as argument
        if t1 is None or t2 is None:
            return 0
        
        if t1.tag != t2.tag:
            return 0

        flag = 0
        # Recording alignment as nodes are matched
        # Not an elegant way, bad time complexity. Each call of tree_match calls this. Think
        # of some workaround for this.
        for matching in matched:
            if t1 in matching or t2 in matching:
                flag = 1
        if flag == 0:
            # To remove unncecesary script tags matching
            if t1.tag != "script" and t2.tag != "script":
                matched.append([t1, t2])
        child1 = t1.getchildren()
        child2 = t2.getchildren()
        m = len(t1)
        n = len(t2)
        M = np.zeros((m+1, n+1), np.int)
        for i in range(1, m+1):
            for j in range(1, n+1):
                M[i][j] = max(M[i][j-1], M[i-1][j], M[i-1][j-1] +
                              self.tree_match(child1[i-1], child2[j-1], matched))
        return (M[m][n]+1)

    def tree_alignment(self):
        pass

