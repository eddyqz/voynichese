# Based on closest_friend.py from https://github.com/viking-sudo-rm/voynich2vec
# Visualizations at the word level

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
import matplotlib.patches as mpatches


from get_word_characteristics import find_language, find_scribe, \
	did_scribe_write_word, is_word_in_topic, get_scribe_count, \
	is_word_in_language, find_topic

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

# Regular plot
plt.scatter(*zip(*image), c="r", marker='.', alpha=0.25)
plt.title("Voynich Word Embeddings")
plt.savefig("images/words.png")
plt.clf()


# plotting by language
lang_color = {
	'A': 'red',
	'B': 'blue',
	'X': 'grey',
	'Both': 'purple'
}
lang_patches = [mpatches.Patch(color = val, label = key) for key,val in lang_color.items()]
plt.scatter(*zip(*image), c = [lang_color[find_language(i, lang_labels)] for i in words], s = 5)
plt.legend(handles = lang_patches)
plt.title("Distribution of Words by Language")
plt.savefig("images/words_by_lang.png")
plt.clf()


# alternative (better?) plotting for language
lang_visibility = {
	True: 0.25,
	False: 0
}
plt.scatter(*zip(*image), alpha = [lang_visibility[is_word_in_language(i, lang_labels, "A")] for i in words], s = 5, c = "red")
plt.scatter(*zip(*image), alpha = [lang_visibility[is_word_in_language(i, lang_labels, "B")] for i in words], s = 5, c = "blue")
plt.scatter(*zip(*image), alpha = [lang_visibility[is_word_in_language(i, lang_labels, "X")] for i in words], s = 5, c = "grey")
plt.title("Distribution of Words by Language")
plt.legend(["A","B","X"])
plt.savefig('images/words_by_lang_better.png')
plt.clf()


# Plotting randomly labeled languages

# Preliminary graph
random_dialect_sample = get_random_dialect_sample()
plt.scatter(*zip(*image), c = [lang_color[find_language(i, random_dialect_sample)] for i in words], s = 5)
plt.legend(handles = lang_patches)
plt.title("Distribution of Words by Language From a Random Sample")
plt.savefig("images/words_by_lang_random.png")
plt.clf()

plt.scatter(*zip(*image), alpha = [lang_visibility[is_word_in_language(i, random_dialect_sample, "A")] for i in words], s = 5, c = "red")
plt.scatter(*zip(*image), alpha = [lang_visibility[is_word_in_language(i, random_dialect_sample, "B")] for i in words], s = 5, c = "blue")
plt.scatter(*zip(*image), alpha = [lang_visibility[is_word_in_language(i, random_dialect_sample, "X")] for i in words], s = 5, c = "grey")
plt.title("Distribution of Words by Language From a Random Sample")
plt.legend(["A","B","X"])
plt.savefig('images/words_by_lang_random_better.png')
plt.clf()


# Plotting scribes TODO STILL

scribe_color = {
	1: 'red',
	2: 'yellow',
	3: 'green',
	4: 'blue',
	5: "purple",
	"Multiple": "white",
	'X': "grey"
}

# Unique words
scribe_color_data = [scribe_color[find_scribe(i, scribe_labels)] for i in words]
plt.scatter(*zip(*image), c = scribe_color_data, 
			s = 15, 
			edgecolors=["black" if color=="white" or color=="grey" else color for color in scribe_color_data], 
			linewidths=1, 
			alpha=[0.05 if data=="white" or data=="grey" else 1 for data in scribe_color_data])
scribe_patches = [mpatches.Patch(color = val, label = key) for key,val in scribe_color.items()]
plt.legend(handles = scribe_patches)
plt.title("Distribution of Words by Scribe (Unique Words Only)")
plt.savefig("images/words_by_scribe_unique.png")
plt.clf()


# Plotting scribes all 
visibility = {
	True: 0.25,
	False: 0
}
plt.scatter(*zip(*image), alpha = [visibility[did_scribe_write_word(i, scribe_labels, 1)] for i in words], s = 5, c = "red")
plt.scatter(*zip(*image), alpha = [visibility[did_scribe_write_word(i, scribe_labels, 2)] for i in words], s = 5, c = "yellow")
plt.scatter(*zip(*image), alpha = [visibility[did_scribe_write_word(i, scribe_labels, 3)] for i in words], s = 5, c = "green")
plt.scatter(*zip(*image), alpha = [visibility[did_scribe_write_word(i, scribe_labels, 4)] for i in words], s = 5, c = "blue")
plt.scatter(*zip(*image), alpha = [visibility[did_scribe_write_word(i, scribe_labels, 5)] for i in words], s = 5, c = "purple")
plt.legend([1,2,3,4,5])
plt.title("Distribution of Words by Scribe")
plt.savefig("images/words_by_scribe.png")
plt.clf()

# Plotting number of scribes into the tranparency of the dot
plt.scatter(*zip(*image), alpha = [(get_scribe_count(i, scribe_labels)+1)/6 for i in words], s = 5, c = "black")
plt.title("Distribution of Words")
plt.savefig("images/words_by_scribe_number.png")
plt.clf()

# Plotting topic
topic_color = {
	"astro": 'red',
	"herbal": 'yellow',
	"multiherbal": 'green',
	"bath": 'blue',
	"text": "purple",
	"multiple": "white",
	'X': "grey"
}
topic_color_data = [topic_color[find_topic(i, section_labels)] for i in words]
plt.scatter(*zip(*image), c = topic_color_data, 
			s = 15, 
			edgecolors=["black" if color=="white" or color=="grey" else color for color in topic_color_data], 
			linewidths=1, 
			alpha=[0.05 if data=="white" or data=="grey" else 1 for data in topic_color_data])
topic_patches = [mpatches.Patch(color = val, label = key) for key,val in topic_color.items()]
plt.legend(handles = topic_patches)
plt.title("Distribution of Words by Topic (Unique Topics Only)")
plt.savefig("images/words_by_topic_unique.png")
plt.clf()

# Plotting topic better
plt.scatter(*zip(*image), alpha = [visibility[is_word_in_topic(i, section_labels, "astro")] for i in words], s = 5, c = "red")
plt.scatter(*zip(*image), alpha = [visibility[is_word_in_topic(i, section_labels, "herbal")] for i in words], s = 5, c = "yellow")
plt.scatter(*zip(*image), alpha = [visibility[is_word_in_topic(i, section_labels, "multiherbal")] for i in words], s = 5, c = "green")
plt.scatter(*zip(*image), alpha = [visibility[is_word_in_topic(i, section_labels, "bath")] for i in words], s = 5, c = "blue")
plt.scatter(*zip(*image), alpha = [visibility[is_word_in_topic(i, section_labels, "text")] for i in words], s = 5, c = "purple")
plt.legend(["astro", "herbal", "multiherbal", "bath", "text"])
plt.title("Distribution of Words by Topic")
plt.savefig("images/words_by_topic.png")
plt.show()



#####################################