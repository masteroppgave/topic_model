import tornado.ioloop
import tornado.web
import json
from topic_model import generate_lda_topics, generate_hdp_topics
from bag_of_words import create_bag_of_words
from num_topics import create_lsi_model
from num_topics import find_number_of_topics
from hashtags import most_common
from pymemcache.client.base import Client
import hashlib
from random import randint
import twitter
from topic.keys import *

api = twitter.Api(consumer_key = CONSUMER_KEY,
				consumer_secret = CONSUMER_SECRET,
				access_token_key = ACCESS_TOKEN,
				access_token_secret = ACCESS_TOKEN_SECRET)

def search_twitter(query, count=50):
	tweets = api.GetSearch(query, count=count, lang="en")

	return [{"text": tweet.text, "_id": str(tweet.id), "sentiment": get_sentiment("yo")} for tweet in tweets]

client = Client(('localhost', 11211))

def get_sentiment(text):
	return ["positive", "neutral", "negative"][randint(0,2)]

class SearchTwitterSentimentHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Content-Type', 'application/json')

		query = self.get_argument("query", "donald trump", True)

		tweets = search_twitter(query)

		pos = sum([el["sentiment"]=="positive" for el in tweets])
		neu = sum([el["sentiment"]=="neutral" for el in tweets])
		neg = sum([el["sentiment"]=="negative" for el in tweets])

		d = {}

		d["array"] = tweets
		d["num_positive"] = pos
		d["num_neutral"] = neu
		d["num_negative"] = neg

		self.write(json.dumps(d, indent=4, ensure_ascii=False))

class SimpleSentimentHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Content-Type', 'application/json')

		text = self.get_argument("text", "test", True)

		sentiment = get_sentiment("text")

		self.write(json.dumps({"sentiment": sentiment}, indent=4, ensure_ascii=False))


class HashtagCooccurrenceHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Content-Type', 'application/json')

		json_file=self.get_argument("json", "29jan_tweets", True)

		if not "." in json_file:
			json_file += ".json"

		f = open(json_file)

		# Get result from memcache if exists
		print("Getting md5sum for memcache")
		md5sum_file = md5sum(json_file)
		print("MD5: " + md5sum_file)
		key = "hashtag" + md5sum(json_file)
		#client.delete(key)
		res = client.get(key)

class TopHashtagsHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Content-Type', 'application/json')

		json_file=self.get_argument("json", "29jan_tweets", True)
		num_hashtags = int(self.get_argument("num_hashtags", 20, False))

		if not "." in json_file:
			json_file += ".json"

		f = open(json_file)

		# Get result from memcache if exists
		print("Getting md5sum for memcache")
		md5sum_file = md5sum(json_file)
		print("MD5: " + md5sum_file)
		key = "most_common_hashtag" + md5sum(json_file)
		#client.delete(key)
		res = client.get(key)

		response = most_common(f.readlines(), num_hashtags)
		response["json_file"] = json_file

		self.write(json.dumps(response, indent=4, ensure_ascii=False))


class LdaHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Content-Type', 'application/json')

		passes = self.get_argument("passes", 1, True)
		num_topics = self.get_argument("num_topics", 0, True)
		json_file=self.get_argument("json", "29jan_tweets", True)

		if not "." in json_file:
			json_file += ".json"

		# Get result from memcache if exists
		print("Getting md5sum for memcache")
		md5sum_file = md5sum(json_file)
		print("MD5: " + md5sum_file)
		key = "lda" + str(passes) + str(num_topics) + md5sum(json_file)
		#client.delete(key)
		res = client.get(key)

		if res:
			print("Found in memcache!")
			response = json.loads(res)
		else:
			print("Not found in memcache.")
			topics = run_lda(json_file, int(passes), int(num_topics))
			topics = list(topics.values())

			print "===TOPICS==="
			print topics

			new_topics = []

			for topic in topics:
				temp_tokens = []
				tokens = topic.split(" + ")
				for token in tokens:
					t = {}
					t["percentage"], t["value"] = token.split("*")
					temp_tokens.append(t)
				new_topics.append(temp_tokens)

			response = {"file": json_file, "topics": new_topics, "num_topics": topics, "passes": passes, "method": "LDA"}
			client.set(key, json.dumps(response))
			print("Added result to memcache.")

		self.write(json.dumps(response, indent=4, ensure_ascii=False))

class HdpHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Content-Type', 'application/json')

		num_topics = self.get_argument("num_topics", 0, True)
		json_file = self.get_argument("json", "29jan_tweets", True)

		if not "." in json_file:
			json_file += ".json"

		# Get result from memcache if exists
		print("Getting md5sum for memcache")
		md5sum_file = md5sum(json_file)
		print("MD5: " + md5sum_file)
		key = "hdp" + str(num_topics) + md5sum(json_file)
		#client.delete(key)
		res = client.get(key)

		if res:
			print("Found in memcache!")
			response = json.loads(res)
		else:
			print("Not found in memcache.")
			topics = run_hdp(json_file, int(num_topics))
			topics = list(topics.values())

			print "===TOPICS==="
			print topics

			new_topics = []

			for topic in topics:
				temp_tokens = []
				tokens = topic.split(" + ")
				for token in tokens:
					t = {}
					t["percentage"], t["value"] = token.split("*")
					temp_tokens.append(t)
				new_topics.append(temp_tokens)

			response = {"file": json_file, "topics": new_topics, "num_topics": topics, "method": "HDP"}
			client.set(key, json.dumps(response))
			print("Added result to memcache.")

		self.write(json.dumps(response, indent=4, ensure_ascii=False))

def app():
    return tornado.web.Application([
        (r"/lda", LdaHandler),
        (r"/hdp", HdpHandler),
        (r"/hashtags/common", TopHashtagsHandler),
        (r"/sentiment", SimpleSentimentHandler),
        (r"/sentiment/search", SearchTwitterSentimentHandler),
    ])

def run_lda(file_name, passes, num_topics):
	dictionary, corpus = create_bag_of_words(file_name)

	if not num_topics:
		print("Number of topics not provided. Finding optimal number of topics by using the Elbow method.")
		create_lsi_model(file_name)
		num_topics = find_number_of_topics(file_name)

	print "=== Using " + str(num_topics) + " topics ==="

	return generate_lda_topics(num_topics, corpus, dictionary, passes)

def run_hdp(file_name, num_topics):
	dictionary, corpus = create_bag_of_words(file_name)

	if not num_topics:
		print("Number of topics not provided. Finding optimal number of topics by using the Elbow method.")
		create_lsi_model(file_name)
		num_topics = find_number_of_topics(file_name)

	print "=== Using " + str(num_topics) + " topics ==="

	return generate_hdp_topics(num_topics, corpus, dictionary)

def md5sum(filename, blocksize=2**16):
    _hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            _hash.update(block)
    return _hash.hexdigest()


if __name__ == "__main__":
    app = app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
