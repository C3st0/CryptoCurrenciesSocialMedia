
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import csv

#Variables that contains the user credentials to access Twitter API 
access_token = "1D"
access_token_secret = "IZn"
consumer_key = "onzDI5"
consumer_secret = "xNPa"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        decoded = json.loads(data)
        print (decoded['user']['screen_name'],decoded['created_at'], decoded['text'].encode('utf-8', 'ignore'))

        with open('C:\\Users\\Public\\Documents\\twitterstreemAPI-dataNEW.txt', 'a',encoding='utf-8') as f: 
            f.write(';')
            writer = csv.writer(f)
            writer.writerow([decoded['user']['screen_name'],decoded['cretated_at'], decoded['text'].encode('utf-8', 'ignore')])
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #-----------------------------------------------------------------------------------------------------------------------------------

    def start_stream():
        while True:
            try:
                stream = Stream(auth, l)

                #This line filter Twitter Streams to capture data by the keyword: 'btc'
                stream.filter(track=['btc','bitcoin'])
            except: 
                continue

    start_stream()


    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------