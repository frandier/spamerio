import tweepy

class Twitter: 
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(self.auth)
    
    def get_tweets(self, query, count, geocode, lang="es", result_type="recent"):
        filtered = query + "-filter:retweets"

        tweets = tweepy.Cursor(
            self.api.search_tweets, 
            q=filtered, 
            lang=lang,
            result_type=result_type,
            geocode=geocode
        ).items(count)

        return tweets