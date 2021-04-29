import tweepy
import logging
import time
import pandas as pd
from datetime import date, timedelta
import csv
from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def search_tweets(api, text_query, coordinates, language, numTweets, max_id, all_tweets):
  logger.info('Retrieving tweets')
  for tweet in tweepy.Cursor(api.search, q=text_query, geocode=coordinates, lang=language, result_type='recent', max_id=max_id).items(numTweets):
    tweets_list = [tweet.created_at,  
                  tweet.user.screen_name, 
                  tweet.user.id_str, 
                  tweet.user.location, 
                  tweet.id_str,  
                  tweet.favorite_count,
                  tweet.retweet_count,   
                  tweet.entities['hashtags'],
                  tweet.text]
    all_tweets.append(tweets_list)

def main():
    text_query = 'vacunacion OR vacuna -filter:retweets'
    coordinates = '40.463667,-3.74922,250mi'
    language = 'es'
    numTweets = 500
    all_tweets = []
    max_id = 1385744943306534914
    api = create_api()
    numLoops = 0

    while numLoops < 18:
        search_tweets(api,text_query, coordinates, language, numTweets, max_id, all_tweets)
        data = pd.DataFrame(all_tweets)
        max_id = int(data[4].min())-1
        data.to_csv('22abril.csv', index=False)
        if max_id <= 1385019005325484033:
          break
        tweets_retrieved = len(all_tweets)
        logger.info('Tweets retrieved: ' + str(tweets_retrieved))
        logger.info('Waiting...')
        time.sleep(420)
        numLoops += 1
    
if __name__ == "__main__":
    main()