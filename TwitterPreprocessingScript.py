import csv
import nltk
import re
import codecs
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
import enchant
import pandas as pd

readfile = "D:\\LearningDevelopmentProject\\PreprocessedData\\TwitterData1.csv"
outputFile = "D:\\LearningDevelopmentProject\\PreprocessedData\\TwitterData_Processed.csv"

listTweets = []
listUsers = []
with open(readfile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

   
    for row in csv_reader:

        if line_count == 0 or (row[3] in listTweets and row[1] in listUsers):
            
            line_count += 1 
        else:

           
            listTweets.append(row[3])
            listUsers.append(row[1])

            tweetsStemmed = []
            tweetsLemmanized = []
            #======================================================================================================================================================================
            #                                                 CONVERT TO LOWERCASE,REMOVED WHITESPACES,  REMOVED PUNCTUATIONS
            #======================================================================================================================================================================

            #lower
            tweets = row[3].lower()

            

            #Punctuations
            no_punctStr = ""

            for char in tweets:
               if char not in punctuations:
                   no_punctStr = no_punctStr + char
            
            #Whitespaces
            tweets = no_punctStr.strip()

            #========================================================================================================================================================================


            #======================================================================================================================================================================
            #                                     SPELL CHECKER ( not very efficient, because have to  manually add words which are not in library )
            #======================================================================================================================================================================
            
            
            spell = SpellChecker()

            tweetsTokens = word_tokenize(tweets)

            
            spell.word_frequency.load_words(['bitcoin', 'paypal', 'btc', 'ether'])

            misspelled = spell.unknown(tweetsTokens)

            new_words = [word for word in tweetsTokens if word not in misspelled]

            finalTweet = ' '.join(str(e) for e in new_words)

               
            
            #========================================================================================================================================================================


            #======================================================================================================================================================================
            #                                     ENGLISH WORDS LIBRARY ( not very efficient )
            #======================================================================================================================================================================

            #d = enchant.Dict("en_US")

            #english_words = []

            #for word in tweets.split():

            #    if d.check(word):
            #        english_words.append(word)

            #print(" ".join(english_words))
            
            #========================================================================================================================================================================

            #======================================================================================================================================================================
            #        REMOVED  ENGLISH  STOP  WORDS   
            #======================================================================================================================================================================
         
            stop_words = set(stopwords.words('english'))
            tweetsTokens = word_tokenize(finalTweet)
            tweetsRes = [i for i in tweetsTokens if not i in stop_words]

            #==========================================================================================================================================================================================
            #                                               STEMMING  AND   LEMMATIZATION   (Text Normalization)
            #                                               ----------------------------------------------------
            #==========================================================================================================================================================================================
            #          
            # STEMMING: Reducing inflection in words to their root forms.  I've used Porter Stemmer Algorithm which uses Suffix Stripping (e.g "cats" -> "cat", "trouble,troubling,troubled" -> "trouble"
            #           "Connect,Connected,Connections,Connecting" -> "Connect", "Friend,Friends" -> "Friend", "Friendships" -> "Friendship")
            #
            #LEMMATIZATION: Unlike Stemming, Lemmatization reduces inflected words properly ensuring root word belong to language.  Root word is called LEMMA.  (e.g "Playing" -> "Play", "Swimming" -> "Swim"
            #               "Runnning" -> "Run"
            #===========================================================================================================================================================================================
            
            #stemmer= PorterStemmer()
            #for word in tweetsRes:
            #    tweetsStemmed.append(stemmer.stem(word))

            #finalTweetStemmed = ' '.join(str(e) for e in tweetsStemmed)

            #Lemmatization
            lemmatizer = WordNetLemmatizer()
            
            

            for word in tweetsRes:
               tweetsLemmanized.append(lemmatizer.lemmatize(word))

            finalTweetLemmatized = ' '.join(str(e) for e in tweetsLemmanized)

            #========================================================================================================================================================================
           


          
           
            
            #Remove Small words
            shortword = re.compile(r'\W*\b\w{1,3}\b')
            tweets = shortword.sub('', tweets)



            #========================================================================================================================================================
            # Lookup dictionary 
            #========================================================================================================================================================
            lookup_dict = {'rt':'Retweet', 'dm':'direct message', 'awsm' : 'awesome', 'luv' :'love'}
            def _lookup_words(input_text):
                words = input_text.split() 
                new_words = [] 
                new_text = ""
                for word in words:
                    if word.lower() in lookup_dict:
                        word = lookup_dict[word.lower()]
                    new_words.append(word) 
                    new_text = " ".join(new_words) 
                return new_text

            finalTweet = _lookup_words(finalTweetLemmatized)   

            #========================================================================================================
             


            #from nltk.collocations import BigramCollocationFinder

            #bigrams = nltk.collocations.BigramAssocMeasures()
            #trigrams = nltk.collocations.TrigramAssocMeasures()
            #bigramFinder =
            #nltk.collocations.BigramCollocationFinder.from_words(tweetsTokens)
            #trigramFinder =
            #nltk.collocations.TrigramCollocationFinder.from_words(tweetsTokens)


            ##bigrams
            #bigram_freq = bigramFinder.ngram_fd.items()
            #bigramFreqTable = pd.DataFrame(list(bigram_freq),
            #columns=['bigram','freq']).sort_values(by='freq', ascending=False)
            #bigramFreqTable.to_csv('D:\\LearningDevelopmentProject\\PreprocessedData\\TwitterData_Test03.csv')

            
            #=========================================WRITING DATA TO CSV FILE==================================================
             
            rowWrite = [row[0], row[1], row[2], finalTweet]

            with open(outputFile, 'a', newline="") as csvFile:
                writer = csv.writer(csvFile,delimiter=",")
                writer.writerow(rowWrite)
            csvFile.close()

            #===================================================================================================================
            line_count += 1
