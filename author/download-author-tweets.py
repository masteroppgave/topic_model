from topic.keys import *
import tweepy
import json
import os

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def get_tweets_by_user(username, all_metadata=False, discard_quote = True, discard_media = False, discard_urls=True, discard_replies=True, discard_directed_tweets=True, discard_retweets=True):

	all_tweets = []

	tweets = api.user_timeline(screen_name=username, count=200)

	all_tweets.extend(tweets)
	oldest = all_tweets[-1].id - 1

	while tweets:
		tweets = api.user_timeline(screen_name = username, count=200, max_id=oldest)

		all_tweets.extend(tweets)

		oldest = all_tweets[-1].id - 1

		print "...%s tweets downloaded so far" % (len(all_tweets))

	file_name = "%s_tweets.json" % (username)
	print "Done fetching %s tweets. Writing to file %s" % (len(all_tweets), file_name)

	with open(os.path.join("data/tweets", file_name), "a") as f:
		for i, line in enumerate(all_tweets):
			dict_tweet = line._json

			if discard_replies and dict_tweet["in_reply_to_status_id"]:
				print "Discarding reply"
				continue

			if discard_directed_tweets and dict_tweet["text"][0]=="@":
				print "Discard tweet directed at another user"
				continue

			if discard_retweets and dict_tweet["text"].startswith("RT @"):
				print "Dicarding retweet"
				continue

			if discard_urls and dict_tweet["entities"]["urls"]:
				print "Discarding tweet containing url"
				continue

			if discard_media and "media" in dict_tweet["entities"]:
				print "Discarding tweet containing media"
				continue

			if discard_quote and dict_tweet["text"].startswith("\"@"):
				print "Discarding quote"
				continue

			print("%s/%s" % (i, len(all_tweets)))

			if all_metadata:
				f.write(json.dumps(dict_tweet) + "\n")
			else:
				f.write(json.dumps({"text": dict_tweet["text"], "screen_name": dict_tweet["user"]["screen_name"], "created_at": dict_tweet["created_at"]}) + "\n")


#get_tweets_by_user("justinbieber")
#get_tweets_by_user("BarackObama")