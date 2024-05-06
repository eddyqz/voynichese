#!/usr/bin/python
import io
import numpy as np
import numpy.linalg as npla
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import fasttext
import argparse
import sys
import math

<<<<<<< HEAD
from get_word_characteristics import find_language, find_scribe, did_scribe_write_word
import vms_tokenize
=======
from get_word_characteristics import find_language, find_scribe, did_scribe_write_word, is_word_in_topic, get_scribe_count, find_topic
>>>>>>> 6fd57d2498e5a94a3c186a37ce4e73ac8980a1b6

from lang_labels import *
from scribe_labels import *
from section_labels import *
from random_sample import get_random_dialect_sample

path = "models/voynich.bin"
model = fasttext.load_model(path)

words = list(model.words)

# print(words)
# from this print statement, it was discovered that the first "word"
# in words is '</s>' which is not an actual word. Thus, it must be removed
words = words[1:len(words)]
# print(words)

vectors = np.array([model[w] for w in words])

mag = npla.norm(vectors, axis=1)[:,None] * npla.norm(vectors, axis=1)

sims = np.divide(np.dot(vectors, vectors.T), mag)
sims = np.tril(sims, -1) # don't align to self and remove dups
### changed this to :1 to only get top match for plotting
indices = np.flip(np.argsort(sims, axis=1), axis=1)[:,:1]

word_dist = []
for i, w in enumerate(words):
	L = [(w, words[j], math.acos(sims[i, j])) for j in indices[i, :]]
	word_dist.extend(L)
	# print w
	# for _, match, dist in L:
	# 	print "\t", match, "\t", dist

word_dist.sort(key = lambda x: x[2])

# for w in word_dist:
# 	print (w[0], "&", w[1],  "\t", w[2])


def annotate(image, words, n=float("inf")):
	annotation_list = []
	for i, (label, x, y) in enumerate(zip(words, image[:, 0], image[:, 1])):
		if i == n: break
		plt.annotate(
			label,
			xy=(x, y), # xytext=(-20, 20),
			alpha = 0.4,
			# textcoords='offset points', ha='right', va='bottom',
			# bbox=dict(boxstyle='round,pad=0.5', fc='black', alpha=0.5),
			# arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0')
		)

tsne = TSNE(n_components=2, metric='cosine')
image = tsne.fit_transform(vectors)

#####################################
# plotting code
color = {
	'A': 'red',
	'B': 'blue',
	'X': 'grey',
	'Both': 'purple'
}


# plt.scatter(*zip(*image), c="r", marker='.')

# This line below is meant to do the same plot as the line above but with colors

# for language A, B, X (unknown language), and Both for both (purple)

# plt.scatter(*zip(*image), c = [color[find_language(i, lang_labels)] for i in words], s = 5)

# for language A, B, and X (unknown language)
# keep in mind that get_word_language.find_language() returns a list, so pick
# one element from the list
plt.scatter(*zip(*image), c = [color[find_language(i, lang_labels)] for i in words], s = 5)


# Plotting randomly labeled languages
# random_dialect_sample = get_random_dialect_sample()
# plt.scatter(*zip(*image), c = [color[get_word_language.find_language(i, random_dialect_sample)] for i in words], s = 5)

# Plotting scribes

# scribe_color = {
# 	1: 'red',
# 	2: 'yellow',
# 	3: 'green',
# 	4: 'blue',
# 	5: "purple",
# 	"More": "white",
# 	'X': "grey"
# }
# scribe_color_data = [scribe_color[find_scribe(i, scribe_labels)] for i in words]
# plt.scatter(*zip(*image), c = scribe_color_data, 
# 			s = 15, 
# 			edgecolors=["black" if color=="white" or color=="grey" else color for color in scribe_color_data], 
# 			linewidths=1, 
# 			alpha=[0.05 if data=="white" or data=="grey" else 1 for data in scribe_color_data])

# Plotting scribes better

# scribe_color = {
# 	True: 0.25,
# 	False: 0
# }
# plt.scatter(*zip(*image), alpha = [scribe_color[did_scribe_write_word(i, scribe_labels, 1)] for i in words], s = 5, c = "red")
# plt.scatter(*zip(*image), alpha = [scribe_color[did_scribe_write_word(i, scribe_labels, 2)] for i in words], s = 5, c = "yellow")
# plt.scatter(*zip(*image), alpha = [scribe_color[did_scribe_write_word(i, scribe_labels, 3)] for i in words], s = 5, c = "green")
# plt.scatter(*zip(*image), alpha = [scribe_color[did_scribe_write_word(i, scribe_labels, 4)] for i in words], s = 5, c = "blue")
# plt.scatter(*zip(*image), alpha = [scribe_color[did_scribe_write_word(i, scribe_labels, 5)] for i in words], s = 5, c = "purple")

visibility = {
	True: 0.25,
	False: 0
}
# plt.scatter(*zip(*image), alpha = [visibility[did_scribe_write_word(i, scribe_labels, 1)] for i in words], s = 5, c = "red")
# plt.scatter(*zip(*image), alpha = [visibility[did_scribe_write_word(i, scribe_labels, 2)] for i in words], s = 5, c = "yellow")
# plt.scatter(*zip(*image), alpha = [visibility[did_scribe_write_word(i, scribe_labels, 3)] for i in words], s = 5, c = "green")
# plt.scatter(*zip(*image), alpha = [visibility[did_scribe_write_word(i, scribe_labels, 4)] for i in words], s = 5, c = "blue")
# plt.scatter(*zip(*image), alpha = [visibility[did_scribe_write_word(i, scribe_labels, 5)] for i in words], s = 5, c = "purple")

# Plotting number of scribes into the tranparency of the dot
# plt.scatter(*zip(*image), alpha = [(get_scribe_count(i, scribe_labels)+1)/6 for i in words], s = 5, c = "black")


# Plotting topic
# topic_color = {
# 	"astro": 'red',
# 	"herbal": 'yellow',
# 	"multiherbal": 'green',
# 	"bath": 'blue',
# 	"text": "purple",
# 	"More": "white",
# 	'X': "grey"
# }
# section_color_data = [topic_color[find_topic(i, section_labels)] for i in words]
# plt.scatter(*zip(*image), c = section_color_data, 
# 			s = 15, 
# 			edgecolors=["black" if color=="white" or color=="grey" else color for color in section_color_data], 
# 			linewidths=1, 
# 			alpha=[0.05 if data=="white" or data=="grey" else 1 for data in section_color_data])


# Plotting topic better
# plt.scatter(*zip(*image), alpha = [visibility[is_word_in_topic(i, section_labels, "astro")] for i in words], s = 5, c = "red")
# plt.scatter(*zip(*image), alpha = [visibility[is_word_in_topic(i, section_labels, "herbal")] for i in words], s = 5, c = "green")
# plt.scatter(*zip(*image), alpha = [visibility[is_word_in_topic(i, section_labels, "multiherbal")] for i in words], s = 5, c = "lime")
# plt.scatter(*zip(*image), alpha = [visibility[is_word_in_topic(i, section_labels, "bath")] for i in words], s = 5, c = "yellow")
# plt.scatter(*zip(*image), alpha = [visibility[is_word_in_topic(i, section_labels, "text")] for i in words], s = 5, c = "black")


# coords = dict(zip(words, image))

# for w in word_dist:
# 	a = coords[w[0]]
# 	b = coords[w[1]]
# 	plt.plot((a[0], b[0]), (a[1], b[1]), alpha=0.3)

# Plotting word count across entire VMS (frequency)

# recall that wc is a global Counter() object from vms_tokenize
# we can already access the words and their counts using this w, v in vms_tokenize format
# we want wc as a dict so we can use it in the plt.scatter statement below
wc_as_dict = {w:v for w, v in vms_tokenize.wc.most_common()}
print(wc_as_dict)
print(type(wc_as_dict))

plt.scatter(*zip(*image), c = [math.log(wc_as_dict[word]) for word in words], s = 5, cmap = 'Blues', linewidths=5)


plt.title('Voynich Word Embeddings')

# annotate(image, words)

plt.show()


#####################################


