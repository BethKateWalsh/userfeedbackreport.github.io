import pymysql.cursors
from textblob.classifiers import NaiveBayesClassifier
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import preprocessor as p

# Connect to MYSQL database
dbServerName = "localhost"
dbUser = "root"
dbPassword = "woodycool123"
dbName = "azure_support_tweets"
cusrorType = pymysql.cursors.DictCursor

connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset='utf8mb4', cursorclass=cusrorType)


# NLTK objects created
porter = PorterStemmer()
wnl = WordNetLemmatizer()

# Get tweets from raw_tweets and process
try:
    # Create a cursor object
    cursorObject = connectionObject.cursor()

    # Create new table for processed tweets IF DOSE NOT ALREADY EXSIST
    sqlQuery = "CREATE TABLE IF NOT EXISTS preprocessed_tweets(id_tweet varchar(200), text_tweet text)"

    # Execute the sqlQuery
    cursorObject.execute(sqlQuery)

    # Select id_tweet
    cursorObject.execute("SELECT id_tweet, text_tweet FROM raw_tweets")
    for i in cursorObject.fetchall():
        id_tweet = i["id_tweet"];
        text_tweet = i["text_tweet"];

        # tweet-preprocessor library
        p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.RESERVED, p.OPT.SMILEY, p.OPT.NUMBER)
        text_tweet = p.clean(text_tweet)

        # Case folding
        text_tweet = text_tweet.casefold()

        # Tokenize
        tokenized_tweet = word_tokenize(text_tweet)

        # Stemming (Stop it removing the from words!)
        stemmed_tweet_words = []
        for tweet in tokenized_tweet:
            if tweet.endswith("e"):
                stemmed_tweet_words.append(wnl.lemmatize(tweet))
            else:
                stemmed_tweet_words.append(porter.stem(tweet))

        # Put string back together
        text_tweet = " ".join(stemmed_tweet_words)

        # Remove hashtags but keep the words and special characters
        text_tweet = text_tweet.replace("#", "")
        text_tweet = re.sub(r'([^\s\w]|_)+', ' ', text_tweet)

        # Remove multiple spaces
        text_tweet = ' '.join(text_tweet.split())

        # Add tweet text and id to table
        addrowQuery = 'INSERT INTO preprocessed_tweets (id_tweet, text_tweet) VALUES (%s, %s);'
        cursorObject.execute(addrowQuery, (id_tweet, text_tweet))
        connectionObject.commit()

except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connectionObject.close()