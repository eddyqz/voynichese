# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:12:39 2024

@authors: eddyz and chris-yao

The purpose of this code is to check what language (A, B, unlabeled, or both), 
scribe (1 through 5 or multiple),
and topic (astro, herbal, multiherbal, bath, text, or multiple) a word in the VMS is.

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


#####################################
# actual function to find word's language

def find_language(word, lang_labels):
	'''
	

	Parameters
	----------
	word : string
		This is supposed to be a word from the EVA transcription of the VMS.
	lang_labels : dict
		Dictionary where the keys are the folio numbers and the keys are the
		language of the page

	Returns
	-------
	language : string
		This is the "language" the word is written in (A, B, Both, or X) as 
		determined by Currier, where X is unclear.

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

def is_word_in_language(word, lang_labels, lang):
	"""

	Parameters
	----------
	word : string
		This is supposed to be a word from the EVA transcription of the VMS.
	lang_labels : dict
		Dictionary where the keys are the folio numbers and the keys are the
		language of the page
	lang: string
		This is the language.

	Returns
	-------
	lang_bool : boolean
		Returns True if word is in language, otherwise false.
	"""

	for page in word_page_dict[word]:
		if page in lang_labels.keys():
			if lang_labels[page] == lang:
				return True
	return False

def find_scribe(word, scribe_labels):
	'''
	

	Parameters
	----------
	word : string
		This is supposed to be a word from the EVA transcription of the VMS.
	scribe_labels : dict
		Dictionary where the keys are the folio numbers and the keys are which
		scribe wrote the page

	Returns
	-------
	scribe : string
		This is the scribe who wrote the word is written in as 
		determined by Davis.

	'''
	
	scribe_list = []
	
	for page in word_page_dict[word]:
		if page in scribe_labels.keys():
			if scribe_labels[page] not in scribe_list:
				scribe_list.append(scribe_labels[page])
		else:
			if 'X' not in scribe_list:
				scribe_list.append('X')
				
	if len(scribe_list) == 1:
		return scribe_list[0]

	if (len(scribe_list) >=2 and 'X' not in scribe_list) or len(scribe_list) >= 3:
		return "Multiple"
	if 1 in scribe_list:
		return 1
	if 2 in scribe_list:
		return 2
	if 3 in scribe_list:
		return 3
	if 4 in scribe_list:
		return 4
	if 5 in scribe_list:
		return 5
	
def get_scribe_count(word, scribe_labels):
	'''
	

	Parameters
	----------
	word : string
		This is supposed to be a word from the EVA transcription of the VMS.
	scribe_labels : dict
		Dictionary where the keys are the folio numbers and the keys are which
		scribe wrote the page

	Returns
	-------
	scribes : integer
		This is the number of scribe who have written the word as 
		determined by Davis.

	'''
	
	scribe_list = []
	
	for page in word_page_dict[word]:
		if page in scribe_labels.keys():
			if scribe_labels[page] not in scribe_list:
				scribe_list.append(scribe_labels[page])

	return len(scribe_list)



def did_scribe_write_word(word, scribe_labels, scribe_number):
	'''
	

	Parameters
	----------
	word : string
		This is supposed to be a word from the EVA transcription of the VMS.
	scribe_labels : dict
		Dictionary where the keys are the folio numbers and the keys are which
		scribe wrote the page
	scribe_number: integer
		This is the number of the scribe.

	Returns
	-------
	scribe_bool : boolean
		Returns True if scribe has written word, otherwise false.

	'''
		
	for page in word_page_dict[word]:
		if page in scribe_labels.keys():
			if scribe_labels[page] == scribe_number:
				return True
	return False


def find_topic(word, topic_labels):
	'''
	

	Parameters
	----------
	word : string
		This is supposed to be a word from the EVA transcription of the VMS.
	topic_labels : dict
		Dictionary where the keys are the folio numbers and the keys are the topic
		of the page

	Returns
	-------
	topic : string
		This is the topic of the word as 
		determined by Davis.

	'''
	
	topic_list = []
	
	for page in word_page_dict[word]:
		if page in topic_labels.keys():
			if topic_labels[page] not in topic_list:
				topic_list.append(topic_labels[page])
		else:
			if 'X' not in topic_list:
				topic_list.append('X')
				
	if len(topic_list) == 1:
		return topic_list[0]

	if (len(topic_list) >=2 and 'X' not in topic_list) or len(topic_list) >= 3:
		return "multiple"
	if "astro" in topic_list:
		return "astro"
	if "herbal" in topic_list:
		return "herbal"
	if "multiherbal" in topic_list:
		return "multiherbal"
	if "bath" in topic_list:
		return "bath"
	if "text" in topic_list:
		return "text"

def is_word_in_topic(word, topic_labels, topic):
	'''
	

	Parameters
	----------
	word : string
		This is supposed to be a word from the EVA transcription of the VMS.
	topic_labels : dict
		Dictionary where the keys are the folio numbers and the keys are the topic
		of the page
	topic: string
		The topic to test.

	Returns
	-------
	topic_bool : boolean
		Returns True if the word is related to the topic (appears in a page
		labeled as the topic), otherwise false.

	'''
		
	for page in word_page_dict[word]:
		if page in topic_labels.keys():
			if topic_labels[page] == topic:
				return True
	return False

