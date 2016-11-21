import sys
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import re
from os import listdir
from os.path import isfile, join
import cPickle

all_tweets = cPickle.load(open('all_tweets.p','rb'))
all_mixtures = cPickle.load(open('all_mixtures.p','rb'))
files = cPickle.load(open('files.p','rb'))
dictionary = cPickle.load(open('dictionary.p','rb'))

num_topics = 5
def cosine_sim(a,b):
	p = [0]*num_topics
	q = [0]*num_topics
	for i,val in all_mixtures[a[0]][a[1]]:
		p[i] = val
	for i,val in all_mixtures[b[0]][b[1]]:
		q[i] = val
	ans = 0
	for i in xrange(0,num_topics):
		ans += p[i]*q[i]
	return ans

for i in xrange(0)
