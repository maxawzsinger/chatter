import twint 
from datetime import timedelta, date, datetime
import random
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from pytz import timezone



import pandas as pd

#some important values:




def tweetscrape(stock_list, window):

	#return values
	stock_series = {} #1st return value - holds time series 
	stock_examples = {} #2nd return value - holds random tweets for each stock as decoration

	#combining data - "time windows" created by the alpha vantage times
	tweets_vs_stock = {}

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

		#get tweets

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

			#convert datetime to seconds for comparison to stock time series
			for tweet in tweets:
				tweet_dt = datetime.strptime(tweet.datestamp+ tweet.timestamp, '%Y-%m-%d%H:%M:%S') #tweet[0] is time
				tweet_ssepoch = tweet_dt.timestamp()

				if tweet.timestamp >= '04:00:00' and tweet.timestamp <= '20:00:00':

					if tweet_ssepoch not in mentions:
						mentions[tweet_ssepoch] = 1
					else:
						mentions[tweet_ssepoch] += 1
			#there are sometimes duplicates on same timestamp, this stacks duplicates on top of each other


			#convert tweet dict to list for indexing allowing for loop to look at
			#subsequent smaller and smaller slices 
			tweet_list = []
			for ssepoch, vol in mentions.items():
				temp = [ssepoch,vol]
				tweet_list.append(temp)

		else:
			return "no tweet data"


		# pulling data from alpha_vantage

		data, meta_data = ts.get_intraday(stock, interval='1min')

		# pruned_mentions = mentions #size will change during iteration, stores a record
		# tweet_mentions = mentions

		

		ssepoch_stocks = {}

		for stock_time in data:
			stock_dt = datetime.strptime(stock_time,'%Y-%m-%d %H:%M:%S')
			stock_ssepoch = stock_dt.timestamp()
			ssepoch_stocks[stock_ssepoch] = data[stock_time]['4. close']

		start_index = 0 #allow for loop to look at smaller and smaller subsample


		for ssepoch, price in ssepoch_stocks.items():

			new_stock_time = True

			for tweet in tweet_list[start_index:]:
				#convert key to comparable dt object (currently only a time no date)
				# tweet_dt = datetime.strptime(tweet[0], '%Y-%m-%d %H:%M:%S') #tweet[0] is time
				# tweet_ssepoch = tweet_dt.timestamp()
				print('tweet time: ',tweet[0], 'stock time: ', stock_ssepoch)
				print('is larger: ', tweet[0] > stock_ssepoch)

				if tweet[0] > ssepoch:

					print('adding')


				if tweet[0] > ssepoch:

					if new_stock_time:
						tweets_vs_stock[ssepoch] = {
						'price': price,
						'tweet_vol' : tweet[1] #tweet[1] is tweet volume
						}

						new_stock_time = False
						start_index += 1
					else:
						tweets_vs_stock[ssepoch]['tweet_vol'] += tweet[1] #tweet[1] is tweet volume
						start_index +=1
				if tweet[0] < ssepoch:
					print('attemping to break')
					break
			print('successfully broke')



			
			#CHANGE WINDOW TO BE

			#refactor code into smaller chunks, seperate functions (not so monolithic)
			#save sections of code so i can run my scripts faster....

				#	experiment with smaller sample size..








	return tweets_vs_stock

	# for time, values in tweets_vs_stock.items():
	# 	if



#test

stock_list = ['TSLA']
window = 3 #change this to grab tweets from same range as the alphavantage..



output = tweetscrape(stock_list, window)



tweet_time = []
tweet_value = []

stock_time = []

stock_value = []

for time, values in output.items():

	tweet_time.append(time)
	stock_time.append(time)
	tweet_value.append(values['tweet_vol'])
	stock_value.append(values['price'])


df = pd.DataFrame({
	'tweet_vol': tweet_value,
	'stock_price': stock_value
	}, index=tweet_time)

print(df)

lines = df.plot.line()

df.to_csv(r'/Users/stu/Desktop/tweettest/tweet/chatter/chatter/stonks3.csv')






