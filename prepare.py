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
def process(text):
    
    text1 = re.sub('[^a-zA-Z ]', ' ', text)
    text1 = text1.lower()

    return text1

def stop_words_list():
    '''
        A stop list specific to the observed timelines composed of noisy words
        This list would change for different set of timelines
    '''
    return ['amp','get','got','hey','hmm','hoo','hop','iep','let','ooo','par',
            'pdt','pln','pst','wha','yep','yer','aest','didn','nzdt','via',
            'one','com','new','like','great','make','top','awesome','best',
            'good','wow','yes','say','yay','would','thanks','thank','going',
            'new','use','should','could','really','see','want','nice',
            'while','know','free','today','day','always','last','put','live',
            'week','went','wasn','was','used','ugh','try','kind','https','http','much',
            'need', 'next','app','ibm','appleevent','using', 'will', 'can']

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en') + stop_words_list()

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

def mytokenize(doc):
    global tokenizer
    global en_stop
    global p_stemmer

    tokens = tokenizer.tokenize(doc)
    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if len(i) > 2 and (i not in en_stop)]

    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    # add tokens to list
    return stemmed_tokens



mypath = "./"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
files = []
for i in onlyfiles:
    if ".csv" in i :
        files.append(i)

cPickle.dump(files,open('files.p','wb'))
doc_set = []
all_tweets = []
for myfile in files:
    doc = ""
    tweets = []
    with open(myfile,'r') as f:
        f.readline()
        for line in f.readlines():
            try:
                indices = [i for i, ltr in enumerate(line) if ltr == ',']
                indices2 = [i for i, ltr in enumerate(line) if ltr == '[']
                if len(indices2 )== 0:
                    text = line[indices[1]:]
                else:
                    text = line[indices[1]:indices2[0]  ]
                tweet = process(text)
                doc += tweet + " "
                tweets.append(tweet)
            except:
                pass
        if len(doc)>0:
            doc_set.append(doc)
            all_tweets.append(tweets)
        print myfile + " done"
cPickle.dump(all_tweets,open('all_tweets.p','wb'))
texts,texts1 = [],[]
# print doc_set
# loop through document list
for doc in doc_set:
    texts1.append(mytokenize(doc))

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts1)
cPickle.dump(dictionary,open('dictionary.p','wb'))

for tweets in all_tweets:
    doc = " ".join(tweets[0:int(len(tweets)*0.8)])
    texts.append(mytokenize(doc))

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]


# Initialize Parameters
lda_filename    = 'kb.lda'
lda_params      = {'num_topics': 5, 'passes': 20, 'alpha': 0.001}

print("Running LDA with: %s  " % lda_params)
lda = gensim.models.ldamodel.LdaModel(corpus, id2word=dictionary,
                        num_topics=lda_params['num_topics'],
                        passes=lda_params['passes'],
                        alpha = lda_params['alpha'])

print "print_topics"
print(lda.print_topics(num_topics=lda_params['num_topics'], num_words=10))
lda.save(lda_filename)
print("lda saved in %s " % lda_filename)
# lda = models.LdaModel.load("kb.lda")

all_mixtures = []
for tweets in all_tweets:
    all_mixtures.append([lda[dictionary.doc2bow(mytokenize(tweet))] for tweet in tweets])

cPickle.dump(all_mixtures,open('all_mixtures.p','wb'))