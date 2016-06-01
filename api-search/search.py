import twitter
from topic.keys import *

api = twitter.Api(consumer_key = CONSUMER_KEY,
				consumer_secret = CONSUMER_SECRET,
				access_token_key = ACCESS_TOKEN,
				access_token_secret = ACCESS_TOKEN_SECRET)

# search for tweets by keyword
tweets = api.GetSearch("donald trump", count=50)

for tweet in tweets:
	d = {"text": tweet.text, "id": tweet.id}
	print d
