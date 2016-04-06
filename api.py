import tornado.ioloop
import tornado.web
import json
from lda import generate_topics
from bag_of_words import create_bag_of_words
from num_topics import create_lsi_model
from num_topics import find_number_of_topics

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Content-Type', 'application/json')

		passes = self.get_argument("passes", 1, True)
		num_topics = self.get_argument("num_topics", 0, True)
		json_file=self.get_argument("json", "29jan_tweets", True)

		if not "." in json_file:
			json_file += ".json"

		topics = run_lda(json_file, int(passes), int(num_topics))

		response = {"file": json_file, "topics": topics, "num_topics": len(topics.keys()), "passes": passes}

		self.write(json.dumps(response, indent=4, ensure_ascii=False))

def app():
    return tornado.web.Application([
        (r"/lda", MainHandler),
    ])

def run_lda(file_name, passes, num_topics):
	dictionary, corpus = create_bag_of_words(file_name)

	if not num_topics:
		print("Number of topics not provided. Finding optimal number of topics by using the Elbow method.")
		create_lsi_model(file_name)
		num_topics = find_number_of_topics(file_name)

	print "=== Using " + str(num_topics) + " topics ==="

	return generate_topics(num_topics, corpus, dictionary, passes)


if __name__ == "__main__":
    app = app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
