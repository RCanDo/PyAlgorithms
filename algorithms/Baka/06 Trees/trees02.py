#! python3
# -*- coding: utf-8 -*-
"""
---
# This is YAML, see: https://yaml.org/spec/1.2/spec.html#Preview
# !!! YAML message always begin with ---

title: Trees
subtitle: General Tree
version: 1.0
type: algorithms
keywords: [tree]
description: Implemantation of a general tree.
remarks:
todo:
    - Write it anew applying logic similar to BST (trees01.py).
    - Try to make it superclass for BST (check first if it is sensible -- BST logic is quite specific)
    - What about Red Black Trees and other balanced trees?
    - What about expression trees?
sources:
    - title: Python Data Structures And Algorithms
      chapter: 06 Trees
      pages: 131-
      link: "D:/bib/Python/pythondatastructuresandalgorithms.pdf"
      date: 2017-05
      authors:
          - fullname: Benjamin Baka
      usage: inspiration
file:
    usage:
        interactive: True   # if the file is intended to be run interactively e.g. in Spyder
        terminal: False     # if the file is intended to be run in a terminal
    label: "trees02.py"
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
# import numpy as np

#%%

def fun(x):
    if x < 0:
        raise Exception("qq!")
        return False
    else:
        return True

def fun(x):
    if x < 0:
        try:
            raise Exception("qq!")
        except Exception as e:
            print(e)
        finally:
            return False
    else:
        return True

#%%

class ChildNotFound(Exception):
    def __init__(self, msg: str):
        super().__init__("There is no children to this node: {}".format(msg))

class Node():
    """Node of a tree
    """
    def __init__(self, value, label=None):
        self.value = value
        self.label = label if label is not None else str(value)
        self.parent = None
        self.children = []
        self.level = 0

    def parent(self):
        return self.parent

    def children(self):
        return self.children

    def add(self, node, parent_label=None):

        if parent_label is None:
            parent_label = self.label

        if parent_label == self.label:
            node.level = self.level + 1
            node.parent = self
            if node.label in list(map(lambda l: l.label, self.children)):
                return False
            else:
                self.children.append(node)
                return True

        elif len(self.children) == 0:
            try:
                raise ChildNotFound(self.label)
            except ChildNotFound as e:
                print(e)
            finally:
                return False
        else:
            found = False
            for ch in self.children:
                found = ch.add(node, parent_label)
                if found:
                    break
            return found

    def remove(self, node:str):
        found = False
        for ch in self.children:
            found = ch.label == node
            if found:
                self.children.remove(ch)
            else:
                found = ch.remove(node)
            if found:
                break
        return found

    def print(self):
        print("  "*self.level + self.label + " : " + str(self.value))
        for ch in self.children:
            ch.print()

    def get(self, node:str):
        if self.label == node:
            return self
        else:
            found = None
            for ch in self.children:
                if ch.label == node:
                    found = ch
                    break
                else:
                    found = ch.get(node)
            return found

    def __str__(self):
        string = "{}{} : {}\n".format(" "*2*self.level, self.label, str(self.value))
        for ch in self.children:
            string += ch.__str__()
        return string

    def __repr__(self):
        string = "Node({}, '{}')".format(self.value, self.label)
        return string

    @property
    def is_root(self):
        is_root = self.parent is None
        return is_root

    @property
    def is_leaf(self):
        is_leaf = len(self.children) == 0
        return is_leaf


#%% manual tests

n1 = Node(1)
n1
print(n1)

n1.is_root
n1.is_leaf

n1_ = n1.get(1)
print(n1_)
n1_ = n1.get('1')
print(n1_)

n1.add(Node(2))
n1
print(n1)

n1.is_leaf
n1.get('2').is_root

n1.add(Node(3))
print(n1)

n2_ = n1.get('2')
print(n2_)

n1.add(Node(4, '2'))   #  bad!!!
print(n1)

# BUT
n1.add(Node(4, '2'), '2')
print(n1)

## i.e. labels must be unique within the direct children of the given node

n1.add(Node(5), '3')
print(n1)

n1.add(Node('a'), '5')
print(n1)

n1.children
n3 = n1.children[1]
n3
n3.print()

n1_ = n3.parent
n1_.print()

n1.add(Node('b', '4'))
n1.print()

n1.remove('4')
n1.print()

n1.remove('a')
n1.print()

n1.remove('z')
n1.print()


#%%
class Tree(Node):
    """General Tree
    """
    def __init__(self, value=0, label=None):
        label = label if label is not None else str(value)
        self.root = Node(value, label)

    def __repr__(self):
        string = "Tree({}, '{}')".format(self.value, self.label)
        return string







