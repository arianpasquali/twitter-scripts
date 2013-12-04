from textblob import TextBlob
import csv
import ConfigParser
from optparse import OptionParser
import cld

_DEFAULT_OUTPUT_FILE = "result.csv"

_FIELDS = ["id",
"created_at",
"user_id",
"user_screen_name",
"user_name",
"user_description",
"user_created_at",
"user_followers_count",
"user_friends_count",
"user_statuses_count",
"user_listed_count",
"text",
"source",
"retweet_count",
"place_id",
"place_type",
"place_country_code",
"place_country",
"place_name",                                
"place_fullname",
"sentiment_name",
"sentiment_code"]

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

def decode_sentiment(value):
    if(value > 0.2):
        return 1,"Positive"
    else:
        if(value < -0.2):
            return -1,"Negative"
        else:
            return 0,"Neutral"



def process(input_file):
    count = 0
    
    reader = unicode_csv_reader(open(input_file))
    for status in reader:
        count = count + 1
        
        status_text = status[_FIELDS.index("text")]
        
        tb  = TextBlob(status_text)
        lang_detected = cld.detect(status_text.encode("utf-8"))
    
        # consider only english tweets
        if(lang_detected[0] == "ENGLISH"):
            sentiment = decode_sentiment(tb.sentiment[0])
            
            print str(count), sentiment[1]," - " ,status_text.encode("utf-8")
            
            try:
                csvwriter.writerow([
                                    status[_FIELDS.index("id")],
                                    status[_FIELDS.index("created_at")],
                                    status[_FIELDS.index("user_id")],
                                    status[_FIELDS.index("user_screen_name")],
                                    status[_FIELDS.index("user_name")].encode("utf-8"),
                                    status[_FIELDS.index("user_description")].encode("utf-8"),
                                    status[_FIELDS.index("user_created_at")],
                                    status[_FIELDS.index("user_followers_count")],
                                    status[_FIELDS.index("user_friends_count")],
                                    status[_FIELDS.index("user_statuses_count")],
                                    status[_FIELDS.index("user_listed_count")],
                                    status[_FIELDS.index("text")].encode("utf-8"),
                                    status[_FIELDS.index("source")].encode("utf-8"),
                                    status[_FIELDS.index("retweet_count")],
                                    status[_FIELDS.index("place_id")],
                                    status[_FIELDS.index("place_type")],
                                    status[_FIELDS.index("place_country_code")],
                                    status[_FIELDS.index("place_country")].encode("utf-8"),
                                    status[_FIELDS.index("place_name")].encode("utf-8"),
                                    status[_FIELDS.index("place_fullname")].encode("utf-8"),
                                    sentiment[1],
                                    sentiment[0]
                                    ])
            except Exception as e:
                print "Exception ", e

if __name__ == "__main__":
    cmd_parser = OptionParser(version="%prog 0.1")
    cmd_parser.add_option("-I", "--input", type="string", action="store", dest="input_file", help="Input file")
    cmd_parser.add_option("-O", "--output", type="string", action="store", dest="output_file", help="Output file", default=_DEFAULT_OUTPUT_FILE)

    (cmd_options, cmd_args) = cmd_parser.parse_args()
    
    if not (cmd_options.input_file):
        cmd_parser.print_help()
        sys.exit(3)        
    
    output_file_csv = open(cmd_options.output_file,"w")
    csvwriter = csv.writer(output_file_csv, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
    process(cmd_options.input_file)

