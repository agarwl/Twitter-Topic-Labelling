#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import sys

#Twitter API credentials
consumer_key = "rBBYLyLixN2LUMu6Tl7kb07mx"
consumer_secret = "v6Dq1RLF7TPrccdskvMTahlMaGPGFsQ0AnvQxDgCaBsesDm9iy"
access_key = "726727268391878656-wl60horopZ4HoGpwaJWXZ4Bl9ZkvD7f"
access_secret = "3xaa3QpuJY3jdFj7xNW9b2oEqTWtvrjkySvffaYiZWwbB"



#returns true is the tweet is a text tweet
def not_photo_tweet(tweet):
    try:
        if(tweet.entities['media'][0]['type'] == 'photo'):
            return False
    except:
        try:
            if tweet.entities['urls'][0]['expanded_url']:
                return False
        except:
            pass
        # if 'youtube' in json.load(urllib2.urlopen('http://api.longurl.org/v2/expand?url=' + tweet.entities['urls'][0]['expanded_url']+'&format=json'))['long-url']:

    return True

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save the id of the oldest tweet less one
    oldest = new_tweets[-1].id - 1

    new_tweets = [tweet for tweet in new_tweets if (not_photo_tweet(tweet) and tweet.lang == 'en')]
    #save most recent tweets
    alltweets.extend(new_tweets)

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        new_tweets = [tweet for tweet in new_tweets if (not_photo_tweet(tweet) and tweet.lang == 'en')]
        #save most recent tweets
        alltweets.extend(new_tweets)

         #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    # transform the tweepy tweets into a 2D array that will populate the csv
    # outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    outtweets = [[i.id_str,i._json['user']['name'],i.text.encode('utf-8'),i.entities['hashtags'],i.in_reply_to_status_id] for i in alltweets]

    #write the csv
    with open('%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","posted_by","text","hashtags","in_reply_to_status_id"])
        writer.writerows(outtweets)

    pass


if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets(sys.argv[1])