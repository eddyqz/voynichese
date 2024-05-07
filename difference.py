# Based on closest_friend.py
# Finds the closest word vector in B to a vector in A, no repeats.

import fasttext
import numpy as np
import numpy.linalg as npla
import math
from lang_labels import *
from get_word_characteristics import find_language
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt

def angle_between_vectors(first, second, model):
	"""
	takes in two words and a model, and gives the angle between them
	
	"""
	v1 = model[first]
	v2 = model[second]
	return math.acos(np.dot(v1, v2)/(np.linalg.norm(v1) * np.linalg.norm(v2)))

path = "models/voynich.bin"
model = fasttext.load_model(path)


words = list(model.words)
# in words is '</s>' which is not an actual word. Thus, it must be removed
words = words[1:]

a_words = []
b_words = []
both_words = []
for word in words:
	if find_language(word, lang_labels) == "A":
		a_words.append(word)
	if find_language(word, lang_labels) == "B":
		b_words.append(word)
	if find_language(word, lang_labels) == "Both":
		both_words.append(word)
        

used_words = []
closest_a_b_pairs = []
num_vectors = 40
# A has fewer words than B, 51 unique to be exact
all_pairs_and_angles = []
for a_word in a_words:
	tmp = [[a_word, b_word, angle_between_vectors(a_word, b_word, model)] for b_word in b_words]
	all_pairs_and_angles.extend(tmp)

all_pairs_and_angles.sort(key = lambda x: x[2])
for a_word, b_word, _ in all_pairs_and_angles:
	if a_word in used_words or b_word in used_words: continue
	closest_a_b_pairs.append([a_word, b_word])
	if len(closest_a_b_pairs) >= num_vectors: break

difference_vectors = [model[a]-model[b] for a,b in closest_a_b_pairs[:num_vectors]]
difference_vectors = np.array(difference_vectors)
tsne = TSNE(n_components=2, metric='cosine')
image = tsne.fit_transform(difference_vectors)
plt.scatter(*zip(*image), c="r", marker='.')
plt.title("Distribution of Difference Vectors A - B Without Repeats")
plt.savefig("images/difference_vectors_a_b_no_repeats.png")

	
# not accounting for a and b
control_used_words = []
control_closest_a_b_pairs = []
control_all_pairs_and_angles = []
num_vectors = 150


for a_word in words:
	tmp = [[a_word, b_word, angle_between_vectors(a_word, b_word, model)] for b_word in words if a_word!=b_word]
	control_all_pairs_and_angles.extend(tmp)

control_all_pairs_and_angles.sort(key = lambda x: x[2])
for a_word, b_word, _ in control_all_pairs_and_angles:
	if a_word in control_used_words or b_word in control_used_words: continue
	control_closest_a_b_pairs.append([a_word, b_word])
	if len(control_closest_a_b_pairs) >= num_vectors: break
	
control_difference_vectors = [model[a]-model[b] for a,b in control_closest_a_b_pairs[:num_vectors]]

		

	
control_difference_vectors = np.array(control_difference_vectors)
tsne = TSNE(n_components=2, metric='cosine')
control_image = tsne.fit_transform(control_difference_vectors)
plt.scatter(*zip(*control_image), c="r", marker='.')
plt.title("Distribution of Closest Difference Vectors Without Repeats")
plt.savefig("images/difference_vectors_no_repeats.png")
plt.show()