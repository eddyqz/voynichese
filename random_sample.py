#!/usr/bin/env python
# get document vectors & plot
#
# variety of schemes to constuct document vectors: can use counts or tfidf,
# and can use word vectors or one-hot vectors

import random
from lang_labels import *

def get_random_dialect_sample():
    A_sum = sum([label=="A" for label in lang_labels.values()])
    random_sample = {label: "B" for label in lang_labels.keys()}
    random.seed(1729) #change seed if you want another random sample
    random_folios = random.sample(list(lang_labels.keys()), A_sum)
    for folio in random_folios:
        random_sample[folio] = "A"
    
    return random_sample

