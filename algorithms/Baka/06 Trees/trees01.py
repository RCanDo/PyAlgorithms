#! python3
# -*- coding: utf-8 -*-
"""
---
# This is YAML, see: https://yaml.org/spec/1.2/spec.html#Preview
# !!! YAML message always begin with ---

title: Trees
subtitle: BST -- binary search tree.
version: 1.0
type: algorithms
keywords: [tree, BST]
description: |
    Implemantation of a BST.
    It is simpler then general tree which is implemented in the next file.
remarks:
todo:
sources:
    - title: Python Data Structures And Algorithms
      chapter: 06 Trees
      pages: 131-
      link: "E:/bib/Python/pythondatastructuresandalgorithms.pdf"
      date: 2017-05
      authors:
          - fullname: Benjamin Baka
      usage: inspiration
file:
    usage:
        interactive: True   # if the file is intended to be run interactively e.g. in Spyder
        terminal: False     # if the file is intended to be run in a terminal
    label: "trees01.py"
    path: "D:/ROBOCZY/Python/algorithms/Baka/"
    date: 2019-10-17
    authors:
        - nick: kasprark
          fulllname: Arkadiusz Kasprzyk
          email:
              - arkadiusz.kasprzyk@tieto.com
              - akasp666@google.com
              - arek@staart.pl
"""

#%%
import typing as typ
from typing import List, Tuple, Dict, Set, Optional, Union, NewType

# BSTNode = NewType('BSTNode')  # NO!, see help(NewType)

#%%

class BSTNode(object):
    """
    BST (Binary Search Tree) Node.
    It has only 'left' and 'right' children where 'left's value is never greater then
    node's value while 'right's value is always greater then node's value:
        self.left.value <= self.value
        self.right.value > self.value
    This is the basic property of BST.

    Attributes:
        value: int
            Value of the node.
        parent: BSTNode
            Indicates the parent of the node.       (by ref or by value???)
            `None` only for root of the tree.
        left: BSTNode
            Left child of the node, which value is never greater then value of the node.
            May be None.
        right: BSTNode
            Right child of the node, which value is always greater then value of the node.
            May be None.

    Properties:
        is_leaf: bool
        is_left_child: bool
        degree: int
            Number of children (0, 1, 2).
        children: List[BSTNode]

    Methods:
        max(): int
        min(): int
        to_dict(): dict
    """

    def __init__(self, value: Union[int, float, str], parent=None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    @property
    def is_left_child(self) -> bool:
        if self.parent is None:
            return None
        else:
            return self.value <= self.parent.value

    @property
    def degree(self) -> int:
        return sum((self.left is not None, self.right is not None))

    @property
    def children(self) -> Tuple:
        return [self.left, self.right]

    def __str__(self) -> str:
        left, right = self.left.__str__(), self.right.__str__()
        left, right = tuple(map(lambda s: "" if s == "None" else s, [left, right]))
        if left == right == "":
            string = "{}".format(self.value)
        else:
            string = "{}:({}, {})".format(self.value, left, right)
        return string

    def __repr__(self) -> str:
        left, right = self.left.__repr__(), self.right.__repr__()
        if left == right == "None":
            ss = "None"
        elif left == "None":
            ss = "{{None:None, {}}}".format(right)
        elif right == "None":
            ss = "{{{}, None:None}}".format(left)
        else:
            ss = "{{{}, {}}}".format(left, right)
        string = "{}:{}".format(self.value, ss)
        return string

    def to_dict(self) -> Dict:
        """
        Returns a whole subtree stemming from this node in the form of dictionary.
        """
        def keyvalue(node):
            if node is None:
                return None, None
            elif node.is_leaf:
                return node.value, None
            else:
                return node.value, node.to_dict()

        return dict(map(keyvalue, [self.left, self.right]))


    def max(self):
        """
        Returns ascendent node having maximum value in the whole subtree.
        It is used to search recursively for the max of the whole BST.
        Notice that it return whole node not only its value, so to get the value
        use `node.max().value`.
        """
        if self.right is None:
            return self
        else:
            return self.right.max()

    def min(self):
        """
        Returns ascendent node having minimum value in the whole subtree.
        It is used to search recursively for the min of the whole BST.
        Notice that it return whole node not only its value, so to get the value
        use `node.min().value`.
        """
        if self.left is None:
            return self
        else:
            return self.left.min()



class BST(object):
    """
    Binary Search Tree.

    Arguments:
        seq: Sequence of values to be added to tree in the form of list or dictionary.
            In case of list of values the tree will build itself according to BST rules
            (see BSTnode description) thus the consistency with BST definition is guaranteed.
            In case of dictionary the whole structure of the tree is recreated from it
            hence the consistency with BST rules is not guranteed if the data are wrong.
            However the method ._check()may be applied to check this consistency.
            The format of dictionary with the BST encoded is as follows
            {root.value:{v0:{v2:{...}, v3:{...}}, v1:{...} }}
            where if node terminates (is a leaf) then we have
            n:None
            and if one children is None (e.g. left) the we have
            nx:{None:None, ny:{...}} or nx:{None:None, ny:None}.
            Notice that n:{None:None, None:None} is impossible as it means n is a leaf
            what is encoded simply with n:None.

    Examples:
        t = BST([3, 6, 4, 9, 1, 0, 5, 7, 8, 2])
        t = BST({3:{1:{0:None, 2:None}, 6:{4:{None:None, 5:None}, 9:{7:{None:None, 8:None}, None:None}}}})

    Attributes:
        root: BSTNode

    Properties:

    Methods:
        insert(int):
        to_dict():


    """
    def __init__(self, seq: Union[List, Dict] = None):
        self.root = None
        if seq is None:
            pass
        elif isinstance(seq, list):
            self.from_list(seq)
        elif isinstance(seq, dict):
            self.from_dict(seq)
        else:
            raise ValueError("`seq` must be list or dictionary or None.")

    def __str__(self) -> str:
        return self.root.__str__()

    def __repr__(self) -> str:
        return "BST({" + self.root.__repr__() + "})"

    def __insert(self, value: Union[int, float, str], parent: BSTNode):
        if value <= parent.value:
            if parent.left is None:
                parent.left = BSTNode(value, parent)
            else:
                self.__insert(value, parent.left)
        else:
            if parent.right is None:
                parent.right = BSTNode(value, parent)
            else:
                self.__insert(value, parent.right)

    def insert(self, value: Union[int, float, str]):
        if self.root is None:
            self.root = BSTNode(value)
        else:
            self.__insert(value, self.root)

    def __find(self, value: int, node: BSTNode) -> BSTNode:
        if node is None:
            return None
        elif value < node.value:
            return self.__find(value, node.left)
        elif value > node.value:
            return self.__find(value, node.right)
        else:  # value == node.value:
            return node

    def find(self, value: int) -> BSTNode:
        return self.__find(value, self.root)

    def min(self) -> BSTNode:
        if self.root is None:
            return None
        else:
            return self.root.min()

    def max(self) -> BSTNode:
        if self.root is None:
            return None
        else:
            return self.root.max()

    def remove(self, value: Union[int, float, str]) -> bool:
        """
        Removing node with a given value from a tree.
        We use the following version:
            - if node is a leaf then it's just deleted;
            - if node has no left child then it's simply replaced with its right child;
            - if node has no right child then it's replaced with its left child;
            - if node has both children (left and right) then its value is replaced
              with the maximum of its left subtree i.e. value of the right-most node
              of the left subtree stemming from it;
              this right-most node is then replaced by its left child if it exists -
              it cannot have the right child as it is 'right-most node'! - if not then is
              simply deleted.
        Notice that the last procedure could be replaced by the dual procedure in which
        'left' and 'right' are swapped and 'maximum' is changed for 'minimum'.
        Remember too that 'nodes' carry with them their children!
        """
        node = self.find(value)
        if node is None:
            return False
        else:
            if node.is_leaf:
                if node.is_left_child:
                    node.parent.left = None
                else:
                    node.parent.right = None
            elif node.left is None:
                node.right.parent = node.parent
                if node.is_left_child:
                    node.parent.left = node.right
                else:
                    node.parent.right = node.right
            elif node.right is None:
                node.left.parent = node.parent
                if node.is_left_child:
                    node.parent.left = node.left
                else:
                    node.parent.right = node.left
            else:
                node_left_max = node.left.max()
                node.value = node_left_max.value
                node_left_max.parent.right = node_left_max.left
                  # as node_left_max is a right-most node of the left subtree stemming from the node
            return True

    def __check(self, node: BSTNode) -> bool:
        """
        For checking if the tree is still BST i.e.
        all nodes on the left have smaller values then those on the right.
        For self-testing.
        """
        if node is None:
            res = True
        else:
            res = (node.left is None or node.left.value <= node.value) and \
                  (node.right is None or node.value < node.right.value) and \
                  self.__check(node.left) and self.__check(node.right)
        return res

    def _check(self) -> bool:
        return self.__check(self.root)

    def from_list(self, lst: List[int]) -> bool:
        """This is tree creation -- will always be proper BST
        """
        for l in lst:
            self.insert(l)
        return True

    def __from_dict(self, dic: Dict, node: BSTNode):
        """This is tree REcreation -- may not be BST if data are wrong.
        However we take only first two entries of each sub-dictionary.
        """
        left, right = tuple(dic.keys())[:2]

        if left is not None:
            node.left = BSTNode(left)
            if isinstance(dic[left], dict):
                self.__from_dict(dic[left], node.left)

        if right is not None:
            node.right = BSTNode(right)
            if isinstance(dic[right], dict):
                self.__from_dict(dic[right], node.right)

    def from_dict(self, dic: Dict) -> bool:
        root = tuple(dic.keys())[0]
        if root is not None:
            self.root = BSTNode(root)
            self.__from_dict(dic[root], self.root)
        return True


    def traverse_breadth(self, with_level: bool = True) -> Union[List[int], Dict[int, List[int]]]:
        """equiv. to FIFO service of nodes
        this is why we import deque
        """
        from collections import deque
        if not with_level:
            values = []
            nodes = deque([self.root])
            while len(nodes) > 0:
                node = nodes.popleft()
                values.append(node.value)
                if node.left:
                    nodes.append(node.left)
                if node.right:
                    nodes.append(node.right)
            return values
        else:
            values = dict()
            nodes = deque([(0, self.root)])
            while len(nodes) > 0:
                level, node = nodes.popleft()
                if not values.get(level, False):
                    values[level] = []
                values[level].append(node.value)
                if node.left:
                    nodes.append((level+1, node.left))
                if node.right:
                    nodes.append((level+1, node.right))
            return values

    def to_dict(self) -> Dict:
        dic = dict()
        if self.root is not None:
            dic[self.root.value] = self.root.to_dict()
        return dic

    def traverse_depth(self, printit: bool = True, indent: str ='--') -> Optional[Dict[str, List[int]]]:
        """equiv to LIFO service of nodes
        we may use ordinanry list
        """

        if self.root is None:
            td = None
        else:
            values = [self.root.value]
            new_lines = [True]
            indents = [0]

            def innertd(node):
                ind = indents[-1] + 1
                for i, nod in enumerate(node.children):
                    if nod is not None:
                        values.append(nod.value)
                        new_lines.append(i>0)     # for BST it's important which is left or right
                        indents.append(ind)
                        innertd(nod)

            innertd(self.root)

            span = len(str(self.max().value))  #! assumes non-negatives only!

            if print:
                for k in range(len(values)):
                    v, nl, i = values[k], new_lines[k], indents[k]
                    if nl:
                        print()
                        if i > 0:
                            tab = (" " * (span + len(indent))) * (i-1) + (" " * span + indent)
                        else:
                            tab = ""
                        #print("'{}'!".format(tab))
                    else:
                        tab = indent
                        #print("'{}'?".format(tab))
                    print(tab + str(v).rjust(span), end="")
                print()

            # class erzatz
            td = {'values':values,       # {0, 1}
                  'new_line':new_lines,   # {}
                  'indent':indents}
        return td



#%%
t = BST([3, 6, 4, 9, 1, 0, 5, 7, 8, 2])
t.traverse_depth()

t
print(t)

t.root.left.left.children
t.root.degree


ll = t.traverse_depth()
ll

#%%
t = BST([3, 6, 4, 9, 1, 0, 5, 7, 8, 2])
t
print(t)
t.to_dict()
_ = t.traverse_depth()
t.traverse_breadth(True)

t = BST({3:{1:{0:None, 2:None}, 6:{4:{None:None, 5:None}, 9:{7:{None:None, 8:None}, None:None}}}})
t


#%%
t = BST([3, 6, 4, 9, 1, 0, 5, 7, 8, 2])
t
print(t)
t._check()
t.remove(6)
print(t)

dd = t.traverse_breadth(True)
dd

ll = t.traverse_breadth()
ll

t1 = BST(ll)
ll1 = t1.traverse_breadth()
ll1
ll == ll1  # True

#%%
import numpy as np
ll = np.random.randint(0, 100, 50)
ll
t = BST(list(ll))
t
print(t)
t.td()

%timeit ll.min()
%timeit t.min()
%timeit t.min().value

%timeit ll.max()
%timeit t.max()
%timeit t.max().value

#%%
ll = np.random.randint(0, int(1e9), int(1e5))

t = BST(list(ll))

%timeit ll.min()
%timeit t.min()
%timeit t.min().value

%timeit ll.max()
%timeit t.max()
%timeit t.max().value




#%%

t = BST()
t
print(t)
t.root

t.insert(4)
print(t)

t.insert(2)
print(t)

t.insert(7)
print(t)

t.insert(5)
print(t)
t.insert(6)
print(t)

t.insert(3)
t.insert(1)
print(t)

t.root
t

#%%
t.min().value
t.max().value


n4 = t.find(4)
print(n4)
n4.min().value
n4.max().value


n5 = t.find(5)
print(n5)
n5.min().value
n5.max().value
n5.is_left_child

print(t)
t.remove(7)
t._check()
t.remove(5)
t.remove(6)

t.remove(4)


#%% Experiment
"""
distribution of the tree depth wrt its size (as nr of elements 0, 1, ..., N -- all unique):
"""
from numpy import random
NN = 100
trials = 1000

def experiment(N, trials):
    results = []
    for k in range(trials):
        data = list(random.choice(N, N, replace=False))
        bst = BST(data)
        dd = bst.traverse_breadth(with_level=True)
        results.append(len(dd))
    return results

results = dict()

for N in range(20, NN):
    results[str(N).rjust(2, "0")] = experiment(N, trials)

#%%
import pandas as pd
import pandas_profiling

respd = pd.DataFrame(results)
respd

profile = respd.profile_report()
profile.to_file("experiment01.html")


#%%
