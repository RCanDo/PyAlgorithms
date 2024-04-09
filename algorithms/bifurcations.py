#! python3
# -*- coding: utf-8 -*-
"""
---
# This is YAML, see: https://yaml.org/spec/1.2/spec.html#Preview
# !!! YAML message always begin with ---

title: bifurcation demo
subtitle:
version: 1.0
type: tutorial
keywords: [bifurcation, ...]
description: |
remarks:
todo:
sources:
file:
    usage:
        interactive: True   # if the file is intended to be run interactively e.g. in Spyder
        terminal: False     # if the file is intended to be run in a terminal
    date: 2024-01-04
    authors:
        - nick: rcando
          fullname: Arkadiusz Kasprzyk
          email:
              - rcando@int.pl
"""

# %%
import numpy as np
import matplotlib.pyplot as plt

from typing import Callable
from itertools import islice

# %%
def logistic(x, r=.65, p=1) -> float:
    """
    x: float in (0, 1)
    r: float in (0, 1)
    p: float > 0
    -on-> (0, 1)
    """
    y = r * (4 * x * (1 - x)) ** p
    return y

# logistic(.5, 1)     # 1


def sin2(x, r=.65, p=1):
    """
    x: in (0, 1)
    r: in (0, 1)
    p: > 0
    -on-> (0, 1)
    """
    y = r * np.sin(x * np.pi) ** p
    return y


# %%
def iterate(f, x0=.5, **params):
    x = x0
    while True:
        x = f(x, **params)
        yield x


[k for k in islice(iterate(logistic), 9)]


# %%
def seq(n, f, x0=.5, **params):
    s = [y for y in islice(iterate(f, x0, **params), n)]
    return s


# %%
seq(99, logistic)
seq(99, logistic, r=.2)
np.unique(seq(999, logistic, r=.2), return_counts=True)

# %%
plt.plot(seq(99, logistic, r=.2))
plt.plot(seq(222, logistic, r=.4))
plt.plot(seq(222, logistic, r=.5))
plt.plot(seq(222, logistic, r=.7))
plt.plot(seq(222, logistic, r=.8))
plt.plot(seq(222, logistic, r=.9))

# %%
N = 200
data = [(r, seq(N, sin2, r=r, x0=.3)) for r in np.linspace(.99 / 4, 3.99 / 4, 1000)]
counts = [(r, *np.unique(s, return_counts=True)) for r, s in data]

fig, ax = plt.subplots()
for tup in counts:
    xx = [tup[0]] * len(tup[1])
    yy = tup[1]
    alpha = np.sqrt(tup[2] / N)
    ax.scatter(xx, yy, alpha=alpha, color='k', s=.3)

# %%
N = 256 * 2
data = [(r, seq(N, sin2, r=r)) for r in np.linspace(.99 / 4, 3.99 / 4, 1000)]

fig, ax = plt.subplots()
for r, yy in data:
    yy = yy[::8]
    xx = [r] * int(N / 8)
    ax.scatter(xx, yy, alpha=10/N, color='k', s=.3)

# %%
