---
layout: post
title: "Google Code Jam 2019 Round 2 Q1: New Elements"
author: Tikai Chang
tags: ["GCJ", "competition", "python"]
comments: true
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
# sort the list according to the total weight
# "key=" designates the comparator function
L_sorted(wc,wj) = sorted(L
	, key = c*wc+j*wj for (c,j) in L)

# Determine the number of possible orders
answer = len({L_sorted(wc,wj), 
	for all wc,wj > 0, s.t. no ties})
```
### Reflection during the contest

I like to visualize things, one way is for each detected tuple, we place a dot on the 2D-graph.
Take an example, $$C_1J_2$$ corresponds to (1,2) on the 2D *compound space*.

In the same manner in the *weight space*, (wc,wj) can also be plotted in 2D.

There are at most N! types of orderings (number of permutations of length N).
 
The pertinent question is, when in the *weight space* does the order change?
This *change* occurs when at least two molecules in the list enters a tie. For example (1,2) and (2,1), corresponding to $$\left[C_1J_2,C_2J_1\right]$$ contains a tie at $$(wc,wj) = (1,1)$$

How did this happen? well $$(1,1)\cdot(1,2) = (1,1)\cdot(2,1)$$ ($$\cdot$$Denotes [inner product](https://en.wikipedia.org/wiki/Dot_product)). In other words  $$(1,1)\cdot\left((1,2)-(2,1)\right) = 0$$. Note that a tie (e.g. (1,1)) automatically implies that any multiple of this tuple (e.g. (5,5) ) is also a tie-generating weight-tuple.

This gives us an inspiration for an algorithm that could work: count the number of boundaries (straight lines) in the weight-space by iterating over compund space-pairs and computing a tie-generating weight pair such that $$(wc,wj)\cdot(\Delta c,\Delta j) = 0$$ (Here $$\Delta$$ means difference). Any point in weight space can be mapped to a fraction in the rational number space $$Q$$: 1/1 = 5/5 = 4/4.

Since $$Q$$ is [dense](https://en.wikipedia.org/wiki/Dense_set), any two fractional numbers are bound to have another one in between. Any one number has another arbitrarily (infinitesimally) close, smaller or bigger neighbor. Therefore between any *two* neighboring tie-generating weight-tuples (we can consider 0/1 and 1/0 = +Inf as invisible boundary tuples that are always present), we can always find one weight-tuple in between which un-breaks both ties. By the definition of *neighboring* and the *finiteness* of boundaries ( &#60; 2^N ) there cannot be any ties for this weight-tuple in between, and the generated ordering will be legal (strictly increasing). Since two (or more) elements that enter a tie changed their relative position with respect to each other at this very unique weight-tuple [equivalent class](https://en.wikipedia.org/wiki/Equivalence_class) (1/1 = 2/2 = 3/3...), there are at least **(the number of tie-conditions) + 1** different orders (two separators seperates three books!), and all such generated orders are distinct! There are also at most so many too because between two tie-breaking fractions the order remains the same (def of neighboring)!

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

### Correct code after the contest

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

This solved the TLE problem. We first just generate a list of maximum size 90000, then we convert it into a set in one go. The size of the hashtable will thus be decided at the end and hashing/resizing is done only once.
