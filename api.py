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

		r = stuff("29jan_tweets.json")

		self.write(json.dumps(r, indent=4, ensure_ascii=False))

def app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

def stuff(file_name):
	dictionary, corpus = create_bag_of_words(file_name)
	num_topics = 10 # default

	create_lsi_model(file_name)
	num_topics = find_number_of_topics(file_name)
	print "=== Using " + str(num_topics) + " topics ==="

	return generate_topics(num_topics, corpus, dictionary)


if __name__ == "__main__":
    app = app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
