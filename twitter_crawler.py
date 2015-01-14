#!/usr/bin/env python
# -*- coding: utf-8  -*-
#encoding=utf-8

import tweepy
import time
import sys
from random import randint
import constants

class TwitterCrawler():
    # Fill in the blanks here for your own Twitter app.
    consumer_key = constants.consumer_key
    consumer_secret = constants.consumer_secret
    access_key = constants.access_key
    access_secret = constants.access_secret
    auth = None
    api = None

    def __init__(self):
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(self.auth, parser=tweepy.parsers.JSONParser())
        #print self.api.rate_limit_status()

    def re_init(self):
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(self.auth, parser=tweepy.parsers.JSONParser())

    def check_api_rate_limit(self, sleep_time):
        try:
            rate_limit_status = self.api.rate_limit_status()
        except Exception as error_message:
            if error_message['code'] == 88:
                print "Sleeping for %d seconds." %(sleep_time)
                #print rate_limit_status['resources']['statuses']
                time.sleep(sleep_time)

        while rate_limit_status['resources']['statuses']['/statuses/user_timeline']['remaining'] < 10:
            print "Sleeping for %d seconds." %(sleep_time)
            #print rate_limit_status['resources']['statuses']
            time.sleep(sleep_time)
            rate_limit_status = self.api.rate_limit_status()
        #print rate_limit_status['resources']['statuses']['/statuses/user_timeline']

    def crawl_user_profile(self, user_id):
        self.check_api_rate_limit(900)
        try:
            user_profile = self.api.get_user(user_id)
        except:
            return None
        return user_profile

    def crawl_user_tweets(self, user_id, count):
        self.check_api_rate_limit(900)
        try:
            tweets = self.api.user_timeline(screen_name = user_id, count = count)
        except:
            tweets = None
        tried_count = 0
        while len(tweets) < count:
            try:
                tweets.extend(self.api.user_timeline(user_id, count = count))
            except:
                pass
            tried_count += 1
            if tried_count == 3:
                break
        return tweets[:count]
    
    def get_tweets_text(self, tweets):
        for tweet in tweets:
            print tweet['text']
    
    def search_query(self, query, count):
        self.check_api_rate_limit(900)
        try:
            tweets = self.api.search(query, count=count)
        except:
            tweets = None
        tried_count = 0
        while len(tweets) < count:
            try:
                tweets.extend(self.api.search(query, count= count))
            except:
                pass
            tried_count += 1
            if tried_count == 3:
                break
        return tweets
    
    def get_query_search_text(self, tweets):
        for tweet in tweets['statuses']:
            print tweet['text']
    
    def write_data_to_file(self,tweets,filename):
        f = open(filename, 'w+')
        count = 0
        for tweet in tweets['statuses']:
            count += 1
            f.write(tweet['text'].encode('ascii', 'ignore')+'\n')
        return count
    
    def get_single_string_for_tweets(self, tweets):
        line = ""
        for tweet in tweets['statuses']:
            line += tweet['text'].encode('ascii', 'ignore')+' '
        return line
        
        
def main():
    tc = TwitterCrawler()
    tc.check_api_rate_limit(900)
    query = "Satya Nadella"
    #user = tc.crawl_user_profile('satyanadella')
    #print user
    #tweets = tc.crawl_user_tweets('satya nadella', 5)
    #tc.get_tweets_text(tweets)
    tweets = tc.search_query(query, 5)
    #total_tweets = tc.write_data_to_file(tweets, query)
    print tc.get_single_string_for_tweets(tweets)

if __name__ == "__main__":
    main()