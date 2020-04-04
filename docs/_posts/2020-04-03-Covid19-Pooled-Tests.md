---
layout: post
title: Covid 19 Pooled Diagnosis
author: Tikai Chang
tags: [algorithm]
comments: true
status: "working"
---
full story [Part I here](https://medium.com/@teacup123123/the-benefits-and-limits-of-pooled-screening-and-how-it-can-accelerate-covid-19-screening-part-1-2-6bf11dd7def6) and 
[Part II here](https://medium.com/@teacup123123/the-benefits-and-limits-of-pooled-screening-and-how-it-can-accelerate-covid-19-screening-part-2-2-3278af7ecbc7)

Here I will put the technical details of how to prove by reduction that we can not do better than the shannon entropy of the population using Pooled Testing.


## Proof by reduction of the Shannon Entropy limit of Pooled Testing
We will take as granted the following property. And we will reduce the problem of Pooling faster-than-Shannon to the central problem behind this property, is communicating faster-than-shannon possible?  
### Theorem: The Marginal Communications Cost is bounded by the Entropy (textbook example, given without proof)
Given a random experiment with different outcomes (say a dice has 6 outcomes), whose distribution is not necessasarily uniform. We wish to communicate over a bit-channel the outcome. You may share beforehand conventions, algorithms, since what we are interested is the marginal cost -- we wish to repeat a huge number of times, therefore all overhead beforehand is irrelavent, since the random experiment has not been performed, and you can not smuggle any data in the preparation stage. We require correctness: your compression should be lossless, the decompression should be faithful.

In this case, the *marginal* (i.e. per single run of the experiment) Cost (unit:bit) is bounded by the Entropy associated to the probability distribution -- whatever the algorithm, whatever the distribution.
### Defining properly an Algorithm for Pooled Testing (APT)
Let us give the specs of a deterministic algorithm on Pooled Testing:
- It takes as input, a known probability vector P discribing the probability of each individual (labeled i=1~N) to be tested.
- In a deterministic manner, it outputs a subset of the labels of the individuals to be included in the next pool. And it patiently wait for you to perform that test and await your input of the result.
- The previous step is repeated many times, after that it outputs a boolean vector declaring who is infected and who is not.
- Correctness requirement: On the assumption that there are no false positives/negatives inputed to the algorithm, each individual declared as negative have participated at least in one negative pool. Each individual indicated as positive have not been tested negative and has participated in a pool in which all others are declared neagative. The log of the interaction should be coherent and each input must be in accordance to the OR result of each participents' declaration.

### Wrapping the Algorithm in a compression algorithm.
We write the following program to compress a N-Tuple Boolean Variable whose sub-Boolean Variable are described by a probability vector P. The subvariables are independently distributed.

1. The preparation overhead before the streaming of data: we share the P vector as a given prior to the receiver.
2. We call the APT algorithm defined above and input the vector P as the sickness vector.
3. For each participent label subset outputed by the APT, we perform the OR operation on the subvariables of the N-Tuple Variable. The result is inputted back to the APT algorithm. During the whole process we keep each boolean inputted to the APT algorithm in a sidenote log.
3. If the APT correctedly behaves, the declaration should match the N-Tuple Variable you wish to compress.
4. We transmit the APT-log to the receiver. It does not including the P vector since P is shared beforehand in the preparation.

Decompression works trivially, the only difference being we read the interaction log received and input the yes/no to the pools asked accordingly. Since the APT algorithm is supposedly deterministic, the interaction sequence is identical to compression. Finally, we take the declaration as the decompressed original message.

From the point of view of the APT algorithm, the interaction it sees is identically distributed to a scenario where COVID19 pooled testing is being done. It can not guess that you were actually using it to compress a variable over the internet...

We have thus realized a compression algorithm on Boolean Tuples described by any probabilty P. According to the theorem stated above the size of the message should be smaller than the entropy. We just prooved that the number of boolean inputs (each corresponding to a COVID19 testing pool) must be inferior to the Shannon Entropy. CQED.

### Illustrative use of the reduction process

Say that we wish to compress statistics on a battlefield continuously to the Central Command. We know that the first variable indicates the weather: sunny/cloudy (In England that's 10-90 chance...). The next 100 bits describes if the 100 soldiers in your battailion are operational or not. After some statistics you know that they are healthy, and the odds are 99-01. You can compress using the APT algorithm taking as parameter the probability list 0.1,0.99,0.99 .... 
