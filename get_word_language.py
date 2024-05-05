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

lang_labels = {
	'f1r': 'A',
	'f1v': 'A',
	'f2r': 'A',
	'f2v': 'A',
	'f3r': 'A',
	'f3v': 'A',
	'f4r': 'A',
	'f4v': 'A',
	'f5r': 'A',
	'f5v': 'A',
	'f6r': 'A',
	'f6v': 'A',
	'f7r': 'A',
	'f7v': 'A',
	'f8r': 'A',
	'f8v': 'A',
	'f9r': 'A',
	'f9v': 'A',
	'f10r': 'A',
	'f10v': 'A',
	'f11r': 'A',
	'f11v': 'A',
	'f13r': 'A',
	'f13v': 'A',
	'f14r': 'A',
	'f14v': 'A',
	'f15r': 'A',
	'f15v': 'A',
	'f16r': 'A',
	'f16v': 'A',
	'f17r': 'A',
	'f17v': 'A',
	'f18r': 'A',
	'f18v': 'A',
	'f19r': 'A',
	'f19v': 'A',
	'f20r': 'A',
	'f20v': 'A',
	'f21r': 'A',
	'f21v': 'A',
	'f22r': 'A',
	'f22v': 'A',
	'f23r': 'A',
	'f23v': 'A',
	'f24r': 'A',
	'f24v': 'A',
	'f25r': 'A',
	'f25v': 'A',
	'f26r': 'B',
	'f26v': 'B',
	'f27r': 'A',
	'f27v': 'A',
	'f28r': 'A',
	'f28v': 'A',
	'f29r': 'A',
	'f29v': 'A',
	'f30r': 'A',
	'f30v': 'A',
	'f31r': 'B',
	'f31v': 'B',
	'f32r': 'A',
	'f32v': 'A',
	'f33r': 'B',
	'f33v': 'B',
	'f34r': 'B',
	'f34v': 'B',
	'f35r': 'A',
	'f35v': 'A',
	'f36r': 'A',
	'f36v': 'A',
	'f37r': 'A',
	'f37v': 'A',
	'f38r': 'A',
	'f38v': 'A',
	'f39r': 'B',
	'f39v': 'B',
	'f40r': 'B',
	'f40v': 'B',
	'f41r': 'B',
	'f41v': 'B',
	'f42r': 'A',
	'f42v': 'A',
	'f43r': 'B',
	'f43v': 'B',
	'f44r': 'A',
	'f44v': 'A',
	'f45r': 'A',
	'f45v': 'A',
	'f46r': 'B',
	'f46v': 'B',
	'f47r': 'A',
	'f47v': 'A',
	'f48r': 'B',
	'f48v': 'B',
	'f49r': 'A',
	'f49v': 'A',
	'f50r': 'B',
	'f50v': 'B',
	'f51r': 'A',
	'f51v': 'A',
	'f52r': 'A',
	'f52v': 'A',
	'f53r': 'A',
	'f53v': 'A',
	'f54r': 'A',
	'f54v': 'A',
	'f55r': 'B',
	'f55v': 'B',
	'f56r': 'A',
	'f56v': 'A',
	'f57r': 'B',
	'f58r': 'A',
	'f58v': 'A',
	'f66r': 'B',
	'f66v': 'B',
	'f75r': 'B',
	'f75v': 'B',
	'f76r': 'B',
	'f76v': 'B',
	'f77r': 'B',
	'f77v': 'B',
	'f78r': 'B',
	'f78v': 'B',
	'f79r': 'B',
	'f79v': 'B',
	'f80r': 'B',
	'f80v': 'B',
	'f81r': 'B',
	'f81v': 'B',
	'f82r': 'B',
	'f82v': 'B',
	'f83r': 'B',
	'f83v': 'B',
	'f84r': 'B',
	'f84v': 'B',
	'f85r1': 'B',
	'f85r2': 'B',
	'f86v4': 'B',
	'f86v6': 'B',
	'f85v2': 'B',
	'f86v5': 'B',
	'f86v3': 'B',
	'f87r': 'A',
	'f87v': 'A',
	'f88r': 'A',
	'f88v': 'A',
	'f89r1': 'A',
	'f89r2': 'A',
	'f89v2': 'A',
	'f89v1': 'A',
	'f90r1': 'A',
	'f90r2': 'A',
	'f90v2': 'A',
	'f90v1': 'A',
	'f93r': 'A',
	'f93v': 'A',
	'f94r': 'B',
	'f94v': 'B',
	'f95r1': 'B',
	'f95r2': 'B',
	'f95v2': 'B',
	'f95v1': 'B',
	'f96r': 'A',
	'f96v': 'A',
	'f99r': 'A',
	'f99v': 'A',
	'f100r': 'A',
	'f100v': 'A',
	'f101r1': 'A',
	'f101v2': 'A',
	'f101v1': 'A',
	'f102r1': 'A',
	'f102r2': 'A',
	'f102v2': 'A',
	'f102v1': 'A',
	'f103r': 'B',
	'f103v': 'B',
	'f104r': 'B',
	'f104v': 'B',
	'f105r': 'B',
	'f105v': 'B',
	'f106r': 'B',
	'f106v': 'B',
	'f107r': 'B',
	'f107v': 'B',
	'f108r': 'B',
	'f108v': 'B',
	'f111r': 'B',
	'f111v': 'B',
	'f112r': 'B',
	'f112v': 'B',
	'f113r': 'B',
	'f113v': 'B',
	'f114r': 'B',
	'f114v': 'B',
	'f115r': 'B',
	'f115v': 'B',
	'f116r': 'B',
}


#####################################
# helper function

# everything below was lifted from vms_tokenize.py

from collections import Counter
import re, io

wc = Counter()

def get_words(file, page_numbers=False):
	global wc
	with io.open(file, 'r', encoding="latin_1") as file:
		for line in file.read().splitlines():
			# pull out page numbers
			# if page_numbers:
			# 	m = re.match(r'^<(f\d+[rv].?)>', line)

			# 	if m:
			# 		pg = str(m.group(1))
			# 		yield ['#', pg]

			# pull out takahashi lines
			m = re.match(r'^<(f.*?)\..*;H> +(\S.*)$', line)
			if not m:
				continue

			transcription = m.group(2)
			pg = str(m.group(1))

			# ignore entire line if it has a {&NNN} or {&.} code
			if re.search(r'\{&(\d|\.)+\}', transcription):
				continue

			# remove extraneous chracters ! and %
			s = transcription.replace("!", "").replace("%", "")

			# delete all end of line {comments} (between one and three observed)
			# ...with optional line terminator
			# allow 0 occurences to remove end-of-line markers (- or =)
			s = re.sub(r'([-=]?\{[^\{\}]+?\}){0,3}[-=]?\s*$', "", s)

			# delete start of line {comments} (single or double)
			s = re.sub(r'^(\{[^\{\}]+?\}){1,2}', "", s)

			# these tags are word breaks
			# breaks = [r'plant', r'figure', r'gap', r'root', r'hole', r'spray',
			# 		  r'gal', r'sync gap', r'diagram', r'star', r'blot\??', r'stem',
			# 		  r'stitched slit', r'stream', r'top of diagram', r'wide gap',
			# 		  r'\|\|', r'fold', r'crease']
			# s = re.sub(r'[-=]\{(' + r'|'.join(breaks) + r')\}', ".", s)

			# simplification: tags preceeded by -= are word breaks
			s = re.sub(r'[-=]\{[^\{\}]+?\}', '.', s)

			# these tags are nulls
			# plant is a null in one case where it is just {plant}
			# otherwise (above) it is a word break
			# s = re.sub(r'\{(fold|crease|blot|&\w.?|plant)\}', "", s)
			# simplification: remaining tags in curly brackets
			s = re.sub(r'\{[^\{\}]+?\}', '', s)

			# special case .{\} is still a word break
			s = re.sub(r'\.\{\\\}', ".", s)

			# split on word boundaries
			# exclude null words ('')
			words = [str(w) for w in s.split(".") if w]

			wc.update(w for w in words)

			if page_numbers:
				r = [pg]
				r.extend(words)
				
				# so basically what happens here is that r is a list that contains 
				# information for a single line of the VMS
				# the first element of r is always the page number, like f116r for example
				# the reason they use yield here is because each time this function
				# is called, it only produces one line of text at a time. 
				# Thus, you need to iterate over the function to get every single 
				# line out. 
				# See vms_tokenize.py for the original source of this code
				yield r
# 				print(r)
			else:
				yield words

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

print(word_page_dict)

#####################################
# actual function to find word's language

def find_language(word):
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


#####################################
# testing code
print(find_language('xoiin'))
	
	



