---
layout: post
title: Reflections regarding maximum pairing
author: Tikai Chang
tags: [algorithm]
comments: true
status: "working"
---

I am solving a problem in which we present an undirected graph of 100 nodes, highly connected (the complementary graph regarding edges seems sparse). The question is to find the maximum pairing in the graph.

It could be seen as an linear programming problem with integer constraints. At first I conjectured that the BFS's *are exactly* the matchings. So I started writing an LP solver. Then after pen-and-paper work I found out that There are graphs in which the optimal BFS is actually fractional.

```
Graph: integers designates nodes, with a total of 6
1,2,3 are interconnected
4,5,6 are interconnected
variables: one variable per edge
objective function (max) is the total number of edges
constraints: sum of all edges connected to a node is at most 1

Solution:
all edges between 1,2,3 and respectively 4,5,6 have 0.5 as the value
```

So Apparently the conjecture that LP programming will give a good *integer* solution is wrong.

So I really had to ask my self do I actually want to write a MIP solver?

I was halfway through the Implementation of LP and I saw that the [Blossom algorithm](https://en.wikipedia.org/wiki/Blossom_algorithm) solves this problem exactly. So I am hesitating whether or not to code the Blossom algorithm from scratch and throw the LP into the bin...

So I dwelved into the article on the Blossom Algo, and looked at how it actually worked. First thing that struck me was Berge's Lemma, which stated:
> a matching M in a graph G is maximum (contains the largest possible number of edges) if and only if there is no augmenting path (a path that starts and ends on free (unmatched) vertices, and alternates between edges in and not in the matching)

This kinds of feels like the jump from BFS to BFS in linear programming. So it led me to rethink the conjecture again, maybe we do have:
> all matchings are BFS's, although the inverse is not true.

The intuition for a proof is that the geometrical interpretation of BFS's are vertices of a convex polytope. And that seems to me like points that are essentially intersections of the most number of hyperplane boundaries. The boundaries for matching are just that all edges are between 0 and 1, and that the sum of edges stemming from a vertex is between 0 and 1. Both of these constraints are at their interval boundaries, therefore it seems to be the case.

If this is indeed the case, MIP programming which always explores integer solutions, which are essentially valid pairings, will be limited to BFS's. So in this special case, it seems to me that MIP doesn't need to explore the interior of the polytope for integers close to the fractional optimal solution. Doing a bread-first search of all neighboring BFS's until we find the best *integer* BFS seems likely to work.

Moreover if this is the case, Berge's lemma says is that within all integer BFS's, either we are optimal or either there is a local move (augmented path) which improves our solution. My intuition is that this augmenting local move might actually be a valid LP transition? The augmenting path can be seen as lifting the constraint of the sum of the 2 vetices, and changing the value from 0 to 1. all other constraints remain untouched! My idea is the following: if there is a path visiting only integer BFS's to reach the augmented path then by restricting only to integer BFS we would reproduce the Blossom algorithm?

Let us revisit the LP transition, we replace one non zero edge variable with another originally-zero variable which takes on the non-zero role. In other words, we assign something from 0 to non-zero, and adjust all originally non-necessary-zeros accordingly. Just with this description, no proof seems to exist. Let me try to make a counter example for a general graph.
```
4 <= x+y <=6
1 <= x-y <=3
maximize x
BFS's:
(2.5,1.5;0,2,0,2) # note the slack variables after ;
(3.5,2.5;2,0,0,2)
(4.5,1.5;2,0,2,0)
(3.5,0.5;0,2,2,0)

All bfs are fractional!
```

If this is to work, then for sure we need to use the special structure of the model. First of all there are as many constraints as there are nodes N each summing to 1, whereas the in an integer BFS the number of pairs will never exceed N/2. This means starting from an integer BFS for example the trivial 0,0,0..., and making a move to a neighboring BFS. Let's take a triangle:
```
(0,0,0;1,1,1)# edges order: 3-2, 1-3, 1-2; slack indexed by node num
during transition: (0.5,0,0;1,0.5,0.5)
(1,0,0;1,0,0)
during transition: (0.5,0.5,0;0.5,0.5,0)
(0,1,0;0,1,0)
```
So it would seem to me that in this example the LP transition from integer BFS to integer BFS corresponds to a alternating shift that preserves the objective function, exposing eventually vertices that we can later connect.

## Summary:
I could either:
- implement the Blossom algorithm

Moreover if my conjecture
> all matchings are BFS's, although the inverse is not true.

is true , then:
- LP -> dijstra-like breadfirstsearch for integer BFS would produce a good result, this would be like a convenient MIP which happens to visit only BFS's

Let A be an augmented path with respect to P. The augmentation is essentially an objective-preserving shift, followed immediately by the addition of a pair. The shift corresponds to adding the last edge variable into the basic variables and exiting the first edge variable. The addition is exiting a slack in favor of an edge. So in total 4 variables entered/exited the basic variables according to this decomposition, fewer than 2 LP moves suffice to reproduce the augmentation (maybe there is a way to say 1 LP move suffices?). To detect the improvement will be the key, so a depth-2 LP search limited on integer BFS's should suffice (again maybe entering the added edge and exiting the slack of the last node might suffice to do it in 1 LP move?).
- depth-2-LP limited on integer BFS's will probably work
- depth-1-LP limited on integer BFS's will probably work, I think exiting the last node's slack, and entering the added edge will reproduce an augmentation.

But since all this is not so rigorous I thik the likelihood of obtaining a 100% working algo is Blossom > LP-breadfirstsearch > depth-2 LP on int > depth-1 LP on int.

I think the rational decision is to implement Blossom or LP-breadfirstsearch.
I'll upload my code once I have coded it.  
