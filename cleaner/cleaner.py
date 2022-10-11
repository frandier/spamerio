import re

class Cleaner:
    def clean_tweet(self, tweet):
        r = tweet.lower()
        r = re.sub("(@[A-Za-z0-9_]+)", ' ', r)
        r = re.sub(r'((?<=[A-Za-z])(?=[A-Z][a-z]))',' ', r)
        r = re.sub("([^A-Za-z0-9äÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])",' ', r)
        r = re.sub("(\w+:\/\/\S+)",' ', r)
        r = ' '.join(r.split())
        return r