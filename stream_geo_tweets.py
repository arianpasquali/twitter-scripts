import sys
import tweepy
from textblob import TextBlob
import json, csv

consumer_key="GJGALwtkuTDljV3eBDAYaQ"
consumer_secret="lGENO2QQVasMzalcpp6A3fAciNO1u0wA2ZihMpibyY0"
access_key = "1689890738-QzDeXa7AvDQw7NUQeTaSjSgIE0Y6JRfZCNbMDwH"
access_secret = "f3pna4v7OnxbDtfwGsUhirlHrHHm2Vq4Jw92jrBN2o" 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

csvfile = open("tweet_facts.csv","w")
csvwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

class CustomStreamListener(tweepy.StreamListener):
    
    def compute_sentiment(self,textblob):
        value = textblob.sentiment
        
        return value
        
        # if(value > 0.2):
#             return "Positive"
#         else:
#             if(value < -0.2):
#                 return "Negative"
#             else:
#                 return "Neutral"
    
    def on_status(self, status):
        text = status.text
        # print text.encode("utf-8")
        if(status.place != None):
            bb = status.place
            
            retweet_count = 0;
            
            if( hasattr(status,"retweeted_status")):
                if(status.retweeted_status != None):    
                    retweet_count = status.retweeted_status.retweet_count
            
            user_bio = ""
            if(status.user.description != None):
                user_bio = status.user.description.encode("utf-8")
            
            print "-----------------------------------------------------------------------"
            print "who : ", status.user.name.encode("utf-8")
            print "when : ", status.created_at
            print "what : ", text.encode("utf-8")
            print "where: ", status.place.full_name.encode("utf-8")
            
            csvwriter.writerow([status.id,
                                status.created_at,
                                status.user.id,
                                status.user.screen_name,
                                status.user.name.encode("utf-8"),
                                user_bio,
                                status.user.created_at,
                                status.user.followers_count,
                                status.user.friends_count,
                                status.user.statuses_count,
                                status.user.listed_count,
                                status.text.encode("utf-8"),
                                status.source.encode("utf-8"),
                                retweet_count,
                                status.place.id,
                                status.place.place_type,
                                status.place.country_code,
                                status.place.country.encode("utf-8"),
                                status.place.name.encode("utf-8"),
                                status.place.full_name.encode("utf-8")
                                ])
            
        # text_blob  = TextBlob(text)
        # sentiment = self.compute_sentiment(text_blob)
        
        # if(int(sentiment[1]) != 0):
            # print sentiment, " - ", text_blob.detect_language()

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
# sapi.filter(track=['cristiano ronaldo'])
sapi.sample()