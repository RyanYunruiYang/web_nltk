#The only important functions are imaging() and naive_comparison(), they are used in run.py
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize

from nltk.probability import FreqDist
import matplotlib.pyplot as plt

from wordcloud import WordCloud

import numpy as np
import math
from PIL import Image, ImageDraw

from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer


text = "."

def init():
	global text
	text_file = open("scitext.txt")

	text = text_file.read()

	sentences = sent_tokenize(text)
	words = word_tokenize(text)

	# tagged_words = []
	# for w in words:
	# 	tagged_words.append(nltk.pos_tag(words))
	# print(tagged_words)


	words_no_punc = []

	for w in words:
		if w.isalpha():
			words_no_punc.append(w.lower())
	# print(words_no_punc,end='\n\n')
	# print(words_no_punc)

	# fdist = FreqDist(words_no_punc)

	# print(fdist.most_common(10))
	# fdist.plot(10)


	from nltk.corpus import stopwords

	stopwords = stopwords.words("english")
	#stopwords are stuff like i, me, my, myself, etc.

	clean_words = []
	dirty_words = []

	for w in words_no_punc:
		if w not in stopwords:
			clean_words.append(w)
		else:
			dirty_words.append(w)

	#print(clean_words,end='\n\n')

	fdist = FreqDist(clean_words)

	#####print(fdist.most_common(10))

#---------------------------------------
#---------------------------------------


def imaging(text_string):#This creates a wordcloud in the shape of a circle to wordcloud.png
	try:
		char_mask = np.array(Image.open("/Users/ryanyang/java2020/cs550/web_nltk/public/circle_web.png"))

		wordcloud = WordCloud(background_color="black", mask=char_mask).generate(text_string)

		plt.figure(figsize = (8,8))
		plt.imshow(wordcloud)

		plt.axis("off")
		plt.savefig("/Users/ryanyang/java2020/cs550/web_nltk/public/worldcloud.png")
	except:
		print("oh no")

#---------------------------------------
#---------------------------------------
def word_comparison():
	from nltk.stem import PorterStemmer

	porter = PorterStemmer()
	#print(porter.stem("Studying"))

	#Synsets
	# for word in wordnet.synsets("Fun"):
	# 	print(word.name())
	# 	print(word.definition())
	# 	print(word.examples())

	# 	for lemma in word.lemmas():
	# 		print(lemma)
	# 	print("\n")

	#hypernym, more abstract
	word = wordnet.synsets("Play")[0]
	print(word.hypernyms())
	print(word.hyponyms())
	print(word.lemmas()[0].name())

	synonyms = []
	antonyms = []
	for words in wordnet.synsets("Fun"):
		for lemma in words.lemmas():
			synonyms.append(lemma.name())
			if lemma.antonyms():
				antonyms.append(lemma.antonyms()[0].name())
	print(synonyms)
	print(antonyms)

	word1 = wordnet.synsets("ship","n")[0]
	word2 = wordnet.synsets("boat","n")[0]
	print(word1.wup_similarity(word2))



def naive_comparison(sentence1, sentence2):#This uses tf-idf to calculate word similarity, I explain this on the website itself as well
	sentences = [sentence1, sentence2]

	vectorizer = TfidfVectorizer(norm = None)

	X=vectorizer.fit_transform(sentences).toarray()

	#print(vectorizer.vocabulary_)
	#print(vectorizer.get_feature_names())
	
	sum_idf = 0
	for elem in X:
		for number in elem:
			sum_idf += number
	k=X.size//2
	print(X)
	print(k)
	dp = 0
	size1 = 0
	size2 = 0

	for i in range(k):
		dp += X[0][i]*X[1][i]
		size1 += X[0][i]**2
		size2 += X[1][i]**2

	return dp/math.sqrt(size1*size2)

def main():
	#word_comparison()
	#init()
	print(naive_comparison("oh la la", "the la la pog"))

if __name__ == "__main__":
	main()









