#!/usr/bin/env python
# get document vectors & plot
#
# variety of schemes to constuct document vectors: can use counts or tfidf,
# and can use word vectors or one-hot vectors

# Based on the file doc_vectors.py in https://github.com/viking-sudo-rm/voynich2vec
# Visualizations at the page/folio level 

import vms_tokenize
from collections import Counter, defaultdict, OrderedDict
from math import log, acos

import numpy as np
import numpy.linalg as npla
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import fasttext

from section_labels import *
from lang_labels import *
from scribe_labels import *
from random_sample import get_random_dialect_sample

def term_freq(term, page):
	# raw count
	# return term_counts[page][term]

	# normalize by page length
	#return float(term_counts[page][term]) / sum(term_counts[page].values())

	# normalize by most common word
	return float(term_counts[page][term]) / max(term_counts[page].values())

def inv_doc_freq(term):
	return log(float(len(pages)) / len(doc_counts[term]))

def tfidf(term, page):
	return term_freq(term, page) * inv_doc_freq(term)


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

path = "models/voynich.bin"
model = fasttext.load_model(path)

term_counts = defaultdict(Counter)
doc_counts = defaultdict(set)

# really this should be a set, but we want ordering
pages = OrderedDict()

# load words
for line in vms_tokenize.get_words("text16e6.evt", page_numbers=True):
	pg = line.pop(0)
	pages[pg] = True

	term_counts[pg].update(line)
	for word in line:
		doc_counts[word].add(pg)

embedded = OrderedDict()

# count terms on page
doc_vectors = []
for p in pages:
	v = np.zeros(100)
	total_tfidf = 0
	for w in set(term_counts[p]):
		if w in model:
			ti = tfidf(w, p)
			v = np.add(v, np.multiply(ti, model[w]))

			total_tfidf += ti

	# normalize
	doc_vectors.append(np.divide(v, total_tfidf))


pagelist = list(pages)
vectors = np.array(doc_vectors)

mag = npla.norm(vectors, axis=1)[:,None] * npla.norm(vectors, axis=1)

sims = np.divide(np.dot(vectors, vectors.T), mag)
sims = np.tril(sims, -1) # don't align to self and remove dups
indices = np.flip(np.argsort(sims, axis=1), axis=1)[:,:5]

doc_dist = []
for i, p in enumerate(pagelist):
	L = [(p, pagelist[j], acos(sims[i, j])) for j in indices[i, :]]
	doc_dist.extend(L)
	# print w
	# for _, match, dist in L:
	# 	print "\t", match, "\t", dist

doc_dist.sort(key = lambda x: x[2])

# for p in doc_dist:
# 	print p[0], "\t", p[1], "\t", p[2]

tsne = TSNE(n_components=2, metric="cosine", random_state=2)
image = tsne.fit_transform(vectors)

# annotate(image, pages)

# Plotting by topic
topic_color = {
	'astro': 'red',
	'herbal': 'green',
	'multiherbal': 'lime',
	'bath': 'cyan',
	'text': 'grey'
}
plt.scatter(*zip(*image), c = [topic_color[section_labels.get(i, 'X')] for i in pages])
topic_patches = [mpatches.Patch(color = val, label = key) for key,val in topic_color.items()]
plt.legend(handles = topic_patches)
plt.title("Distribution of Folios by Topic")
plt.savefig("images/folios_by_topic.png")
plt.clf()



# Plotting by language
lang_color = {
	'A': 'red',
	'B': 'blue',
	'X': 'grey'
}
plt.scatter(*zip(*image), c = [lang_color[lang_labels.get(i, 'X')] for i in pages])
lang_patches = [mpatches.Patch(color = val, label = key) for key,val in lang_color.items()]
plt.legend(handles = lang_patches)
plt.title("Distribution of Folios by Language")
plt.savefig("images/folios_by_lang.png")
plt.clf()


# Comparing this to a random sample of language labels
random_dialect_sample = get_random_dialect_sample()

plt.scatter(*zip(*image), c = [lang_color[random_dialect_sample.get(i, 'X')] for i in pages])
plt.legend(handles = lang_patches)
plt.title("Distribution of Folios by Language From a Random Sample")
plt.savefig("images/folios_by_lang_random.png")
plt.clf()


scribe_color = {
	1: 'red',
	2: 'yellow',
	3: 'green',
	4: 'blue',
	5: 'purple',
	"X": "grey"
}
plt.scatter(*zip(*image), c = [scribe_color[scribe_labels.get(i, 'X')] for i in pages])
scribe_patches = [mpatches.Patch(color = val, label = key) for key,val in scribe_color.items()]
plt.legend(handles = scribe_patches)
plt.title("Distribution of Folios by Scribe")
plt.savefig("images/folios_by_scribe.png")

plt.show()

