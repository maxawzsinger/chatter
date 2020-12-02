import twint 
from datetime import timedelta, date, datetime
import random
import pandas as pd
from alpha_vantage.timeseries import TimeSeries





def tweetscrape(stock_list, window):

	stock_series = {} #1st return value - holds time series 
	stock_examples = {} #2nd return value - holds random tweets for each stock as decoration



	#stock_list is list of strings of format 'AAPL'
	#window should be integer of either 1, 7, 30, 183, 365 (days)

	#producing date string for config 
	date_range = date.today() + timedelta(days=-window)
	date_string = date_range.strftime('%Y-%m-%d')

	#setting default configs
	c = twint.Config()
	c.Since = date_string
	c.Hide_output = True
	c.Store_object = True

	#alphavantage config

	ts = TimeSeries(key='JCLZ7M60COAOXC66') #my unique alphavantage key




	#iterating over stock list, storing in stock_series
	#as {stock:{date:mentions, date:mentions}}

	for stock in stock_list:


		c.Search= '$'+stock #$ added for twitter


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

			for tweet in tweets:
				tweet_datetime = tweet.datestamp + ' ' + tweet.timestamp
				if tweet_datetime not in mentions:
					mentions[tweet_datetime] = 1
				else:
					mentions[tweet_datetime] += 1

		stock_series[stock] = mentions

		# pulling data from alpha_vantage

		data, meta_data = ts.get_intraday(stock)

		#combining data - "time windows" created by the alpha vantage times
		tweets_vs_stock = {}

		pruned_mentions = mentions #size will change during iteration, stores a record
		tweet_mentions = mentions
		for stock_time, prices in data.items():

			stock_dt = datetime.strptime(stock_time,
                           '%Y-%m-%d %H:%M:%S')
			stock_ssepoch = stock_dt.timestamp()

			close_price = prices['4. close']

			new_stock_time = True

			for tweet_time, tweet_vol in tweet_mentions.items():
				#convert key to comparable dt object (currently only a time no date)
				tweet_dt = datetime.strptime(tweet_time,
                           '%Y-%m-%d %H:%M:%S')
				tweet_ssepoch = tweet_dt.timestamp()

				if tweet_ssepoch > stock_ssepoch:

					if new_stock_time:
						tweets_vs_stock[stock_time] = {
						'price':close_price,
						'tweet_vol' : tweet_vol
						}

						new_stock_time = False
						del pruned_mentions[tweet_time]
					else:
						tweets_vs_stock[stock_time]['tweet_vol'] += tweet_vol
						del pruned_mentions[tweet_time]
				else:
					break
			tweet_mentions = pruned_mentions











	return stock_series,stock_examples, tweets_vs_stock


#test

stock_list = ['TSLA']
window = 1 #change this to grab tweets from same range as the alphavantage..

print('window: ', window)

print(tweetscrape(stock_list,window))





