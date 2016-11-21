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
from heapq import heappush, heappop

all_tweets = cPickle.load(open('all_tweets.p','rb'))
all_mixtures = cPickle.load(open('all_mixtures.p','rb'))
files = cPickle.load(open('files.p','rb'))
dictionary = cPickle.load(open('dictionary.p','rb'))

num_topics = 5

#tuple of indices of tweets passed as arguements
def cosine_sim(a,b):
	global all_tweets
	global all_mixtures
	global files
	global dictionary
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


cum_accuracy = 0.0
num_test = 0.0

for i in xrange(0,len(all_tweets)):
	for j in xrange(int(0.8*len(all_tweets[i]))+1, len(all_tweets[i])):
		heap = []
		num_test+=1
		for k in xrange(0,len(all_tweets)):
			for l in xrange(0,int(0.8*len(all_tweets[k]))):
				heappush(heap,(0-cosine_sim((i,j),(k,l)),(k,l)))
		#retrieve indices of max 10 heaps by negating
		accuracy = 0
		for m in xrange(0,10):
			a = heappop(heap)
			retreived_i = a[1][0]
			retreived_j = a[1][1]
			if i==retreived_i:
				accuracy+=1
		# print accuracy
		cum_accuracy+=accuracy
	print i

cum_accuracy = cum_accuracy/num_test
print cum_accuracy