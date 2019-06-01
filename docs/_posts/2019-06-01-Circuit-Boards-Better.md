---
layout: post
title: "Google Kick Start 2019 Round C Q2 Circuit Boards [Revision]"
author: Tikai Chang
tags: ["GKS", "competition", "python"]
comments: true
status: "done"
---
Let us start anew and look at the [solution](https://codingcompetitions.withgoogle.com/kickstart/round/0000000000050ff2/0000000000150aae) (click analysis).

First of all my min/max-range can be speeded up by the log(300). My mistake... Just take a look [here](https://www.geeksforgeeks.org/sparse-table/). You only need to take two subranges of maximally 2^T size to cover any range!

So here they transform the finding the maximum rectangle problem into finding the biggest rectangle under a histogram. (They say *well known* method, but this is the first time I see this ><...) Very clever indeed.

For the test set two, the first sentence is very difficult to parse... The meaning of Pij is the maximum horizontal line segment size starting at this pixel. So there, dichotomy and 1D-min-range queries should be used.

Oh no.... I completely misunderstood the question!!!
>A circuit board is good if in each row, the difference between the thickest square and the least thick square is no greater than K.


So we are indeed back to the old problem of finding the biggest rectangle under a histogram

>If we use a data-structure like Sparse Table to answer the range minimum and maximum queries then we can find all the P-values in O(RClog(C)) time. The last part of finding the largest area rectangle in histogram should be done once for each column, and hence takes O(R) time for each case resulting in O(RC) time in total. Combining both, we have a final complexity of O(RClog(C)). We can further reduce this to a complexity of O(RC) by replacing the Sparse Table data-structure with a two pointers variation using two deques, that approach is left as an exercise for the reader.

For a linear 1D array find for each pixel the largest segment starting from that pixel verifying the K-condition in linear time. I do believe they are speaking of the caterpiller algorithm. I see two pointers but in my case I had used a sparse-table based query in the end.

If you start the catepiller from the right it will be possible to do an assignement of the P table during all expansion steps of the caterpiller under O(1) time. But the implosion steps of the caterpiller you will have to recalculate the min max values of the caterpiller...

I'll keep this in the back of my head, consider this problem solved.
