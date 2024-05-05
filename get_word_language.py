# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:12:39 2024

@author: eddyz

The purpose of this code is to check what language (A, B, or unlabeled) a word
in the VMS is. 

Note on how to use this file:
	Import this file into the file where you actually need the language of a word.
	Then, simply use get_word_language.find_language(word) and plug in the word 
	you want to find the language for.
"""

#####################################
# constants and data needed to run code

FILE = "text16e6.evt"

#####################################
# helper function

# everything below was lifted from vms_tokenize.py

from collections import Counter
import re, io

wc = Counter()

from vms_tokenize import get_words


#####################################
# main

# since this loop in main is where we actually iterate over get_words(),
# I have to create the dictionary of {word:[pages]} here so I'm not 
# creating an entirely new dictionary each time get_words() executes
# unfortunately, I have to make the dictionary a global variable to do this

		
word_page_dict = {}

for line in get_words(FILE, page_numbers=True):
		#print " ".join(line)
		
		# for every word in a line of the VMS
		for word in line[1:len(line)]:
# 			print(word)
			# if the word has already been seen
			if word in word_page_dict.keys():
				# check if it has appeared on an existing page or not
				# If it is being seen on a new page for the first time,
				# add that page to the list. 
				# otherwise, do nothing (we don't want duplicate pages)
				if line[0] not in word_page_dict[word]:
					word_page_dict[word].append(line[0])
			# if word has not already been seen
			else: 
				word_page_dict[word] = [line[0]]
		
		
		pass

# print(word_page_dict)


#####################################
# actual function to find word's language

def find_language(word, lang_labels):
	'''
	

	Parameters
	----------
	word : string
		This is supposed to be a word from the EVA transcription of the VMS.

	Returns
	-------
	language : string
		This is the "language" the word is written in (A, B, or unclear) as 
		determined by Currier.

	'''
	
	language = ''
	language_list = []
	
	for page in word_page_dict[word]:
		if page in lang_labels.keys():
			if lang_labels[page] not in language_list:
				language_list.append(lang_labels[page])
		else:
			if 'X' not in language_list:
				language_list.append('X')
				
	if len(language_list) == 1:
		language = language_list[0]
	else:
		if 'A' in language_list and 'B' in language_list:
			language = 'Both'
		elif 'A' in language_list:
			language = 'A'
		elif 'B' in language_list:
			language= 'B'
	
	return language

	
	



