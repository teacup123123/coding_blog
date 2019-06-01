---
layout: post
title: "Google Kick Start 2019 Round C Q2 Circuit Boards [given up]"
author: Tikai Chang
tags: ["GKS", "competition", "python"]
comments: true
status: "canceled"
betterid: "/2019/06/01/Circuit-Boards-Better"
---

The original question statement is [here](https://codingcompetitions.withgoogle.com/kickstart/round/0000000000050ff2/0000000000150aae)

### Restating the problem

Arsh has an R-by-C circuit board of inhomogenious thickness, each of the $$R\times C$$ cell has an integer thickness $$V_{r,c}$$. He wants to cut a subcircuit board from it which is rectangular and verify that the thickness of the thickest and thinnest cell is within a difference of K

An example:
```
K=2
from the following:
987689
923438
923438
988873

2343
2343
is a valid circuitboard
```
Please find the largest possible area obtainable from a valid subcircuit board.

#### limits

R,C between N=1 to 300
Thickness integer in 0 to 1000

### Reflection

Of course, this question requires a min and max computation over a rectangular range. Then verification of the difference between them. Since max(X:X iterable) is the same as -min(-X:X iterable). We will forget the max aspect of things...

I had experience with another question that required quick min range lookup of a sublist of a list of size N. The bruteforce algorithm would take time complexity N for iterating over all elements in the range. There is an log-algorithm to speed it.

The idea is to precache queries of size 2^t, The answer from the query of two consequtive queries of size 2^(t-1) can be combined to make the answer for another of size 2^t. Iterating from sizes of 2^0, and going up to t=log(300) would take fewer than 300*log(300) combinations and a memory of the same size. A non 2^t-sized range would be done as follows:
- write the size in binary.
- for each non-zero digit, we lookup the precached table
- we combine the results from these lookups
Since there are at most log N lookups, that is the time complexity

However, this problem is a 2D problem. And maybe that is not the same as a simple range-min query over 1D? Is there anything we can borrow?

Well, the two dimensions are not independent: observe in the following case:
```
AB
CD

A,B,C,D adjacent subcircuits

We know that:

min(C)>=min(AC)>=min(ABCD)
min(C)>=min(CD)>=min(ABCD)

but it is hard to say anything about min(AC) and min(CD)...
```

So I get the feeling that the loops in the horizontal direction must always be present... Brute force would take N^2 to decide the two x-boundaries, N^2 for the y-boundaries, N^2 to iterate over all cells within. That is a whooping N^6 = 723000000000000 iterations...

Well, we can first think about the 2D-query of a min-range-2D. By caching all sizes of 2^I-by-2^J rectangles, we can make a 2D version of the 1D rangemin algo.
The maximum number of subrectangles in the rectangle would be logN x logN. So if we iterate over all boundaries with this method, it will become N^4 log(N)^2 = 8100000000*81 = 656100000000~10^12 still too big... The precaching will take N^2 log(N)^2 - negligeable in front of the lookup.

The skeleton would be something like this:

```python
for x_start in range(300):
  for x_end in range(300):
    for y_start in range(300):
      for y_end in range(300):
        doThe2DLog300Lookup(x_start,x_end,y_start,y_end)
```


Then I remembered this [video](https://www.youtube.com/watch?v=XKu_SEDAykw). And I thought about maybe using a two way algorithm... This time the ends are not leftmost and rightmost. But positions 0 and 1. You start off with a unitary subcircuit in the y direction.


```python
for x_start in range(300):
  for x_end in range(300):
    while notBreaked:
      y_start = 0
      y_end = 1 # not included
      res = doThe2DLog300Lookup(x_start,x_end,y_start,y_end)
      if res.valid:
        #too easy to verify with a small subrect, make it bigger!
        y_end+=1
      else:
        #a bit too big...
        y_start+=1
      if y_start == 301:
        break
```
This catepiller movement of `y_start` and `y_end` is so cute :D.
We know for sure that the catepiller can only move forward, so the complexity is N for this while loop. giving a complexity of N^3. The question is will this caterpiller go over all valid configs?

Say the optimal config is [A~B]x[C~D]
A and B are bruteforcefully covered
At a certain moment, `y_start` *is going to become C*, by a rightward movement from y_start = C-1. If `y_end` is left of D, it will now advance until it works, never becoming too big in the process so as to necessite shifting of `y_start`. Is it possible that `y_end` is already right of D? Well in that case going back to the moment when `y_end` just became D, `y_start` must be on the left of C, since that event happened afterwards! And so `y_start` will keep on advancing because it stays invalid until it hits that C, *otherwise, violation of optimality*!

Now that is a whooping N increase, but still,
```python
for i in range(300*300*300*9*9):
    pass
```
took me like a few minutes...
You can't really generalize this to 2D, because the step `beGreedier()` can be interpreted as expand `y_end` or expand `x_end` as in `if stillValid(): beGreedy()`. These kind of binary choice is typical of entering the realm of NP expontial branching...

Or so I thought..., it occured to me that this caterpiller parcours all locally maximal y-ranges for fixed x-ranges. The caterpiller doesn'y care about the achieved size of the rectangle.

Maybe we could define jumps of the caterpiller... if a rectangle of size S was already discovered, nothing to lose by skipping over smaller tries. Nope that doesn't really work, because now the caterpiller might find itseld stuck in a local minimum, not being able to shrink to rebound :(

Another idea flashed, if we have no choice but to bruteforce the y-ranges, maybe we could use the same philosophy on the x-ranges, but considering the size obtained...

Ha I thought about what I call a Fermi Energy Level method:

```python

for sizeGoal in decotomy():
  x_start,x_end = 0,1
  deltaY = caterpillerOnY(x_start,x_end)
  #returns the best Y interval given an x interval
  size = deltaY*(x_end-y_end)
  if size>=sizeGoal:
    #it was too easy, let's become greedier
    x_end+=1
  else:
    # too bad, we should relax the bruteforce
    x_start+=1
```

That will work! Total complexity now is `log(300*300)*300*300*log(300)^2 = 300*300*18*9*9`

```python
for i in range(300*300*18*9*9):
    pass
```

Took 8 seconds! That should do the job!
### Implementation

So I start off by writing a python iterator that does dichotomy in a general way,
it returns besides the probing value two functions that are calleable and will tell the iterator to go up or down, the user should call `higher()` or `lower()` wisely depending on the situation. This code is salvagable for future problems
```python
import numpy as np
import itertools

# dechotomy over a size goal,
# lower and higher are always returned as signaler functions
def dechotomy(sizeGoal):
    low, high = 0, sizeGoal

    def higher():
        global low
        low = mid

    def lower():
        global high
        high = mid

    while True:
        mid = (low + high) // 2
        yield mid, lower, higher
```

Now, we process the inputs.
{% include GCJ_caseT.html %}

```python
# main contest body
t = int(input())
for ti in range(1, t + 1):
    r, c, k = tuple(map(int, input().split()))
    grid = []
    for ri in range(r):
        grid.append(list(map(int, input().split())))
    grid = np.array(grid, dtype=int)
    # variables now all loaded
```

Now that we have loaded the problem into a 2D array, we may begin precaching.
By using numpy (based on C), I hope that I can gain a bit of speed. Although here it is not important, the bottleneck is the number of queries.

```python
    #dynamical program used to precalculate lookups of size 2^I x 2^J
    _ = []
    for operation in [np.max, np.min]:
        precache_max_or_min = np.zeros((r, c, 9, 9), dtype=int)
        precache_max_or_min[:, :, 0, 0] = grid
        for i in range(8):
            for j in range(8):
                temp = np.zeros((r, c, 2), dtype=int)
                temp[:, :, 0] = precache_max_or_min[:, :, i, j]
                temp[:, :, 1] = \
                np.roll(precache_max_or_min[:, :, i, j], -2 ** j, axis=1)
                temp = operation(temp, axis=2)
                precache_max_or_min[:, :, i, j + 1] = temp
            temp = np.zeros((r, c, 2, 9), dtype=int)
            temp[:, :, 0, :] = precache_max_or_min[:, :, i, :]
            temp[:, :, 1, :] = \
            np.roll(precache_max_or_min[:, :, i, :], -2 ** i, axis=0)
            temp = operation(temp, axis=2)
            precache_max_or_min[:, :, i + 1, :] = temp
        _.append(precache_max_or_min)
    precache_max, precache_min = _
```
The two variables `precache_max`, `precache_min` should now contain queries of size 2^Ix2^J. Note that by using roll, I am summing in a cylindrical fashion. It is up to the caller to be responsible for not specifying a range that goes out of range.

Now we implement lookups of any arbitrary size, which returns true or false depending on whether the k-limit is surpassed.
```python
    # The actual lookup for any sizes
    def lookup(xlow, xhigh, ylow, yhigh):
        szx = xhigh - xlow
        szy = yhigh - ylow
        collectedx = []
        collectedy = []
        while szx > 0:
            collectedx.append(szx % 2)
            szx = szx // 2
        while szy > 0:
            collectedy.append(szy % 2)
            szy = szy // 2

        sublookupx = []
        sublookupy = []
        cursor = 0
        for xi, x in enumerate(collectedx):
            if x == 1:
                sublookupx.append((cursor, xi))
                cursor += 2 ** xi
        cursor = 0
        for yi, y in enumerate(collectedy):
            if y == 1:
                sublookupy.append((cursor, yi))
                cursor += 2 ** yi
        minFound,maxFound = grid[xlow,ylow],grid[xlow,ylow]
        for (x, xi), (y, yi) in itertools.product(sublookupx, sublookupy):
            maxFound = max(maxFound, precache_max[x, y, xi, yi])
            minFound = min(minFound, precache_min[x, y, xi, yi])
        if minFound+k>=maxFound:
            return True
        else:
            return False

```
### Realization of a big error

The algorithm doesn't work. For each pair `(xlow, xhigh)`, we can indead find in
 $$ 300*\log(300)^2$$ time the corresponding optimal `(ylow,yhigh)` pair that maximizes the surface.
 Suppose that we suspect that an optimum exist at $$S_{optimal}$$ (near the end of the dechotomy), for example, we found a rectangle of size $$S_{optimal}-1$$, and failed to find one at $$S_{optimal}+1$$, there is still no way to determine whether to do `xlow+=1` or `xhigh-=1` halfway through the iteration.

### Another clever idea

So we have been having big headaches over the 2D aspect, and not being able to control the second caterpiller. Actually I was bound by my deep thought. We could have simply sorted all pixels into a 1D array by thickness.

```
L = [(v_ij,i,j)...]#sorted in increasing order
```

 I have a hunch that I can then perform the caterpiller algorithm over this 1D array of size $$300^2$$.

 Let's suppose that a valid rectangle [a:b]x[c:d] exists with min,max = m,M. This statement is equivalent to saying that the leftward (of m) and the rightward (of M) doesn't have any pixel inside that rectangle

 OK I now have an idea for constructing an algo:
 ```
For all locally maximal caterpiller pairs (I,J)
such that abs(L[I][0]-L[J][0])<=k:
  #complexity is now 300^2


  #Find the biggest rectangle that is valid,
  #using dechotomy of the four boundaries
  For all possible 4 boundaries:
    # complexity multiplied by log(300)^4

    check validity
    # multiplied by log(300)^2
 ```

 In total the complexity should be $$\log(300)^6 * 300^2 = 47829690000 $$ that's still too big.

 I think the dichotomy is a waste of time. Actually what you can do is follow along the caterpiller. The thinnest pixel to be newly engulfed by the complementary of the catepiller range can only make an already valid rectangle smaller and by how much can be answered in `O(1)` time: just see if the included pixel falls in the rectangle!

 The new pixel that is released from the complementary into the caterpiller is more problematical if it is outside the rectangle. The rectangle can be bigger, in the direction of the pixel, the worst case we will have to do dichotomy over two of the four boundaries. Therefore speeding it up by ~100X

 What is better is that Actually it is never both boundaries at the same time, so this speeds it again by 5X.

 Implementing it, I noticed that the pixel leaving the catepiller into the boundary can break a valid rectangle into two valid rectangles of equal size. Which one should we choose? The reverse is true, for a pixel leaving the complementary, it is absolutely possible that the biggest rectangle can jump (have no overlap at all with the old one). So once again it is wrong to assume following the caterpiller would work. Surely there must be a way!?

Let us revisit what we saw: without sorting pixels we were able to transform iteration of one of the two dimensions from 300^2 to 300*log(300). But the other dimension was stuck at 300^2. Then we did pixelization unidimensionalification, shrinking complexity from 300^4 to 300^2. This is without taking into account the query time.

#### Eureka moment

Oh god I just realized something, the number of caterpiller pairs is actually extremely low. since the thicknesses vary from 1~1000. It means that the there are at most 2000 caterpiller pairs... For each caterpiller pair, you have a fixed thickness range, so you transformed your question as follows:
```
given a boolean array 300x300 representing "isInRange?"
find the biggest area of a contingous rectangle
```

Actually, swapping the `min`, `max` operation in the dynamical programming by `and`, you can precache the question "Is this the top left corner of a 2^t sized square?" From which you can construct a quick query of $$log(300)^2$$. I believe that some more complicated construction might let you construct answers to the query: what is the biggest rectangle whose top right corner is you? And I believe it can be done in a single log(300) passage...

The overall complexity will be `2000*(300^2*log(300))`.

But I think I already surpassed too much the thinking time for this question. I should probably just give up and look at the answer...
