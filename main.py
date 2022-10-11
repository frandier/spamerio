import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
from twitter import twitter
from cleaner import cleaner

def main():
    db = new_database()
    client = twitter.Twitter(
        os.environ.get("consumer_key"), 
        os.environ.get("consumer_secret"), 
        os.environ.get("access_token"), 
        os.environ.get("access_secret")
    )
    clean = cleaner.Cleaner()

    try:
        query = str(input("Enter a search query: "))
        tweets = client.get_tweets(query, 1, "4.570868,-74.297333,100km")
    except:
        print("Could not get tweets")
        sys.exit(1)


    for tweet in tweets:
        tw = {
            "text": clean.clean_tweet(tweet.text),
            "user": tweet.user.screen_name,
            "location": tweet.user.location,
            "date": tweet.created_at
        }

        try:
            tw_id = db.tweets.insert_one(tw).inserted_id
            print("Tweet inserted with id: ", tw_id)
        except:
            print("Could not insert tweet")

def new_database():
    try:
        client = MongoClient(os.environ.get("mongo_uri"))
        db = client.twitter
        return db
    except:
        print("Could not connect to MongoDB")

if __name__ == "__main__":
    load_dotenv()
    main()