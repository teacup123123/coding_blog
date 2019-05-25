---
layout: post
title: "Google Code Jam 2019 Round 2 Q1: New Elements"
author: Tikai Chang
tags: ["GCJ", "competition", "python"]
---

The original question statement is [here](https://codingcompetitions.withgoogle.com/codejam/round/0000000000051679/0000000000146183)

### Restating the problem
You are a chemist in the Code Jam universe. There are 2 elements, Codium and Jamarium of unknwon (*integer, >0*) mass. As a chemist you have managed to synthesize different compounds with different numbers of C and J.

Given a list of compositions (number of C and J of all synthesized compounds), determine the number of **strictly increasing** weight order scenarios over all possible integer weights of C and J. By strictly increasing, we mean that any ordering containing ties between any two molecules are discarded.

For example, you have synthesized $$\left[C_1J_2,C_2J_1\right]$$.
- In the case that the weight of C > the weight of J, then $$C_1J_2$$ < $$C_2J_1$$
- Otherwise, $$C_2J_1$$ < $$C_1J_2$$

In total there are **two** possible orders, and you should answer: 2.

In the easy case *[resp. hard]*, there are at least N = 2 molecules/compounds, and at most and 6 *[resp. 300]*. In each compound, there are at most 10^9 Codium and Jamarium respectively. 

### Reformulating the problem
```
#Let L be a list of all detected formulas
L = [(c,j)...] #c>0,j>0

# wc, wj are weights of codium and jamarium 
# we sort the list according to the total weight, key is the comparator function
L_sorted(wc,wj) = sorted(L, key = c*wc+j*wj for (c,j) in L)

# Determine the number of possible orders
answer = len({L_sorted(wc,wj) for all wc,wj >0 / such that there are no ties of weights})
```
### Reflection during the contest

I like to visualize things, one way is for each detected tuple, we place a dot on the 2D-graph.
Take an example, $$C_1J_2$$ corresponds to (1,2) on the 2D *compound space*.

In the same manner in the *weight space*, (wc,wj) can also be plotted in 2D.

There are at most N! types of orderings (number of permutations of length N).
 
The pertinent question is, when in the *weight space* does the order change?
This *change* occurs when at least two molecules in the list enters a tie. For example (1,2) and (2,1), corresponding to $$\left[C_1J_2,C_2J_1\right]$$ contains a tie at $$(wc,wj) = (1,1)$$

How did this happen? well $$(1,1)\cdot(1,2) = (1,1)\cdot(2,1)$$ (Denotes [inner product](https://en.wikipedia.org/wiki/Dot_product)). In other words  $$(1,1)\cdot\left((1,2)-(2,1)\right) = 0$$. Note that a tie (e.g. (1,1)) automatically implies that any multiple of this tuple (e.g. (5,5) ) is also a tie-generating weight-tuple.

This gives us an inspiration for an algorithm that could work: count the number of boundaries (straight lines) in the weight space that generates ties. Any point in weight space can be mapped to a fraction in the rational number space $$Q$$: 1/1 = 5/5 = 4/4.

Since the $$Q$$ is [dense](https://en.wikipedia.org/wiki/Dense_set), any two fractional numbers are bound to have another in between, any one number there is another one arbitrarily (infinitesimally) smaller or bigger. Therefore between any two tie-generating weight tuple, we have another weight tuple which un-breaks the tie. Since two (or more) elements that enters the tie changed their relative position with respect to each other at the the unique tie position, there are at least (the number of tie-conditions) + 1 different orders (two separators seperates three books!)

There are at most so many too because between two tie-breaking fractions the order remains the same!

### Live coding during contest (Time Limit Exceeded for hard case)

{% include GCJ_caseT.html %}


```python
import numpy as np
import itertools
from fractions import Fraction
from collections import defaultdict
t = int(input())
for ti in range(1, t + 1):
    N = int(input())
    types = []
    for ni in range(N):
        C, J = tuple(map(int, input().split()))
        types.append((C,J))

    node = set()
    for i,(ci,ji) in enumerate(types):
        for j,(cj,jj) in enumerate(types):
            if ci>cj and ji<jj:
                fr = Fraction(ci-cj,ji-jj)
                if fr<0:
                    node.add(fr)


    solution = len(node)+1
    print('Case #{}: {}'.format(ti, solution))
```
I would have thought that the overall complexity is 300 x 300 even in the hard case, a small piece of cake. After the contest the hard case had a TLE verdict. Apparently, the line `node.add(fr)`, addition into the set was the cause of this :(

Since it is based over a hash set, the size grows from 0 to 90000 dynamically, requiring rehash I guess...

### Correct code after

Line 13-L19, correction:
```python
    node = list()
    for i,(ci,ji) in enumerate(types):
        for j,(cj,jj) in enumerate(types):
            if ci>cj and ji<jj:
                fr = Fraction(ci-cj,ji-jj)
                if fr<0:
                    node.append(fr)
    node = set(node)
```

This solved the TLE problem. We first just generate a list of maximum size 90000, then we convert it into a set in one go. The size of the hashtable will thus be decided and hashing/resizing is done only once.
