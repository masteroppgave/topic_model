import tornado.ioloop
import tornado.web
import json
from topic_model import generate_lda_topics, generate_hdp_topics
from bag_of_words import create_bag_of_words
from num_topics import create_lsi_model
from num_topics import find_number_of_topics
from pymemcache.client.base import Client

client = Client(('localhost', 11211))

class LdaHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Content-Type', 'application/json')

		passes = self.get_argument("passes", 1, True)
		num_topics = self.get_argument("num_topics", 0, True)
		json_file=self.get_argument("json", "27jan_tweets", True)

		# Get result from memcache if exists
		key = "lda" + str(passes) + str(num_topics) + json_file
		#client.delete(key)
		res = client.get(key)

		if res:
			response = json.loads(res)
		else:
			if not "." in json_file:
				json_file += ".json"

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
			print client.get(key)

		self.write(json.dumps(response, indent=4, ensure_ascii=False))

class HdpHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Content-Type', 'application/json')

		num_topics = self.get_argument("num_topics", 0, True)
		json_file = self.get_argument("json", "27jan_tweets", True)

		# Get result from memcache if exists
		key = "hdp" + str(num_topics) + json_file
		#client.delete(key)
		res = client.get(key)

		if res:
			response = json.loads(res)
		else:
			if not "." in json_file:
				json_file += ".json"

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

		self.write(json.dumps(response, indent=4, ensure_ascii=False))

def app():
    return tornado.web.Application([
        (r"/lda", LdaHandler),
        (r"/hdp", HdpHandler),
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


if __name__ == "__main__":
    app = app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
