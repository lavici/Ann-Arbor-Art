# EECS 486 Assignment 4
# Laura Vicinanza (lavici)

import sys, re, os
from .porterStemmer import *

acronym_and_abbreviation_list = ["i.o.u.", "m.d.", "n.b.", "p.o.", "u.k.", "u.s.", "u.s.a.", "p.s.", "mr.", "mrs.", ".c", ".com", "dr.", ".sh", ".java", "st.", "rd.", "dr."]
# list of contractions
contractions_dict = {'didn\'t': 'did not','don\'t': 'do not', "aren\'t": "are not", "can\'t": "can not", 
"could\'ve": "could have", "couldn\'t": "could not", "didn\'t": "did not", "doesn\'t": "does not",
"don\'t": "do not", "hadn\'t": "had not", "hasn\'t": "has not", "haven\'t": "have not", "he\'d": "he would",
"he\'ll": "he will", "he\'s": "he is", "how\'d": "how did", "how\'ll": "how will", "how'\s": "how is",
"i\'d": "i would", "i\'ll": "i will", "i\'m": "i am", "i\'ve": "i have", "isn\'t": "is not", "it\'d": "it would",
"it\'ll": "it will", "it\'s": "it is", "let\'s": "let us", "might\'ve": "might have", "must\'ve": "must have",
"mustn\'t": "must not", "she\'d": "she would", "she\'ll": "she will", "she\'s": "she is", "should\'ve": "should have",
"shouldn\'t": "should not", "shouldn\'t\'ve": "should not have", "that\'d": "that would", "that\'s": "that is",
"there\'d": "there would", "there\'s": "there is", "they\'d": "they would", "they\'d\'ve": "they would have",
"they\'ll": "they will", "they\'ll\'ve": "they will have", "they\'re": "they are", "they\'ve": "they have",
"wasn\'t": "was not", "we\'d": "we would", "we\'ll": "we will", "we\'re": "we are",	"we\'ve": "we have",
"weren\'t": "were not", "what\'ll": "what will", "what\'re": "what are",
"what\'s": "what is", "what\'ve": "what have", "when\'s": "when is", "when\'ve": "when have", "where\'d": "where did",
"where\'s": "where is", "where\'ve": "where have", "who\'ll": "who will", "who\'ll\'ve": "who will have", "who\'s": "who is",
"who\'ve": "who have", "why\'s": "why is", "why\'ve": "why have", "will\'ve": "will have", "won\'t": "will not",
"would\'ve": "would have", "wouldn\'t": "would not", "wouldn\'t\'ve": "would not have", "y\'all": "you all",
"you\'d": "you would", "you\'d\'ve": "you would have", "you\'ll": "you will", "you\'re": "you are", "you\'ve": "you have" }

def isNumber(str):
	s = re.split('\W+', str)
	for c in s:
		if not c.isdigit():
			return False
	return True

contractions_re = re.compile('(%s)' % '|'.join(contractions_dict.keys()))
def handleContractions(s, contractions_dict=contractions_dict):
	def replace(match):
		return contractions_dict[match.group(0)]
	return contractions_re.sub(replace, s)

# if it's not "special", normal tokenization
def tokenizeText(str):
	str = str.replace('%20', ' ')
	str = str.replace('+', ' ')
	str_list = str.split()
	out_list = []
	for word in str_list:
		word = word.lower()
		# if word is not a number
		if not isNumber(word):
			# tokenization of .
			if word not in acronym_and_abbreviation_list:
				word = word.replace(".", "")
				if word.endswith('.'):
					word = word[:-1]
			# tokenization of '
			word = handleContractions(word)
			# if the size of the list of the string is greater than 1,
			# add the last word to the
			if len(word.split()) > 1:
				out_list.append(word.split()[-1])
				word = word.rsplit(' ', 1)[0]
			# tokenization of - and other characteres
			word = re.sub('[^A-z0-9 . -]', '', word)
		# if a number is the last word in the sentence, remove the period
		if isNumber(word) and word.endswith('.'):
			word = word[:-1]
		if word != '':
			out_list.append(word)
	return out_list

# # removes stopwords from wordList
# def removeStopWords(wordList):
# 	stop_words = {}
# 	with open("/stopwords", "r") as infile:
# 		for line in infile:
# 			# get rid of newline character
# 			line = line.strip()
# 			stop_words[str(line)] = 1
# 	for word in list(wordList):
# 		if word in stop_words:
# 			wordList.remove(word)
# 	return wordList

def stemWords(inList):
	p = PorterStemmer()
	outList = []
	# stem each word in the list 
	for c in inList:
		outList.append(p.stem(c, 0,len(c)-1))
	return outList

