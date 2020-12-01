import twint 
from datetime import timedelta, date
import random

def tweetscrape(stock_list, window):

	#stock_list is list of strings of format '$AAPL'
	#window should be integer of either 1, 7, 30, 183, 365 (days)

	#producing date string for config 
	date_range = date.today() + timedelta(days=-window)
	date_string = date_range.strftime('%Y-%m-%d')

	#setting default configs
	c = twint.Config()
	c.Since = date_string
	c.Hide_output = True
	c.Store_object = True


	stock_series = {} #holds time series 

	stock_examples = {} #holds random tweets for each stock as decoration

	#iterating over stock list, storing in stock_series
	#as {stock:{date:mentions, date:mentions}}

	for stock in stock_list:


		c.Search=stock


		twint.run.Search(c)
		tweets = twint.output.tweets_list

		tweets_length = len(tweets)

		if tweets_length > 0:

			#selecting a random tweet to accompany stock info

			rand_tweet = tweets[random.randint(0, tweets_length)]

			tweet_deets  = {

				'date' : rand_tweet.datestamp,
				'time' : rand_tweet.timestamp,
				'username' : rand_tweet.username,
				'tweet' : rand_tweet.tweet

			}

			stock_examples[stock] = tweet_deets

			
			#iterating over tweets list adding up mentions in mentions dict
			mentions = {}

			# for tweet in tweets:
			# 	if tweet.datestamp not in mentions:
			# 		mentions[tweet.datestamp] = 0
			# 	else:
			# 		mentions[tweet.datestamp] += 1

			for tweet in tweets:
				if tweet.timestamp not in mentions:
					mentions[tweet.timestamp] = 0
				else:
					mentions[tweet.timestamp] += 1

		stock_series[stock] = mentions

	return stock_series,stock_examples


#test

stock_list = ['$TSLA']
window = 1

print('window: ', window)

print(tweetscrape(stock_list,window))





