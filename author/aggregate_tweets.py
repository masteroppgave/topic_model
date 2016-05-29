import json

def aggregate_tweets(_file, _out):
	out_string = ""

	for line in open(_file).readlines():
		line = json.loads(line)
		
		out_string += "%s\n" % line["text"]

	out = open("aggregated_%s_.json" % _out, "a")

	out.write("".join(char for char in out_string if ord(char) < 128))

if __name__=="__main__":
	print aggregate_tweets("data/tweets/rosen/taylorswift13_tweets.json", "taylorswift13")
