import re

class Cleaner:
    def clean_tweet(self, tweet):
        r = tweet.lower()
        r = re.sub("@[A-Za-z0-9_]+","", r)
        r = re.sub("#[A-Za-z0-9_]+","", r)
        r = re.sub(r'http\S+', '', r)
        r = re.sub('[()!?]', ' ', r)
        r = re.sub('\[.*?\]',' ', r)
        r = re.sub("[^a-z0-9]"," ", r)
        return r