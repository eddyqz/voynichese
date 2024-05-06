# Based on closest_friend.py

import fasttext
import numpy as np
import numpy.linalg as npla
import math
from lang_labels import *
from get_word_characteristics import find_language
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt



path = "models/voynich.bin"
model = fasttext.load_model(path)

words = list(model.words)
# in words is '</s>' which is not an actual word. Thus, it must be removed
words = words[1:]

vectors = np.array([model[w] for w in words])
mag = npla.norm(vectors, axis=1)[:,None] * npla.norm(vectors, axis=1)
sims = np.divide(np.dot(vectors, vectors.T), mag)
sims = np.tril(sims, -1) # don't align to self and remove dups
indices =  np.argsort(sims, axis=1)

word_dist = []
for i, w in enumerate(words):
	L = [(w, words[j], math.acos(sims[i, j])) for j in indices[i, :]]
	word_dist.extend(L)
	
word_dist.sort(key = lambda x: x[2])

closest_a_b_pairs = []
difference_vectors = []

num_vectors = 100

# A vs B analysis, includes repeats
for first, second, _ in word_dist:
	if find_language(first, lang_labels) == "A" and find_language(second, lang_labels) == "B":
		closest_a_b_pairs.append([first, second])
		difference_vectors.append(model[first] - model[second])
	elif find_language(first, lang_labels) == "B" and find_language(second, lang_labels) == "A":
		closest_a_b_pairs.append([second, first])
		difference_vectors.append(model[second] - model[first])
	if len(closest_a_b_pairs) >= num_vectors:
		break

difference_vectors = np.array(difference_vectors)
tsne = TSNE(n_components=2, metric='cosine')
image = tsne.fit_transform(difference_vectors)

plt.scatter(*zip(*image), c="r", marker='.')
plt.show()

# Control analysis, repetitions included
# control_closest_a_b_pairs = []
# control_difference_vectors = []
# for first, second, _ in word_dist[:num_vectors]:
#     control_closest_a_b_pairs.append([second, first])
#     control_difference_vectors.append(model[second] - model[first])
	
# control_difference_vectors = np.array(control_difference_vectors)
# tsne = TSNE(n_components=2, metric='cosine')
# control_image = tsne.fit_transform(control_difference_vectors)
# plt.scatter(*zip(*control_image), c="r", marker='.')
# plt.show()