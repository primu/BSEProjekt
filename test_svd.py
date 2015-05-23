import numpy as np

def feature(memory, how_many_stays):
    u, s, v = np.linalg.svd(memory)
    S = np.diag([val if i < how_many_stays else 0 for i, val in enumerate(s)])
    # S = np.diag(s[:how_many_stays])
    feature = np.dot(S, v)

    return u, np.delete(feature, len(feature) - 1, 0)

def transpose(array):
    return [list(i) for i in zip(*array)]

stays = 3

memory1 = [[1, 0, 1, 0, 0], [1, 1, 1, 0, 0], [1, 0, 1, 0, 0], [1, 1, 1, 0, 0]]
memory2 = [[0, 1, 0, 1, 1], [0, 1, 1, 1, 1], [0, 0, 0, 1, 1], [0, 1, 0, 1, 1]]

memory1 = transpose(memory1)
memory2 = transpose(memory2)

u1, feature1 = feature(memory1, stays)
u2, feature2 = feature(memory2, stays)

compare = [[0, 1, 0, 1, 1]]
# compare = transpose(compare)

compare1 = np.dot(compare, u1)
compare1 = np.delete(compare1, -1, 1)
compare1 = np.delete(compare1, -1, 1)

# compare1 = np.dot(compare1.T, compare1)

compare2 = np.dot(compare, u2)
compare2 = np.delete(compare2, -1, 1)
compare2 = np.delete(compare2, -1, 1)

# compare2 = np.dot(compare2.T, compare)

norm1 = np.linalg.norm(compare1.T - feature1)
norm2 = np.linalg.norm(compare2.T - feature2)

print(norm1)
print(norm2)