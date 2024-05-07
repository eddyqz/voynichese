"""
Created on Sat May 5 2024

@author: chris-yao

Create a random sample of folios in the VMS with proportion equal to that of 
dialect A of the VMS, as determined by Currier.

"""

import random
from lang_labels import *

def get_random_dialect_sample():
    """
    Output: A dictionary where the keys are the folio numbers, e.g., f13v,
    and the values are randomly chosen to be "A" or "B" with the correct proportion.
    Only pages that have originally been labeled A or B can be randomly selected
    by this function.
    """
    A_sum = sum([label=="A" for label in lang_labels.values()])
    random_sample = {label: "B" for label in lang_labels.keys()}
    random.seed(1729) #change seed if you want another random sample
    random_folios = random.sample(list(lang_labels.keys()), A_sum)
    for folio in random_folios:
        random_sample[folio] = "A"
    
    return random_sample

