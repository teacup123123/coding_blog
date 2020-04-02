import numpy as np
import numpy.random as rd
import matplotlib.pyplot as pl


def new_proba(sz):
    probas = []
    probas.append(np.ones(sz) * 0.33)  # Bnei Brak tests, high risks
    probas.append(np.ones(sz) * 0.1)  # Tel Avivan tests, medium risks
    probas.append(np.ones(sz) * 0.04)  # American tests
    probas.append(np.ones(sz * 10) * 0.005)  # Taiwanese tests
    return np.concatenate(tuple(probas))


def entropy_unit(p):
    return -np.log2(p) * p - np.log2(1 - p) * (1 - p) if p != 0 and p != 1 else 0


def entropy(probas):
    return sum(entropy_unit(p) for p in probas)


probas = new_proba(200)
answer = np.array([rd.random() < p for p in probas], dtype=bool)


def mix_and_test(sublist):
    positive = 1 - np.product([0 if infected else 1 for infected in answer[sublist]])
    # print(f'{sublist}:{answer[sublist]} -> {"positive" if positive else "negative"}')
    return positive == 1


rounds = 0
positive_clusters = []
entropies = []
while entropy(probas) > 0:
    entropies.append(entropy(probas) + rounds)
    # entropies = np.array(list(map(entropy_unit, probas)))
    # sorted_i = np.argsort(entropies)
    sorted_i = np.argsort(probas)
    sorted_i = list(sorted_i)
    sorted_i = list(filter(lambda i: entropy_unit(probas[i]) > 0, sorted_i))
    # print(f'remaining patients to test {len(sorted_i)} rounds + entropy = {entropy(probas) + rounds}')
    sublist = []
    while np.product(1 - probas[sublist]) > 0.5 and len(sorted_i) > 0:
        if len(sorted_i) > 0:
            sublist.append(sorted_i.pop(0))
    # assert is_approximately_the_same(entropy(sublist), 1)
    result = mix_and_test(sublist)
    rounds += 1
    if result:
        # update the probabilities on the sublist, conditioned on the result being positive
        infected = list(filter(lambda i: answer[i], sublist))
        # print(f'\t{sublist}({infected} infected):{probas[sublist]} -> {probas[sublist] / np.sum(probas[sublist])}')
        print(f'\tPOSITIVE {len(sublist)} tested ({len(infected)} )!')
        probas[sublist] = probas[sublist] / np.sum(probas[sublist])  # first order
        positive_clusters.append(sublist)
    else:
        # All in the sublist are all safe
        print(f'\tNEGATIVE {len(sublist)} tested')
        for c in positive_clusters:
            for s in sublist:
                if s in c:
                    c.remove(s)
                    probas[c] += probas[s] / len(c)
                    probas[c] = np.minimum(0.9, probas[c])
                    if len(c) == 1:
                        probas[c] = 1
                        print(f'\t\t exclusion principle {sublist} -> {1}')
        positive_clusters = list(filter(lambda l: len(l) > 1, positive_clusters))

        probas[sublist] = 0

print(f'sanity check: {"ALL GOOD" if np.product(answer == probas) else "ERROR"}')
print(f'speedup:{len(probas) / rounds}')
pl.plot(entropies)
pl.show()
