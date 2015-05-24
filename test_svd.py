import numpy as np

def get_feature(memory, how_many_stays):
    u, s, v = np.linalg.svd(memory)
    S = np.diag([val if i <= how_many_stays else 0 for i, val in enumerate(s)][:how_many_stays])
    print(u.shape, s.shape, v.shape)
    for x in range(how_many_stays):
        v = np.delete(v, -1, 0)

    feature = np.dot(S, v)

    return u, feature

def transpose(array):
    return [list(i) for i in zip(*array)]

def flatten(data):
    return [item for sublist in data for item in sublist]

stays = 3

memory1 = [[1, 0, 1, 0, 0], [1, 1, 1, 0, 0], [1, 0, 1, 0, 0], [1, 1, 1, 0, 0]]
memory2 = [[0, 1, 0, 1, 1], [0, 1, 1, 1, 1], [0, 0, 0, 1, 1], [0, 1, 0, 1, 1]]

memory1 = transpose(memory1)
memory2 = transpose(memory2)

u1, feature1 = get_feature(memory1, stays)
u2, feature2 = get_feature(memory2, stays)

compare = [[0, 1, 0, 1, 1]]
# compare = transpose(compare)

compare1 = np.dot(compare, u1)
for x in range(len(compare1[0]) - stays):
    compare1 = np.delete(compare1, -1, 1)


# compare1 = np.dot(compare1.T, compare1)

compare2 = np.dot(compare, u2)
for y in range(len(compare[0]) - stays):
    compare1 = np.delete(compare2, -1, 1)

# compare2 = np.dot(compare2.T, compare)

from scipy.spatial.distance import euclidean

norm1 = euclidean(flatten(feature1)[:4], flatten(compare1))
norm2 = euclidean(flatten(feature2)[:4], flatten(compare2))

print(norm1)
print(norm2)