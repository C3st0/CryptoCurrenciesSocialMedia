# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 21:48:35 2019

@author: Christophe Cestonaro
"""


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
#import enchant
import pandas as pd

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
            
readfile = "E:\\__Brunel\\_Project learning development\\TestData\\bitcointweets.csv"
outputFile = "E:\\__Brunel\\_Project learning development\\TestData\\bitcointweetsCleaned.csv"

#ColUser= 
ColDate = 0
ColTweet = 1
ColLabel = 2


listUsers = []
translator = str.maketrans('', '', string.punctuation)
spell.word_frequency.load_words(['bitcoin', 'paypal', 'btc', 'ether'])
stop_words = set(stopwords.words('english'))

with open(readfile, encoding='utf-8') as csv_file:
    with open(outputFile, 'a', newline="") as csvFile:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    
        spell = SpellChecker()
        lemmatizer = WordNetLemmatizer()
       
        for row in csv_reader:
    
            if line_count == 0 :
                
                line_count += 1 
            else:
    
                tweetsStemmed = []
                tweetsLemmanized = []
                #======================================================================================================================================================================
                #                                                 CONVERT TO LOWERCASE,REMOVED WHITESPACES,  REMOVED PUNCTUATIONS
                #======================================================================================================================================================================
    
                #lower
                tweets = row[ColTweet].lower()
    
                #Punctuations
     
                #Whitespaces
                tweets = tweets.translate(translator)
    
                #========================================================================================================================================================================
    
    
                #======================================================================================================================================================================
                #                                     SPELL CHECKER ( not very efficient, because have to  manually add words which are not in library )
                #======================================================================================================================================================================
                
                tweetsTokens = word_tokenize(tweets)
    
                misspelled = spell.unknown(tweetsTokens)
    
                new_words = [word for word in tweetsTokens if word not in misspelled]
    
                finalTweet = ' '.join(str(e) for e in new_words)
    
                #======================================================================================================================================================================
                #        REMOVED  ENGLISH  STOP  WORDS   
                #======================================================================================================================================================================
             
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
    
                finalTweet = _lookup_words(finalTweetLemmatized)   
                 
                rowWrite = [row[0], finalTweet, row[2], row[3], row[4], row[5], row[6], row[7]]
                
                if (line_count%100==0):
                    print(str(line_count)+" "+row[0])
                    
               
                writer = csv.writer(csvFile,delimiter=",")
                writer.writerow(rowWrite)
           
    
                #===================================================================================================================
                line_count += 1
                
csvFile.close()
