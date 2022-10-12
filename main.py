import os
import sys
import pandas as pd
import numpy as np
import spacy
from dotenv import load_dotenv
from pymongo import MongoClient
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from art import tprint

from twitter import twitter
from cleaner import cleaner

def main():
    tprint("SPAMERIO", font="rnd-medium")

    db = new_database()
    client = twitter.Twitter(
        os.environ.get("consumer_key"), 
        os.environ.get("consumer_secret"), 
        os.environ.get("access_token"), 
        os.environ.get("access_secret")
    )

    clean = cleaner.Cleaner()
    nlp = spacy.load("es_core_news_md")
    vectorizer = TfidfVectorizer(
        ngram_range=(1,2), 
        max_df=0.5, min_df=0.001, 
        max_features=None
    )

    """ tweets = get_tweets_from_twitter(client)
    save_tweets(db, tweets) """

    df = clean_and_normalize_tweets(db, clean, nlp)
    fit_transform = feature_extraction(df, vectorizer)

    # Sparse matrix problem
    with np.printoptions(threshold=np.inf):
        print(fit_transform[len(df)-1])

def new_database():
    try:
        client = MongoClient(os.environ.get("mongo_uri"))
        db = client.twitter
        return db
    except:
        print("Could not connect to MongoDB")

def get_tweets_from_twitter(client):
    try:
        query = str(input("Enter a search query: "))
        total = int(input("Enter the number of tweets to collect: "))
        tweets = client.get_tweets(query, total, "4.570868,-74.297333,100km")
        return tweets
    except:
        print("Could not get tweets")
        sys.exit(1)

def save_tweets(db, tweets):
    for tweet in tweets:
        tw = {
            "text": tweet.text,
            "user": tweet.user.screen_name,
            "location": tweet.user.location,
            "date": tweet.created_at
        }

        try:
            tw_id = db.tweets.insert_one(tw).inserted_id
            print("Tweet inserted with id: ", tw_id)
        except:
            print("Could not insert tweet")

def clean_and_normalize_tweets(db, clean, nlp):
    tweets = db.tweets.find()
    df = pd.DataFrame(list(tweets))
    df.drop(["_id", "date", "user", "location"], axis=1, inplace=True)

    cleaned_tweets = ( clean.clean_tweet(str(row)) for row in df['text'] )
    txt = [clean.lemma_stopwords_tweet(doc) for doc in nlp.pipe(cleaned_tweets, batch_size=50, n_process=-1)]
    df['cleaned_tweets'] = txt

    return df

def feature_extraction(df, vectorizer):
    fit_transform = vectorizer.fit_transform(df.cleaned_tweets.values).toarray()
    return fit_transform

if __name__ == "__main__":
    load_dotenv()
    main()