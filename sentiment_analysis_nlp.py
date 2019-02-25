# nltk.download('stopwords')
import csv

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer

def read_twitter2():
    # return a pair (pos, neg)
    pos = []
    neg = []
    #ensure that the file closes even with an error
    with open('TestData/twitter2.csv') as f:
        #we don't need first two lines
        next(f)
        next(f)
        reader = csv.reader(f)
        for row in reader:
            label = row[0]
            text = row[4]
            if label == 'POS':
                pos.append(text)
            elif label == 'NEG':
                neg.append(text)

    return [pos, neg]

def read_bitcointweets():
    # return a pair (pos, neg)
    pos = []
    neg = []
    with open('TestData/bitcointweets.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            text = row[1]
            label = row[7]
            if 'positive' in label:
                pos.append(text)
            elif 'negative' in label:
                neg.append(text)

    return [pos, neg]


def create_word_features(sentence):
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(sentence.lower())
    useful_words = [word for word in words if word not in stopwords.words("english")]
    return {word: True for word in useful_words}


def model_twitter2():
    data = read_twitter2()
    pos_train_set = []
    for sentence in data[0]:
        words = create_word_features(sentence)
        pos_train_set.append((words, 'positive'))
    neg_train_set = []
    for sentence in data[1]:
        words = create_word_features(sentence)
        neg_train_set.append((words, 'negative'))

    train_set = pos_train_set[:20] + neg_train_set[:20]
    test_set = pos_train_set[20:] + neg_train_set[20:]

    classifier = NaiveBayesClassifier.train(train_set)
    accuracy = nltk.classify.util.accuracy(classifier, test_set)
    print('accuracy: ', accuracy)

    return classifier



def model_bitcointweets():
    data = read_bitcointweets()
    pos_train_set = []
    for sentence in data[0]:
        words = create_word_features(sentence)
        pos_train_set.append((words, 'positive'))
    neg_train_set = []
    for sentence in data[1]:
        words = create_word_features(sentence)
        neg_train_set.append((words, 'negative'))

    train_set = pos_train_set[:20000] + neg_train_set[:5000]
    test_set = pos_train_set[20000:] + neg_train_set[5000:]

    classifier = NaiveBayesClassifier.train(train_set)
    accuracy = nltk.classify.util.accuracy(classifier, test_set)
    print('accuracy: ', accuracy)

    return classifier


def classify(classifier, sentence):
    feature = create_word_features(sentence)
    prediction = classifier.classify(feature)

    return prediction
