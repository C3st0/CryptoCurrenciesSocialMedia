# nltk.download('stopwords')
import csv

import nltk.classify.util
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize, RegexpTokenizer

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


def read_bitcointweets():
    # return a list (pos, neg, neu )
    pos = [] # create the classes
    neg = []
    neu = []
    with open('../TestData/bitcointweets.csv') as f:
        reader = csv.reader(f) # read the dataset
        for row in reader:  # for every row we take
            text = row[1]   # the review from the first column
            label = row[7]  # and the polarity from the the seventh
            if 'positive' in label:
                pos.append(text)
            elif 'negative' in label:
                neg.append(text)
            else:
                neu.append(text)

    return [pos, neg, neu]


def create_word_features(sentence):
    tokenizer = RegexpTokenizer(r'\w+') # remove punctuation
    words = tokenizer.tokenize(sentence.lower())  # convert all words to lower case
    useful_words = [word for word in words if word not in stopwords.words('english')]
    # expected input from Naive Bayes is that every word is followed by True
    return {word: True for word in useful_words}


# define the model for training and testing
def model_bitcointweets():
    data = read_bitcointweets()

    # print and plot amount of pos,neg and neu rows
    print('POS:', len(data[0]))
    print('NEG:', len(data[1]))
    print('NEU:', len(data[2]))
    plt.figure(figsize=(10, 6.5), dpi=100)
    plt.bar(['POS', 'NEG', 'NEU'], list(map(len, data)))
    for x, y in zip(['POS', 'NEG', 'NEU'], map(len, data)):
        plt.text(x, y, str(y), fontsize='large', color='blue', ha='center')
    plt.tight_layout()
    plt.savefig('hist.png')

    # convert words to features for all polarities
    pos_train_set = []
    for sentence in data[0]:
        words = create_word_features(sentence)
        pos_train_set.append((words, 'positive'))
    neg_train_set = []
    for sentence in data[1]:
        words = create_word_features(sentence)
        neg_train_set.append((words, 'negative'))
    neu_train_set = []
    for sentence in data[2]:
        words = create_word_features(sentence)
        neu_train_set.append((words, 'neutral'))

    accuracies = []

    len_pos = len(pos_train_set)
    len_neg = len(neg_train_set)
    len_neu = len(neu_train_set)

    # split the data in training and testing data with different split ratio
    # each time, starting with 20% training and 80% testing up to 90% training
    # and 10% testing, in steps of 10%
    for x in range(20, 100, 10):
        split_pos = (len_pos * x) // 100
        split_neg = (len_neg * x) // 100
        split_neu = (len_neu * x) // 100

        # split the dataset in training and testing part
        train_set = pos_train_set[:split_pos] + neg_train_set[:split_neg] + neu_train_set[:split_neu]
        test_set = pos_train_set[split_pos:] + neg_train_set[split_neg:] + neu_train_set[split_neu:]
        # create a Naive Bayes classifier and train it with the training dataset
        classifier = NaiveBayesClassifier.train(train_set)
        # test the accuracy using the testing dataset
        accuracy = nltk.classify.util.accuracy(classifier, test_set)
        print('accuracy: ', accuracy, 'split for training:', x)

        accuracies.append(round(accuracy * 100, 2))

    # plot the accuracies
    plt.figure(figsize=(10, 6.5), dpi=100)
    plt.plot(range(20, 100, 10), accuracies)
    plt.xlabel('split ratio (%)')
    plt.ylabel('accuracy (%)')
    plt.tight_layout()
    plt.savefig('accuracies.png')

    # calculate and plot confusion matrix
    test_features = []
    test_labels = []
    for x in test_set:
        test_features.append(x[0])
        test_labels.append(x[1])

    predicted_labels = classifier.classify_many(test_features)

    confmat = confusion_matrix(
        test_labels,
        predicted_labels,
        labels=['positive', 'negative', 'neutral']
    )
    print(confmat)

    fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
    ax.matshow(confmat, cmap=plt.cm.Blues, alpha=0.3)

    for i in range(confmat.shape[0]):
        for j in range(confmat.shape[1]):
            ax.text(
                x=j, y=i, s=confmat[i, j],
                va='center', ha='center', fontsize='x-large'
            )

    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png')

    return classifier


# build helper function to classify a sentence
def classify(classifier, sentence):
    feature = create_word_features(sentence)
    prediction = classifier.classify(feature)

    return prediction
