import sys
import tweepy
import csv
import ConfigParser
from optparse import OptionParser

_DEFAULT_CONFIG_FILE = "config.cfg"
_DEFAULT_OUTPUT_FILE = "tweets.csv"

class CustomStreamListener(tweepy.StreamListener):
        
    def on_status(self, status):
        text = status.text
        # print text.encode("utf-8")
        if(status.place != None):

            retweet_count = 0;
            
            if( hasattr(status,"retweeted_status")):
                if(status.retweeted_status != None):    
                    retweet_count = status.retweeted_status.retweet_count
            
            print "-----------------------------------------------------------------------"
            print "who  : ", status.user.name.encode("utf-8")
            print "when : ", status.created_at
            print "what : ", text.encode("utf-8")
            print "where: ", status.place.full_name.encode("utf-8")
            
            csvwriter.writerow([status.id,
                                status.created_at,
                                status.user.id,
                                status.user.screen_name,
                                status.user.name.encode("utf-8"),
                                status.user.description.encode("utf-8") if status.user.description != None else '',
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
                                status.place.full_name.encode("utf-8") if status.place.full_name != None else ''
                                ])
            
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


def open_stream(auth):
    print "Opening Twitter Stream"
    try:
        stream = tweepy.streaming.Stream(auth, CustomStreamListener())
        # sapi.filter(track=['pepsi'])
        stream.sample()
        
    except Exception as e:
        print "Exception ", e
        print "Reconnect"
        stream.disconnect()
        open_stream(auth)

def authenticate():    
    print "Authenticating"    
    config = ConfigParser.RawConfigParser()
    config.read(cmd_options.config_file)

    consumer_key = config.get("oauth","consumer_key")
    consumer_secret = config.get("oauth","consumer_secret")
    access_key = config.get("oauth","access_key")
    access_secret = config.get("oauth","access_secret")
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    
    api = tweepy.API(auth)
    
    return auth
    
if __name__ == "__main__":
    cmd_parser = OptionParser(version="%prog 0.1")
    cmd_parser.add_option("-C", "--config", type="string", action="store", dest="config_file", help="Config file", default=_DEFAULT_CONFIG_FILE)
    cmd_parser.add_option("-O", "--output", type="string", action="store", dest="output_file", help="Output file", default=_DEFAULT_OUTPUT_FILE)

    (cmd_options, cmd_args) = cmd_parser.parse_args()
    
    csvfile = open(cmd_options.output_file,"w")
    csvwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
    auth = authenticate()
    open_stream(auth)